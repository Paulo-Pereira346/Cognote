from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)

vector_store = Chroma(
    persist_directory = './chroma_db/',
    embedding_function = embeddings,
    collection_name = 'notes'
)

retriever = vector_store.as_retriever(search_kwargs = {"k" : 3})

llm = ChatGroq(
    model_name = os.environ['GROQ_MODEL']
)

prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.
If the answer isn't there, say "I don't have that in my notes."

Context: {context}
Question: {input}
""")

def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


def ask_langchain(question):
    answer = chain.invoke(question)
    return answer

if __name__ == "__main__":
    answer = ask_langchain("What is Supervised Learning? What are the two types?")
    print(answer)

    