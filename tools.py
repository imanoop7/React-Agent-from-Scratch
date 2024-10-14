import os
import wikipedia
import requests
from bs4 import BeautifulSoup

class Tool:
    def __init__(self, func):
        self.func = func

    def run(self, query):
        return self.func(query)

def duckduckgo_search(query: str) -> str:
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='result__body')
        
        formatted_result = "Search Results:\n"
        for i, result in enumerate(results[:3], 1):
            title = result.find('a', class_='result__a').text
            link = result.find('a', class_='result__a')['href']
            snippet = result.find('a', class_='result__snippet').text
            formatted_result += f"{i}. {title}\n   {link}\n   {snippet[:200]}...\n\n"
        
        return formatted_result
    except Exception as e:
        return f"An error occurred while searching: {str(e)}"

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
