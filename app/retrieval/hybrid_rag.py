import json
from pathlib import Path
import numpy as np
from app.aws_clients import embed_text, execute_sparql, converse
from app.retrieval.graph_rag import build_graph_query
from app.prompts import ANSWER_SYSTEM_PROMPT

DOCS_DIR = Path(__file__).resolve().parents[2] / "data" / "documents"

def load_chunks():
    chunks = []
    for path in sorted(DOCS_DIR.glob("*.txt")):
        paragraphs = [p.strip() for p in path.read_text(encoding="utf-8").split("\\n\\n") if p.strip()]
        for idx, paragraph in enumerate(paragraphs, start=1):
            chunks.append({"source": path.name, "chunk_id": idx, "text": paragraph})
    return chunks

def cosine(a, b):
    av, bv = np.asarray(a, dtype=np.float32), np.asarray(b, dtype=np.float32)
    denominator = float(np.linalg.norm(av) * np.linalg.norm(bv))
    return float(np.dot(av, bv) / denominator) if denominator else 0.0

def retrieve_chunks(question: str, top_k: int = 3):
    chunks = load_chunks()
    if not chunks:
        return []
    query_vector = embed_text(question)
    for chunk in chunks:
        chunk["score"] = cosine(query_vector, embed_text(chunk["text"]))
    return sorted(chunks, key=lambda item: item["score"], reverse=True)[:top_k]

def run_hybrid_rag(customer_id: str, question: str) -> None:
    print("\\n========== HYBRID GRAPH + VECTOR RAG ==========")
    docs = retrieve_chunks(question)
    print("\\n--- Vector-retrieved document passages ---")
    print(json.dumps(docs, indent=2))
    graph_rows = execute_sparql(build_graph_query(customer_id)).get("results", {}).get("bindings", [])
    print(f"\\nNeptune graph facts retrieved: {len(graph_rows)}")
    evidence = {"document_chunks": docs, "neptune_graph_facts": graph_rows}
    answer = converse(ANSWER_SYSTEM_PROMPT,
        f"Answer by combining document passages and graph facts. Distinguish the source "
        f"of each claim. If unsupported, say so.\\nQuestion: {question}\\nEvidence: "
        f"{json.dumps(evidence)}", 1100)
    print("\\n--- Hybrid grounded answer ---\\n" + answer)
