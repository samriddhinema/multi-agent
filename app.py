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


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ------------------ TOOLS ------------------

search_tool = DuckDuckGoSearchRun()

wiki_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=1500
)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

arxiv_wrapper = ArxivAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=2000
)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)

tools = [search_tool, wiki_tool, arxiv_tool]

# ------------------ REACT PROMPT (ONLY FOR RESEARCH) ------------------

template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

# ------------------ RESEARCH AGENT ------------------

research_agent = create_react_agent(llm, tools, prompt)

research_executor = AgentExecutor(
    agent=research_agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ------------------ ORCHESTRATOR ------------------

def run_orchestrator(user_input: str):
   
    research = research_executor.invoke(
        {"input": f"Research the following topic in detail: {user_input}"}
    )["output"]

   
    summary_prompt = (
        "Summarize the following research in 150–250 words:\n\n"
        f"{research}"
    )
    summary = llm.invoke(summary_prompt).content

 
    email_prompt = (
        "Write a professional email based on this summary:\n\n"
        f"{summary}"
    )
    email = llm.invoke(email_prompt).content

    return {
        "research": research,
        "summary": summary,
        "email": email
    }

