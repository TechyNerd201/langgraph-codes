from typing import List , Sequence
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.graph import END , MessageGraph
from chains import chain1, chain2

REFLECT ='reflect'
GENERATE ='generate'

def generate_tweet(state):
    return({
        chain1.invoke({'messages':state})
    })

def critique_tweet(state):
    response = chain2.invoke({'messages':state})
    return [HumanMessage(content=response.content)]

def should_end(state):
    if len(state) > 2:
        return END
    else:
        return REFLECT

graph = MessageGraph()

graph.add_node(GENERATE , chain1)
graph.add_node(REFLECT, chain2)
graph.set_entry_point(GENERATE)
graph.add_conditional_edges(
    GENERATE, 
    should_end,
    {
        REFLECT: REFLECT,
        END: END
    }
)
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

app.get_graph().print_ascii()



response = app.invoke(HumanMessage(content="AI AGENTS ARE COOL or NOT"))

print(response)

