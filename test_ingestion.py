import tempfile
import unittest
from pathlib import Path

from ingestion import VectorStore, chunks


class IngestionTests(unittest.TestCase):
    def test_chunk_boundaries_and_overlap(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "a.txt"
            p.write_text("one two three four five six seven")
            c = chunks(p, "doc", 4, 1)
            self.assertEqual(
                [x["text"] for x in c], ["one two three four", "four five six seven"]
            )
            self.assertEqual(c[1]["location"], "text; words 4-7")
            self.assertEqual(c, chunks(p, "doc", 4, 1))

    def test_resume_and_atomic_design_replacement(self):
        with tempfile.TemporaryDirectory() as t:
            s = VectorStore(Path(t) / "v.db")
            c = [{"id": "1", "source": "d", "location": "p1", "text": "alpha"}]
            self.assertEqual(s.add("a", c, "m", lambda t: [1, 0]), 1)
            self.assertEqual(
                s.add("b", c, "m", lambda t: self.fail("must reuse vectors")), 0
            )
            with self.assertRaises(RuntimeError):
                s.add(
                    "a",
                    c + [dict(c[0], id="2", text="beta")],
                    "m",
                    lambda t: (_ for _ in ()).throw(RuntimeError("quota")),
                )
            self.assertEqual(s.search("a", "m", [1, 0])[0]["id"], "1")
            self.assertEqual(
                s.db.execute('SELECT count(*) FROM chunks WHERE design="a"').fetchone()[
                    0
                ],
                1,
            )

    def test_model_and_dimension_separation(self):
        with tempfile.TemporaryDirectory() as t:
            s = VectorStore(Path(t) / "v.db")
            c = [{"id": "1", "source": "d", "location": "p1", "text": "alpha"}]
            s.add("a", c, "m", lambda t: [1, 0])
            self.assertEqual(s.search("a", "different", [1, 0]), [])
            with self.assertRaises(ValueError):
                s.search("a", "m", [1, 0, 0])

    def test_invalid_chunk_configuration(self):
        with self.assertRaises(ValueError):
            chunks("unused", "d", 4, 4)


if __name__ == "__main__":
    unittest.main()
