import contextlib
import io
import streamlit as st
from app.retrieval.graph_rag import run_graph_rag

st.set_page_config(page_title="GraphRAG", layout="wide")
st.title("GraphRAG — Customer Relationship Exploration")
st.write("Retrieve a customer and traverse its connected entities and literal facts in Neptune. Bedrock then summarizes the retrieved graph evidence.")

customer_id = st.text_input("Customer ID", value="C1001")
if st.button("Explore Customer Graph", type="primary"):
    if not customer_id.strip():
        st.warning("Enter a customer ID.")
    else:
        output = io.StringIO()
        try:
            with st.spinner("Traversing the customer graph..."):
                with contextlib.redirect_stdout(output):
                    run_graph_rag(customer_id.strip())
            st.success("GraphRAG completed.")
            st.text(output.getvalue())
        except Exception as exc:
            st.error(f"The request failed: {exc}")
            captured = output.getvalue()
            if captured:
                st.code(captured)
