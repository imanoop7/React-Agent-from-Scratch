from tavily import TavilyClient
import os
import wikipedia
from duckduckgo_search import DDGS

class Tool:
    def __init__(self, func):
        self.func = func

    def run(self, query):
        return self.func(query)

# def tavily_search(query: str) -> str:
#     tavily_api_key = os.getenv("TAVILY_API_KEY")
#     if not tavily_api_key:
#         return "Error: Tavily API key not found. Please set the TAVILY_API_KEY environment variable."
    
#     tavily_client = TavilyClient(api_key=tavily_api_key)
#     search_result = tavily_client.search(query)
    
#     formatted_result = "Search Results:\n"
#     for i, result in enumerate(search_result['results'][:3], 1):
#         formatted_result += f"{i}. {result['title']}\n   {result['url']}\n   {result['content'][:200]}...\n\n"
    
#     return formatted_result

def duckduckgo_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        
        formatted_result = "Search Results:\n"
        for i, result in enumerate(results, 1):
            formatted_result += f"{i}. {result['title']}\n   {result['href']}\n   {result['body'][:200]}...\n\n"
        
        return formatted_result
    except Exception as e:
        return f"An error occurred while searching DuckDuckGo: {str(e)}"

def wikipedia_search(query: str) -> str:
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return f"No Wikipedia results found for '{query}'."
        
        page = wikipedia.page(search_results[0])
        summary = wikipedia.summary(search_results[0], sentences=3)
        
        return f"Wikipedia: {page.title}\n\nSummary: {summary}\n\nURL: {page.url}"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found for '{query}'. Please be more specific. Options include: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"An error occurred while searching Wikipedia: {str(e)}"
