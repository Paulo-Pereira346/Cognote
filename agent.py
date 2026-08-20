from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools import tools
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model_name=os.environ["GROQ_MODEL"]
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful assistant for the user's personal notes. "
        "Use search_notes for questions that may be answered by the notes, "
        "search_web for current information, and calculate for mathematics."
    )
)

def ask_agent(question):
    response = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return response["messages"][-1].content

if __name__ == "__main__":
    answer = ask_agent(
        "How many layers does the OSI model have multiplied by 5? Also name the OSI layers."
    )
    print(answer)