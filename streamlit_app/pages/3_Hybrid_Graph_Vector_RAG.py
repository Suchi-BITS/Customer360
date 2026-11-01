import contextlib
import io
import streamlit as st
from app.retrieval.hybrid_rag import run_hybrid_rag

st.set_page_config(page_title="Hybrid Graph + Vector RAG", layout="wide")
st.title("Hybrid Graph + Vector RAG")
st.write("Retrieve relevant passages from the sample text documents using embeddings, retrieve connected customer facts from Neptune, and ask Bedrock to answer using both evidence sources.")

customer_id = st.text_input("Customer ID", value="C1001")
question = st.text_area(
    "Your question",
    value="Summarize the customer's contract and support context. Distinguish document evidence from graph facts.",
    height=110,
)
st.caption("This page uses the Titan Text Embeddings model configured in .env. Model access must be enabled for your AWS account.")
if st.button("Run Hybrid Graph + Vector RAG", type="primary"):
    if not customer_id.strip() or not question.strip():
        st.warning("Enter both a customer ID and a question.")
    else:
        output = io.StringIO()
        try:
            with st.spinner("Retrieving document passages and graph facts..."):
                with contextlib.redirect_stdout(output):
                    run_hybrid_rag(customer_id.strip(), question.strip())
            st.success("Hybrid retrieval completed.")
            st.text(output.getvalue())
        except Exception as exc:
            st.error(f"The request failed: {exc}")
            captured = output.getvalue()
            if captured:
                st.code(captured)
