from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
from query import ask
import numexpr

load_dotenv()

#Web Search Client
client = TavilyClient()

@tool
def search_notes(query: str):
    """ Search the users personal notes for answers to the question.
    Use this tool to answer questions that the user has already uploaded notes on. """
    
    answer, sources = ask(query)
    return answer

@tool 
def search_web(query: str):
    """ Search the web for current information not available in personal notes.
    Use this for recent events, facts, or anything not in the notes. """
    
    answer = client.search(query, max_results=3)
    return str(answer)

@tool
def calculate(expression: str):
    """Use this function to calculate the answers to any mathematical expressions 
    entered by the user"""
    try:
        result = numexpr.evaluate(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"

tools = [search_notes, search_web, calculate]