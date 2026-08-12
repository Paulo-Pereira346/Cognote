import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

from ingest import ingest_notes, client
from query import ask

st.set_page_config(page_title="Cognote", page_icon="🧠", layout="centered")
st.title("🧠 Cognote")
st.caption("Ask questions about your notes")

with st.sidebar:
    st.header("📂 Your Notes")
    uploaded_files = st.file_uploader(
        "Upload .txt files",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        os.makedirs("data", exist_ok=True)
        for file in uploaded_files:
            if file.name.endswith(".pdf"):
                with open(f"data/{file.name}", "wb") as f:  # binary mode for PDFs
                    f.write(file.read())
            else:
                with open(f"data/{file.name}", "w") as f:  # text mode for txt
                    f.write(file.read().decode("utf-8"))
        st.success(f"{len(uploaded_files)} file(s) uploaded!")

    if st.button("📥 Ingest Notes", use_container_width=True):
        with st.spinner("Chunking and embedding your notes..."):
            ingest_notes()
        st.success("Notes ingested and ready!")

    if st.button("🗑️ Clear Notes", use_container_width=True):
        client.delete_collection("notes")
        st.warning("Notes cleared!")

st.divider()

question = st.text_input("Ask a question:", placeholder="What is supervised learning?")

if question:
    with st.spinner("Searching notes and thinking..."):
        answer, sources = ask(question)

    st.markdown("### 💬 Answer")
    st.write(answer)

    with st.expander("📎 View retrieved chunks"):
        for i, source in enumerate(sources):
            st.markdown(f"**[{i+1}] From `{source['source_file']}`:**")
            st.text(source["text"][:300] + "...")