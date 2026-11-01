import re
from app.aws_clients import converse, execute_sparql
from app.prompts import KG_SYSTEM_PROMPT, ANSWER_SYSTEM_PROMPT, SCHEMA_CONTEXT

FORBIDDEN = re.compile(r"\\b(INSERT|DELETE|LOAD|CLEAR|DROP|CREATE|COPY|MOVE|ADD|SERVICE)\\b", re.I)

def clean_query(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:sparql)?\\s*", "", text, flags=re.I)
    return re.sub(r"\\s*```$", "", text).strip()

def run_kg_rag(question: str) -> None:
    print("\\n========== KNOWLEDGE GRAPH RAG ==========")
    generated = converse(KG_SYSTEM_PROMPT, f"Schema:\\n{SCHEMA_CONTEXT}\\nQuestion: {question}", 700)
    query = clean_query(generated)
    if not re.search(r"\\bSELECT\\b", query, re.I) or FORBIDDEN.search(query):
        raise ValueError(f"Generated query rejected. Inspect model output:\\n{query}")
    if not re.search(r"\\bLIMIT\\s+([1-9]\\d?)\\b", query, re.I):
        query += "\\nLIMIT 50"
    print("\\n--- Generated SPARQL ---\\n" + query)
    rows = execute_sparql(query).get("results", {}).get("bindings", [])
    print("\\n--- Neptune result bindings ---")
    print(rows)
    answer = converse(ANSWER_SYSTEM_PROMPT, f"Question: {question}\\nNeptune evidence: {rows}")
    print("\\n--- Grounded answer ---\\n" + answer)
