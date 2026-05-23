import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()  #Load Environmental Variables

#Load Model 
model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path='./chroma_db/')

def load_notes(folder="data"):
    file_list = []
   
    for file in os.listdir(folder):
        data_dict = {}
        root, ext = os.path.splitext(file)
        if(ext == '.txt'):
            with open(f"{folder}/{file}",'r') as f:
                content = f.read()
                print("File:",file)
                print("Character Count:",len(content))
            data_dict["filename"] = file
            data_dict["text"] = content
            file_list.append(data_dict)
        
    return file_list

def chunk_text(text, chunk_size=500, overlap=50):
    chunk_list = []
    words = text.split()
    start = 0
    
    while(start < len(words)):
        chunk = " ".join(words[start : start + chunk_size])
        chunk_list.append(chunk)
        
        start = start + chunk_size - overlap
    
    return chunk_list

def embed_chunks(chunk_list):
    embeddings = model.encode(chunk_list)
    print(embeddings.shape)
    
    return embeddings

def ingest_notes():
    collection = client.get_or_create_collection("notes")
    notes = load_notes()
    for doc in notes:
        chunks = chunk_text(doc["text"])
        chunk_embeddings = embed_chunks(chunks)
        chunk_id_list = []
        for i in range(0, len(chunks)):
            chunk_id_list.append(f"{doc['filename']}_chunk_{i}")
    
        collection.add(ids = chunk_id_list, 
                       documents = chunks, 
                       embeddings = chunk_embeddings.tolist(),
                       metadatas = [{"source": doc["filename"]} for _ in chunks])
        print(f"Stored {len(chunks)} chunks from {doc['filename']}")
            
def test_retrieval():
    collection = client.get_or_create_collection("notes")
    query_emb = model.encode(["What is supervised learning?"]).tolist()
    results = collection.query(
        query_embeddings = query_emb,
        n_results = 3
    )
    
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        print(f"\nResult {i+1} from {source}:\n{doc[:200]}")
            

if __name__ == "__main__":
    ingest_notes()
    test_retrieval()