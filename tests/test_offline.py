"""Offline regression tests, no Gemini key/network and no fake embeddings."""
import json
import sqlite3
import tempfile
from unittest.mock import patch
import unittest
from pathlib import Path

from agent import extract_citations, validate_answer, is_refusal, CANONICAL_REFUSAL
from evaluation_core import questions, match_all, prepare_experiment
from rag_core import ROOT, SOURCES_DIR, chunk_file, get_conn, manifest_map, retrieve, store_chunks, index_summary, add_document_pipeline, _embed_document_batch, EMBED_DIMS, available_vectors, EMBED_MODEL


class CorpusTests(unittest.TestCase):
    def test_public_document_coverage(self):
        manifest = manifest_map()
        self.assertGreaterEqual(len(manifest), 3)
        self.assertGreaterEqual(sum(doc['words'] for doc in manifest.values()), 50000)
        self.assertTrue(all(doc['url'].startswith('https://docs.python.org/3.13/') for doc in manifest.values()))

    def test_stable_source_and_topic_citations(self):
        first = chunk_file(SOURCES_DIR / 'simple_statements.md')
        again = chunk_file(SOURCES_DIR / 'simple_statements.md')
        self.assertEqual([c['id'] for c in first], [c['id'] for c in again])
        self.assertTrue(all(c['source']=='simple_statements' for c in first))
        self.assertTrue(all(c['location'].startswith('topic:') for c in first))
        self.assertTrue(all(c['url'].startswith('https://') for c in first))
        self.assertTrue(all(c['filepath']=='source_docs/simple_statements.md' for c in first))

    def test_incremental_ingestion_reuses_existing_vectors(self):
        chunks = chunk_file(SOURCES_DIR/'lexical_analysis.md')
        with tempfile.TemporaryDirectory() as directory:
            conn = get_conn(Path(directory)/'test.sqlite3')
            first = store_chunks(chunks, conn=conn, replace_file=True)
            self.assertFalse(first['skipped'])
            # A stand-in marker is used only in a temp DB to test persistence.
            conn.execute('UPDATE chunks SET vector=? WHERE id=?', (b'EXISTING', chunks[0]['id']))
            conn.commit()
            again = store_chunks(chunks, conn=conn, replace_file=True)
            self.assertTrue(again['skipped'])
            self.assertEqual(conn.execute('SELECT vector FROM chunks WHERE id=?', (chunks[0]['id'],)).fetchone()[0], b'EXISTING')
            conn.close()

    def test_saved_local_index_and_diversity(self):
        info=index_summary()
        self.assertGreaterEqual(info['chunks'], 100)
        hits=retrieve('How does nonlocal affect an enclosing scope?',k=5,design='section_bm25')
        self.assertTrue(hits)
        self.assertEqual(len({(h['source'], h['location']) for h in hits}), len(hits))

    def test_add_document_rejects_outside_incoming(self):
        with self.assertRaisesRegex(ValueError, 'Only regular files'):
            add_document_pipeline(ROOT / 'README.md')

    def test_gemini_batch_maps_one_embedding_per_content(self):
        # Mock ONLY the external SDK transport; this is not a claim of live API use.
        import sys
        from types import ModuleType, SimpleNamespace
        from unittest.mock import patch
        genai = ModuleType('google.genai')
        genai.types = SimpleNamespace(
            Part=SimpleNamespace(from_text=lambda text: {'text':text}),
            Content=lambda parts: {'parts':parts},
            EmbedContentConfig=lambda output_dimensionality: {'dims':output_dimensionality},
        )
        google = ModuleType('google')
        google.genai = genai
        class FakeModel:
            def embed_content(self, **kwargs):
                self.contents = kwargs['contents']
                self.assert_dim = kwargs['config']['dims']
                return SimpleNamespace(embeddings=[SimpleNamespace(values=[float(i)] * EMBED_DIMS)
                                                   for i in range(len(self.contents))])
        m=FakeModel()
        with patch.dict(sys.modules, {'google':google,'google.genai':genai}):
            results = _embed_document_batch(SimpleNamespace(models=m), ['first', 'second'])
        self.assertEqual(len(m.contents), 2)
        self.assertEqual(m.assert_dim, EMBED_DIMS)
        self.assertEqual(results[0][0],0.0)
        self.assertEqual(results[1][0],1.0)

    def test_multipassage_hit_requires_both(self):
        q={'expected_source':'data_model;builtin_types',
           'expected_location':'topic:specialnames;topic:typesmapping'}
        a={'source':'data_model','location':'topic:specialnames'}
        b={'source':'builtin_types','location':'topic:typesmapping'}
        self.assertFalse(match_all(q,[a]))
        self.assertTrue(match_all(q,[a,b]))

    def test_question_kinds(self):
        qs=questions()
        self.assertGreaterEqual(len(qs),30)
        self.assertGreaterEqual(sum(q['kind']=='multi' for q in qs),5)
        self.assertGreaterEqual(sum(q['kind']=='unanswerable' for q in qs),5)
        self.assertTrue(all(not q['expected_source'] for q in qs if q['kind']=='unanswerable'))


