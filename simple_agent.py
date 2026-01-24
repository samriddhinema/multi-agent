import requests
import os
from langchain_community.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic import hub
from langchain_google_genai import ChatGoogleGenerativeAI
import numexpr  # For calculator tool
from dotenv import load_dotenv
load_dotenv()
print(numexpr.evaluate(10+5))
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')
prompt = hub.pull('hwchase17/react')

#1st tool -search tool
search_tool = DuckDuckGoSearchRun()

#2n tool - weather api tool
@tool
def get_weather_data(city:str) -> dict:
    """
    Fetch current weather data.
    Returns temperature as a number.
    """
    data = requests.get("http://api.weatherstack.com/current",params={'access_key': os.getenv("WEATHERSTACK_API_KEY"), "query": city}, 
                                                                      timeout=10).json()
    
    if 'current' not in data:
        raise RuntimeError(data)
    else:
        return{
            'city': city,
            "temperature": data["current"]["temperature"],
            "condition": data["current"]["weather_descriptions"][0]}

# 3rd tool- calculator
@tool
def calculator(expression: str) -> float:
    """Evaluate a math expression safely."""
    return float(numexpr.evaluate(expression))

#step-3 Create the react agent manually with the pulled prompt

agent = create_react_agent(
    llm=llm,
    tools=[search_tool, get_weather_data, calculator],
    prompt=prompt
)

#step-4 Wrap it with AgentExecutor

agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, get_weather_data, calculator],
    verbose=True
)
# Step-5 invoke
response = agent_executor.invoke({"input": "find the capital of India, then find it's current weather condition and then subtract 5 from it"})
#print(response) 
