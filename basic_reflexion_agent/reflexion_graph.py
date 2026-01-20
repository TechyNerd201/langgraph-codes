from typing import List

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph
from langchain_core.messages import AIMessage , BaseMessage , HumanMessage , SystemMessage, ToolMessage
from chains import revisor_chain , first_responder_chain
from tools import execute_tools

MAX_ITERATIONS=3
graph = MessageGraph()

def drapft_node(state):
    result = first_responder_chain.invoke({"messages": state})
    msg = AIMessage(content=result.answer)
    msg.search_queries = result.search_queries
    return msg

def refine_node(state):
    result = revisor_chain.invoke({"messages": state})
    msg = AIMessage(content=result.answer)
    msg.search_queries = result.search_queries
    return msg

graph.add_node("draft", drapft_node)
graph.add_node("search", execute_tools)
graph.add_node("refine", refine_node)

graph.add_edge("draft", "search")
graph.add_edge("search", "refine")

def conditional_function(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)

    num_iterations = count_tool_visits
    if num_iterations > MAX_ITERATIONS:
        return END
    return "search"
    
graph.add_conditional_edges("refine", conditional_function,{
    "search": "search",
    END: END
})

graph.set_entry_point("draft")

app = graph.compile()

print(app.get_graph().draw_mermaid( ))

res =app.invoke("write a article about the best place in the world")
print(res)