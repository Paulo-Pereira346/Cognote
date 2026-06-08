from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dot_env import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)

vector_store = Chroma(
    persist_directory = './chroma_db/',
    embedding_function = embeddings,
    collection = 'notes'
)
retriever = vector_store.as_retriever(search_kwargs = {"k" : 3})

llm = ChatGroq(
    model_name = 'llama-3.1-8b-instant'
)

chain = RetrievalQA.from_chain_type(
    llm = llm,
    retriever = retriever,
    return_source_documents = True
)


def ask_langchain(question):
    answer = chain.invoke({"query": question})
    return answer

if __name__ == "__main__":
    answer = ask_langchain("What is Supervised Learning?")
    print(answer["result"])
    print(answer["source_documents"])
    