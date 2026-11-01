import streamlit as st

st.set_page_config(page_title="Customer 360 RAG Demo", page_icon="🔎", layout="wide")

st.title("Customer 360 — Enterprise RAG Demonstration")
st.write(
    "Explore three retrieval patterns over the Customer 360 knowledge graph "
    "and the supporting sample documents."
)

st.subheader("Demonstration modules")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 1. Knowledge Graph RAG")
    st.write("Natural-language question → Bedrock-generated SPARQL → Neptune → grounded answer.")
with col2:
    st.markdown("### 2. GraphRAG")
    st.write("Start with a customer and traverse connected entities and relationships in Neptune.")
with col3:
    st.markdown("### 3. Hybrid Graph + Vector RAG")
    st.write("Retrieve relevant document passages and graph facts, then combine the evidence.")

st.info("Choose a page from the navigation sidebar to run a demonstration.")
st.caption("This is a learning/demo application. It is not a production customer-data system.")
