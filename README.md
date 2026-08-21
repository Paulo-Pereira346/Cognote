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

## Agentic Mode

Cognote also includes a LangChain agent in `agent.py`. Instead of always
running the same RAG flow, the agent can decide which tool is appropriate for
each question:

- `search_notes` uses the RAG pipeline to search the user's uploaded notes
- `search_web` retrieves current information from the web using Tavily
- `calculate` evaluates mathematical expressions

The agent can call a tool, inspect its result, and then either call another
tool or produce a final answer. This makes it useful for multi-step questions,
such as combining information from personal notes with current web results.

The difference between the two modes is:

- **RAG mode:** retrieves note chunks and sends them to the LLM in a fixed
	pipeline
- **Agentic mode:** lets the LLM choose and sequence tools before generating
	the final response

Agentic mode is more flexible, but it may also make more model and tool calls,
which can increase response time and usage. The Streamlit app currently uses
agentic mode by calling `ask_agent` from `agent.py`.
