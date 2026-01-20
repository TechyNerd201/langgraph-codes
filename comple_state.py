from typing  import TypedDict , List , Annotated
from langgraph.graph import END , StateGraph
import operator

class SimpleState(TypedDict):
    count: str
    sum: Annotated[int , operator.add]
    history: Annotated[List[int] , operator.concat ]


def increment(state : SimpleState) -> SimpleState:
    new_count = state["count"] + 1
    return {
        "count" : new_count,
        "sum" : new_count,
        "history" : [new_count]
    }

def should_continue(state : SimpleState) -> str:
    if( state['count'] < 5):
        return "continue"
    return "END"

graph = StateGraph(SimpleState)
graph.add_node("increment",increment)

graph.add_conditional_edges("increment",should_continue,{
    "continue" : "increment",
    "END" : END
})

graph.set_entry_point("increment")

demo = graph.compile()
res= demo.invoke({
    "count": 0
})
print(res)

