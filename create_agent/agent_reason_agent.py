# here we are just creating the react agent , it will jsut  give input to llm , llm will give output , with all the tools it has to call -> END

from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
import datetime
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain import hub
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Return the current date and time in the specified format."""
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = TavilySearch(search_depth="basic")

tools =[get_system_time, search_tool]

react_prompt = hub.pull("hwchase17/react")

react_agent_runnable = create_react_agent(tools=tools, llm=llm, prompt=react_prompt)

