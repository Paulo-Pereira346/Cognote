from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

chroma_client = chromadb.PersistentClient(path="./chroma_db/")

model = SentenceTransformer('all-MiniLM-L6-v2')

groq_client = Groq()

def ask(question, n=3):
    """This is a function that uses RAG to answer the question"""
    question_embed = model.encode([question]).tolist()
    collection = chroma_client.get_or_create_collection("notes")
    results = collection.query(
        query_embeddings = question_embed,
        n_results = n
    )
    
    source_list = []
        
    for i, doc in enumerate(results["documents"][0]):
        source_dict = {}
        source_dict["source_file"] = results["metadatas"][0][i]["source"]
        source_dict["text"] = doc
        source_list.append(source_dict)
        
    #Building the prompt
    
    context_string = ""
    #Joining the top n chunks together:
    for source in source_list:
        context_string += source["text"]
        context_string += "\n\n---\n\n"
    
    prompt = f"""
    You are a helpful assistant. Answer the question using ONLY 
    the notes provided below. If the answer is not in the notes, 
    say 'I don't have that in my notes.'
    
    NOTES:
    {context_string}
    
    QUESTION: {question}
    
    ANSWER: 
    
    """
    
    response = groq_client.chat.completions.create(
       messages = [
        {
            "role": "user",
            "content": prompt
        }
       ],
       model = "llama-3.1-8b-instant"
    )
    
    answer = response.choices[0].message.content
    
    return answer, source_list

if __name__ == "__main__":
    answer, source = ask("How Many layers does the OSI Model have? Name them")
    print(answer)