"""
Retrieval over the saved index, shared by server.py (the search tool) and
evaluate.py (hit rate per design).

Four designs, none of which needs re-embedding the corpus:
    dense          embeddings only (cosine similarity in ChromaDB)
    dense+filter   embeddings, searching only the companies named in the question
    hybrid         embeddings and keyword search (BM25), merged by rank
    hybrid+filter  both of the above

DESIGN is the one the search tool uses. Set it to the winner of `main.py evaluate`.
"""

import re

from rank_bm25 import BM25Okapi

from index import FILINGS, embed_query, get_collection

DESIGN = "dense+filter"    # chosen on hit rate: ties dense, and never mixes up companies
TOP_K = 5                  # chunks the search tool returns

# Ways a question can name each company. Used by the "filter" designs.
COMPANY_NAMES = {
    "ODFL": ["old dominion", "odfl"],
    "JBHT": ["j.b. hunt", "jb hunt", "j. b. hunt", "hunt", "jbht"],
    "SAIA": ["saia"],
    "KNX": ["knight-swift", "knight swift", "knight", "swift", "knx"],
}


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[.,][0-9]+)*", text.lower())


class Retriever:
    """Loads the saved index once and searches it. Never embeds the corpus."""

    def __init__(self):
        self.reload()

    def reload(self):
        """(Re)load every chunk, e.g. after add_document stored new ones."""
        self.collection = get_collection()
        data = self.collection.get(include=["documents", "metadatas"])
        self.ids = data["ids"]
        self.docs = data["documents"]
        self.metas = data["metadatas"]
        # Keyword index over the same text the embeddings saw (title + chunk).
        corpus = [tokens(f"{m['company']} {m['location']} {d}") for d, m in zip(self.docs, self.metas)]
        self.bm25 = BM25Okapi(corpus) if corpus else None

    def companies_in(self, question: str) -> list[str]:
        q = question.lower()
        return [t for t, names in COMPANY_NAMES.items()
                if any(re.search(rf"\b{re.escape(n)}\b", q) for n in names)]

    def dense(self, query_vector, k, tickers=None):
        where = {"ticker": {"$in": tickers}} if tickers else None
        result = self.collection.query(query_embeddings=[query_vector], n_results=k, where=where)
        return result["ids"][0]

    def keyword(self, question, k, tickers=None):
        scores = self.bm25.get_scores(tokens(question))
        order = sorted(range(len(self.ids)), key=lambda i: scores[i], reverse=True)
        if tickers:
            order = [i for i in order if self.metas[i]["ticker"] in tickers]
        return [self.ids[i] for i in order[:k]]

    def search(self, question, k=TOP_K, design=DESIGN, query_vector=None, company=None):
        """Return the top k chunks as dicts with id, text, metadata and rank.

        query_vector lets evaluate.py embed each test question only once.
        company (a ticker) forces the filter, e.g. when the agent passes it.
        """
        if query_vector is None:
            query_vector = embed_query(question)
        tickers = None
        if company:
            tickers = [company.upper()]
        elif design.endswith("+filter"):
            tickers = self.companies_in(question) or None  # no company named: search everything

        if design.startswith("dense"):
            ranked = self.dense(query_vector, k, tickers)
        else:
            # Reciprocal rank fusion: a chunk's score is the sum of 1 / (60 + rank)
            # over both lists, so chunks that rank well in both come first.
            pool = 4 * k
            fused = {}
            for ranking in (self.dense(query_vector, pool, tickers), self.keyword(question, pool, tickers)):
                for rank, chunk_id in enumerate(ranking):
                    fused[chunk_id] = fused.get(chunk_id, 0) + 1 / (60 + rank)
            ranked = sorted(fused, key=fused.get, reverse=True)[:k]

        position = {chunk_id: i for i, chunk_id in enumerate(self.ids)}
        return [{"id": cid, "text": self.docs[position[cid]], "metadata": self.metas[position[cid]], "rank": r + 1}
                for r, cid in enumerate(ranked)]


def citation(chunk: dict) -> str:
    """How a chunk is cited, e.g. [SAIA 10-K 2025, Item 7 > Outlook]."""
    return f"[{chunk['metadata']['source']}, {chunk['metadata']['location']}]"


def format_results(chunks: list[dict]) -> str:
    if not chunks:
        return "No passages found."
    return "\n\n".join(f"{citation(c)}\n{c['text']}" for c in chunks)


KNOWN_TICKERS = sorted({f[0] for f in FILINGS})
