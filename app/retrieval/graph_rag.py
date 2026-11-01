import json
from app.aws_clients import execute_sparql, converse
from app.config import C360
from app.prompts import ANSWER_SYSTEM_PROMPT

def build_graph_query(customer_id: str) -> str:
    safe_id = customer_id.replace('"', '')
    return f"""PREFIX c360: <{C360}>
SELECT ?customerPredicate ?customerValue ?relationship ?relatedEntity ?relatedPredicate ?relatedValue
WHERE {{
  ?customer a c360:Customer ; c360:customerId "{safe_id}" .
  {{
    ?customer ?customerPredicate ?customerValue .
    FILTER(isLiteral(?customerValue))
    BIND("customer_direct_fact" AS ?relationship)
    BIND(?customer AS ?relatedEntity)
    BIND(?customerPredicate AS ?relatedPredicate)
    BIND(?customerValue AS ?relatedValue)
  }}
  UNION
  {{
    ?customer ?relationship ?relatedEntity .
    FILTER(?relationship IN (c360:hasParty, c360:hasAccount, c360:placesOrder,
      c360:hasInvoice, c360:hasContract, c360:hasSubscription,
      c360:hasSupportCase, c360:hasInteraction))
    ?relatedEntity ?relatedPredicate ?relatedValue .
    FILTER(isLiteral(?relatedValue))
  }}
}}
LIMIT 150
"""

def run_graph_rag(customer_id: str) -> None:
    print("\n========== GRAPHRAG: ENTITY + RELATIONSHIP TRAVERSAL ==========")
    rows = execute_sparql(build_graph_query(customer_id)).get("results", {}).get("bindings", [])
    print(f"Retrieved {len(rows)} graph evidence rows for {customer_id}.")
    print(json.dumps(rows, indent=2))
    answer = converse(ANSWER_SYSTEM_PROMPT,
        f"Summarize this customer's retrieved graph context. Do not infer absent facts. "
        f"Customer ID: {customer_id}. Evidence: {json.dumps(rows)}")
    print("\n--- Bedrock graph-grounded answer ---\n" + answer)
