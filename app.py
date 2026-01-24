import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    ArxivQueryRun
)
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    ArxivAPIWrapper
)

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ------------------ TOOLS ------------------

# DuckDuckGo
search_tool = DuckDuckGoSearchRun()

# Wikipedia
wiki_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=1500
)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# arXiv
arxiv_wrapper = ArxivAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=2000
)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)

tools = [search_tool, wiki_tool, arxiv_tool]

# ------------------ PROMPT ------------------

template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# ------------------ AGENTS ------------------

# Research Agent (with tools)
research_agent = create_react_agent(llm, tools, prompt)
research_executor = AgentExecutor(
    agent=research_agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# Summary Agent (NO tools)
summary_agent = create_react_agent(llm, [], prompt)
summary_executor = AgentExecutor(
    agent=summary_agent,
    tools=[],
    verbose=True
)

# Email Agent (NO tools)
email_agent = create_react_agent(llm, [], prompt)
email_executor = AgentExecutor(
    agent=email_agent,
    tools=[],
    verbose=True
)

# ------------------ ORCHESTRATOR ------------------

def run_orchestrator(user_input: str):
    research = research_executor.invoke(
        {"input": f"Research the following topic in detail: {user_input}"}
    )["output"]

    summary = summary_executor.invoke(
        {"input": f"Summarize this research in 150–250 words:\n{research}"}
    )["output"]

    email = email_executor.invoke(
        {"input": f"Write a professional email based on this summary:\n{summary}"}
    )["output"]

    return {
        "research": research,
        "summary": summary,
        "email": email
    }
