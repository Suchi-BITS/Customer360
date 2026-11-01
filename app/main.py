import argparse
from app.retrieval.kg_rag import run_kg_rag
from app.retrieval.graph_rag import run_graph_rag
from app.retrieval.hybrid_rag import run_hybrid_rag

def main():
    parser = argparse.ArgumentParser(description="Customer 360 RAG pattern demonstrations")
    sub = parser.add_subparsers(dest="mode", required=True)
    kg = sub.add_parser("kg", help="Natural language -> SPARQL -> Neptune")
    kg.add_argument("--question", required=True)
    graph = sub.add_parser("graph", help="Traverse connected customer graph facts")
    graph.add_argument("--customer-id", required=True)
    hybrid = sub.add_parser("hybrid", help="Combine vector documents and graph facts")
    hybrid.add_argument("--customer-id", required=True)
    hybrid.add_argument("--question", required=True)
    args = parser.parse_args()
    if args.mode == "kg":
        run_kg_rag(args.question)
    elif args.mode == "graph":
        run_graph_rag(args.customer_id)
    else:
        run_hybrid_rag(args.customer_id, args.question)

if __name__ == "__main__":
    main()
