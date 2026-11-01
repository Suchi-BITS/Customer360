import contextlib
import io
import streamlit as st
from app.retrieval.kg_rag import run_kg_rag

st.set_page_config(page_title="Knowledge Graph RAG", layout="wide")
st.title("Knowledge Graph RAG")
st.write("Ask a natural-language question. Bedrock generates a read-oriented SPARQL query, Neptune executes it, and Bedrock formulates an answer from the returned evidence.")

question = st.text_area(
    "Your question",
    value="Show the customer IDs and the names of their associated people or organizations.",
    height=100,
)
if st.button("Run Knowledge Graph RAG", type="primary"):
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        output = io.StringIO()
        try:
            with st.spinner("Generating SPARQL and querying Neptune..."):
                with contextlib.redirect_stdout(output):
                    run_kg_rag(question.strip())
            st.success("Knowledge Graph RAG completed.")
            st.text(output.getvalue())
        except Exception as exc:
            st.error(f"The request failed: {exc}")
            captured = output.getvalue()
            if captured:
                st.code(captured)
