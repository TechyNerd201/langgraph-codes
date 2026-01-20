from typing import List,TypedDict
from langgraph.graph import StateGraph , END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

class SimpleState(TypedDict):
    count : int

def increment( state :SimpleState) -> SimpleState:
    return {
        "count" : state["count"] + 1
    }

def should_continue(state : SimpleState) -> str:
    if state["count"] > 3:
        return "end"
    else:
        return "continue"

graph = StateGraph(SimpleState)

graph.add_node("increment",increment)
graph.set_entry_point("increment")
graph.add_conditional_edges("increment",should_continue , {
    "continue" : "increment",
    "end" : END
})



demo = graph.compile()

res = demo.invoke({
    "count" : 0
})
print(res)


