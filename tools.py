import logging
from livekit.agents import function_tool,RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
tools=DuckDuckGoSearchRun()
print(tools.run("geminiai latest news"))

@function_tool
async def get_weather(location:str)->str:
    """Get the current weather for a given location using wttr.in API."""
    try:
        response = requests.get(f"https://wttr.in/{location}?format=3")
        if response.status_code == 200:
            return response.text
        else:
            return f"Could not retrieve weather data for {location}."
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return "An error occurred while fetching the weather data."


@function_tool
async def search_web(
        query: str, run_context: RunContext
) -> str:
    """Search the web using DuckDuckGoSearch and return the top result."""
    try:
        search_tool = DuckDuckGoSearchRun()
        results = await run_context.run_in_threadpool(search_tool.arun, query)
        if results:
            return results[0]['snippet']
        else:
            return "No results found."
    except Exception as e:
        logging.error(f"Error performing web search: {e}")
        return "An error occurred while performing the web search."
        
    
               
               