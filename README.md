# Cognote 🧠

A RAG-based note Q&A system. Upload your notes (txt/pdf) and ask questions — 
it finds the relevant parts and answers using an LLM.

## Tech Stack
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Vector DB: ChromaDB
- LLM: Groq (configurable with `GROQ_MODEL`, defaulting to `openai/gpt-oss-20b`)
- UI: Streamlit
- Also implemented using LangChain LCEL for comparison

## How it works
1. Notes are chunked and embedded into a vector database
2. Questions are embedded using the same model
3. ChromaDB retrieves the most semantically similar chunks
4. Retrieved chunks are stuffed into a prompt and sent to the LLM