class GuardrailTests(unittest.TestCase):
    def test_invalid_citation_refused(self):
        answer, event=validate_answer('Answer [CITE:00000000000000000000]', {'11111111111111111111'})
        self.assertEqual(event['guardrail_fired'], 'invalid_citations')
        self.assertTrue(is_refusal(answer))

    def test_missing_citation_refused(self):
        answer, event=validate_answer('Answer without any reference.', set())
        self.assertEqual(event['guardrail_fired'], 'missing_citations')
        self.assertTrue(is_refusal(answer))

    def test_valid_citation_is_accepted(self):
        cite='abcdefabcdefabcdefab'
        answer,event=validate_answer(f'Claim [CITE:{cite}]', {cite})
        self.assertIsNone(event['guardrail_fired'])
        self.assertEqual(extract_citations(answer), [cite])

    def test_only_notebook_stage_entrypoints(self):
        self.assertTrue((ROOT/'index.ipynb').exists())
        self.assertTrue((ROOT/'evaluate.ipynb').exists())
        self.assertFalse((ROOT/'index.py').exists())
        self.assertFalse((ROOT/'evaluate.py').exists())


class FixRegressionTests(unittest.TestCase):
    def test_mixed_refusal_cannot_hide_uncited_claim(self):
        answer, info = validate_answer("I don't know. The value is definitely 42.", set())
        self.assertEqual(info['guardrail_fired'], 'missing_citations')
        self.assertEqual(answer, CANONICAL_REFUSAL)
        clean, info = validate_answer(CANONICAL_REFUSAL, set())
        self.assertIsNone(info['guardrail_fired'])
        self.assertEqual(clean, CANONICAL_REFUSAL)

    def test_malformed_citation_cannot_sneak_in_with_valid_one(self):
        good = 'abcdefabcdefabcdefab'
        answer, info = validate_answer(f'Claim [CITE:{good}] plus [CITE:FAKE]', {good})
        self.assertEqual(info['guardrail_fired'], 'invalid_citations')
        self.assertTrue(is_refusal(answer))

    def test_source_location_must_be_correct_pair(self):
        row = {'id': 'cross', 'expected_source': 'alpha;beta',
               'expected_location': 'topic:first;topic:second'}
        swapped = [{'source': 'alpha', 'location': 'topic:second'},
                   {'source': 'beta', 'location': 'topic:first'}]
        self.assertFalse(match_all(row, swapped))
        self.assertTrue(match_all(row, [{'source': 'alpha', 'location': 'topic:first'},
                                        {'source': 'beta', 'location': 'topic:second'}]))

    def test_outdated_or_invalid_vector_is_pending(self):
        chunks = chunk_file(SOURCES_DIR / 'lexical_analysis.md')
        with tempfile.TemporaryDirectory() as td:
            conn = get_conn(Path(td) / 'test.sqlite3')
            store_chunks(chunks, conn=conn, replace_file=True)
            conn.execute("UPDATE chunks SET vector=?, embedding_model=? WHERE id=?",
                         (b'BAD', 'older-model', chunks[0]['id']))
            conn.commit()
            self.assertEqual(available_vectors(conn)[1], 0)
            again = store_chunks(chunks, conn=conn, replace_file=True)
            self.assertEqual(again['pending'], len(chunks))
            conn.close()

    def test_empty_replacement_does_not_leave_unnoticed_stale_data(self):
        from rag_core import get_conn as real_get_conn
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / 'test.sqlite3'
            doc = ROOT / 'incoming' / 'temporary_test_addition.md'
            doc.write_text('### TOPIC: example\nThis sentence has enough words to become a chunk of indexed text.\n',
                           encoding='utf-8')
            try:
                with patch('rag_core.get_conn', side_effect=lambda: real_get_conn(db_path)), \
                     patch('rag_core.embed_and_store', return_value={'embedded': 0}):
                    added = add_document_pipeline(doc)
                    self.assertFalse(added['skipped'])
                    duplicate = add_document_pipeline(doc)
                    self.assertTrue(duplicate['skipped'])
                    doc.write_text('', encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'no indexable'):
                        add_document_pipeline(doc)
                    conn = real_get_conn(db_path)
                    self.assertEqual(conn.execute('SELECT COUNT(*) FROM chunks').fetchone()[0], 1)
                    conn.close()
            finally:
                doc.unlink(missing_ok=True)

    def test_checkpoint_signature_change_is_detected(self):
        import evaluation_core as ev
        with tempfile.TemporaryDirectory() as td:
            with patch.object(ev, 'EVAL_DIR', Path(td)):
                ev.prepare_experiment(questions(), overwrite=True)
                (Path(td) / 'answers.jsonl').write_text('{}\n', encoding='utf-8')
                with patch.object(ev, 'experiment_signature', return_value='changed'):
                    with self.assertRaisesRegex(RuntimeError, 'changed'):
                        ev.prepare_experiment(questions(), overwrite=False)


if __name__=='__main__':
    unittest.main()
