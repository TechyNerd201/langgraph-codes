from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.agents import create_agent  # New import
from langchain_core.messages import HumanMessage  # For input format

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
search_tool = TavilySearch(search_depth="basic")
tools = [search_tool]

# Define system prompt for ReAct behavior (equivalent to ZERO_SHOT_REACT_DESCRIPTION)
#
system_prompt = """You are a ReAct agent.
Respond with: Thought: [reason] Action: [tool] {"query": "..."} 
or Final Answer: [response]"""

agent = create_agent(
    llm,                   # Your model
    tools,                 # Your tools
    system_prompt=system_prompt,
    # verbose=True          # Add if needed (uses LangSmith tracing)
)

res = agent.invoke({
    "messages": [HumanMessage(content="what is the weather of nagpur")]  # New input format
})
print(res)