import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm

load_dotenv()  #Load Environmental Variables

#Load Model 
model = SentenceTransformer('all-MiniLM-L6-v2')



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
            

if __name__ == "__main__":
    notes = load_notes()
    chunks = chunk_text(notes[0]["text"])
    print(f"Number of chunks: {len(chunks)}")
    embeddings = embed_chunks(chunks)
    