"""Content-bound evaluation records; never transfer human labels across runs."""
import csv
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_run(root: Path, generation_id: str) -> tuple[str, Path]:
    latest = root / 'eval/latest_run.json'
    if latest.exists():
        saved = json.loads(latest.read_text())
        directory = root / saved['directory']
        if not directory.resolve().is_relative_to((root / 'eval/runs').resolve()):
            raise ValueError('Saved run path is outside eval/runs.')
        manifest_path = directory / 'answers_manifest.json'
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
            if manifest['generation_id'] == generation_id:
                if manifest['answers_sha256'] != digest(directory / 'answers.json'):
                    raise ValueError('Saved answers changed; do not reuse their judge verdicts.')
                return saved['run_id'], directory
    return generation_id, root / 'eval/runs' / generation_id


def load_bound_verdicts(root: Path, directory: Path, answers: dict, rubric: str):
    path = directory / 'judgment_manifest.json'
    if not path.exists():
        return None
    manifest = json.loads(path.read_text())
    name = manifest['verdict_file']
    if name not in {'judge.json', 'judge_draft.json'}:
        raise ValueError('Unknown verdict file in judgment manifest.')
    checks = {
        'answers_sha256': digest(directory / 'answers.json'),
        'questions_sha256': digest(root / 'eval/questions.csv'),
        'rubric_sha256': hashlib.sha256(rubric.encode()).hexdigest(),
        'verdicts_sha256': digest(directory / name),
    }
    if any(manifest.get(key) != value for key, value in checks.items()):
        raise ValueError('Judge evidence changed; saved verdicts cannot be reused.')
    verdicts = json.loads((directory / name).read_text())
    if set(verdicts) != set(answers):
        raise ValueError('Judge verdict IDs do not match saved answers.')
    for value in verdicts.values():
        if any(type(value.get(key)) is not bool for key in ['correct', 'supported', 'bad_test_question']):
            raise ValueError('Judge grades must be explicit booleans.')
        if not value.get('reasoning', '').strip():
            raise ValueError('Judge verdict is missing its reasoning.')
    return verdicts


def agreement(labels: dict, verdicts: dict) -> dict:
    return {
        'graded_answers': len(labels),
        **{key: sum(row[key] == verdicts[id][key] for id, row in labels.items()) / len(labels)
           for key in ['correct', 'supported']},
        'both': sum(all(row[key] == verdicts[id][key] for key in ['correct', 'supported'])
                    for id, row in labels.items()) / len(labels),
    }


def historical_human_validation(root: Path, current_run: str, expected_run: str) -> dict:
    if not expected_run or expected_run == current_run:
        raise ValueError('Historical human review must name a separate run.')
    binding = (root / 'eval/human_labels_run.txt').read_text().strip()
    if binding != expected_run:
        raise ValueError('Human-label binding differs from configured historical run.')
    directory = root / 'eval/runs' / expected_run
    if not directory.resolve().is_relative_to((root / 'eval/runs').resolve()):
        raise ValueError('Invalid historical run path.')
    original_answers = json.loads((directory / 'answers.json').read_text())
    verdict_path = next((directory / name for name in ['judge.json', 'judge_draft.json']
                         if (directory / name).exists()), None)
    if verdict_path is None:
        raise ValueError('Original human review has no matching original judge records.')
    verdicts = json.loads(verdict_path.read_text())
    labels = {}
    with (root / 'eval/human_labels.csv').open(newline='', encoding='utf-8-sig') as handle:
        for row in csv.DictReader(handle):
            id = row.get('id', '').strip()
            if not id:
                continue
            if id in labels or id not in original_answers or id not in verdicts:
                raise ValueError('Human label ID is duplicated or absent from its original run.')
            if any(row.get(key) not in {'0', '1'} for key in ['correct', 'supported']):
                raise ValueError('Human labels must be 0/1.')
            if '0' in [row['correct'], row['supported']] and not row.get('notes', '').strip():
                raise ValueError('Explain each human zero.')
            labels[id] = {key: row[key] == '1' for key in ['correct', 'supported']}
    if len(labels) < 20:
        raise ValueError('Original human review requires at least 20 saved grades.')
    return {'run_id': expected_run, 'applies_to_current_answers': False,
            'agreement_with_original_judge': agreement(labels, verdicts),
            'labels_sha256': digest(root / 'eval/human_labels.csv'),
            'provenance': json.loads((root / 'eval/human_validation_provenance.json').read_text())}
