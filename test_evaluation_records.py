"""Regression checks for stale judgments and cross-run human-grade leakage."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from evaluation_records import digest, resolve_run, load_bound_verdicts, historical_human_validation


class EvaluationRecordsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root/'eval/runs/original-saved-id'
        self.directory.mkdir(parents=True)
        self.write('eval/latest_run.json', {'run_id':'original-saved-id','directory':'eval/runs/original-saved-id'})
        self.write('eval/runs/original-saved-id/answers.json', {'q':{'answer':'Original answer'}})
        self.write('eval/runs/original-saved-id/answers_manifest.json', {'generation_id':'generation-1','answers_sha256':digest(self.directory/'answers.json')})

    def write(self, path, value):
        file = self.root/path
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_text(json.dumps(value))

    def test_orchestration_change_reuses_bound_answers_but_generation_change_does_not(self):
        self.assertEqual(resolve_run(self.root,'generation-1')[0], 'original-saved-id')
        self.assertEqual(resolve_run(self.root,'changed-prompt-generation')[0], 'changed-prompt-generation')

    def test_edited_answers_are_not_silently_reused(self):
        self.write('eval/runs/original-saved-id/answers.json', {'q':{'answer':'Changed'}})
        with self.assertRaisesRegex(ValueError,'answers changed'):
            resolve_run(self.root,'generation-1')

    def test_modified_answers_questions_rubric_or_verdicts_reject_judge_cache(self):
        import hashlib
        questions=self.root/'eval/questions.csv';questions.write_text('original questions')
        verdicts={'q':{'correct':True,'supported':True,'bad_test_question':False,'reasoning':'Fixture evidence'}}
        self.write('eval/runs/original-saved-id/judge_draft.json', verdicts)
        manifest={'answers_sha256':digest(self.directory/'answers.json'),'questions_sha256':digest(questions),'rubric_sha256':hashlib.sha256(b'original rubric').hexdigest(),'verdict_file':'judge_draft.json','verdicts_sha256':digest(self.directory/'judge_draft.json')}
        self.write('eval/runs/original-saved-id/judgment_manifest.json',manifest)
        self.assertEqual(load_bound_verdicts(self.root,self.directory,{'q':{}},'original rubric'),verdicts)
        for file in [self.directory/'answers.json',questions,self.directory/'judge_draft.json']:
            with self.subTest(file=file.name):
                original=file.read_bytes();file.write_bytes(original+b' ')
                with self.assertRaisesRegex(ValueError,'evidence changed'):
                    load_bound_verdicts(self.root,self.directory,{'q':{}},'original rubric')
                file.write_bytes(original)
        with self.assertRaisesRegex(ValueError,'evidence changed'):
            load_bound_verdicts(self.root,self.directory,{'q':{}},'changed rubric')

    def test_historical_grades_compare_only_to_original_judge(self):
        answers={f'q{i}':{} for i in range(20)}
        verdicts={id:{'correct':True,'supported':False} for id in answers}
        self.write('eval/runs/history/answers.json',answers)
        self.write('eval/runs/history/judge_draft.json',verdicts)
        (self.root/'eval/human_labels_run.txt').write_text('history\n')
        self.write('eval/human_validation_provenance.json',{'role':'Synthetic unit-test fixture only'})
        with (self.root/'eval/human_labels.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['id','correct','supported','notes']);w.writeheader()
            w.writerows({'id':id,'correct':'1','supported':'0','notes':'Fixture unsupported claim'} for id in answers)
        result=historical_human_validation(self.root,'different-current-run','history')
        self.assertFalse(result['applies_to_current_answers'])
        self.assertEqual(result['agreement_with_original_judge']['both'],1)
        with self.assertRaisesRegex(ValueError,'separate run'):
            historical_human_validation(self.root,'history','history')
        with self.assertRaisesRegex(ValueError,'binding differs'):
            historical_human_validation(self.root,'different-current-run','another-history')


if __name__=='__main__':unittest.main()
