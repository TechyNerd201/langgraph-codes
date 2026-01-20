from langchain_core.messages import AIMessage , BaseMessage , HumanMessage , SystemMessage, ToolMessage
import json
from typing import List, Dict, Any
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
from models import AnswerQuestion, Reflection
load_dotenv()

tavily_tool = TavilySearchResults(max_results=5  )




def execute_tools(state:List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message = state[-1]

    if not hasattr(last_ai_message, "search_queries") or not last_ai_message.search_queries :
        return []

    tool_messages=[]
    query_results = {}

    for query in last_ai_message.search_queries:
        tool_output = tavily_tool.invoke(query)
        query_results[query] = tool_output
        tool_messages.append(
            ToolMessage(
            content=str(tool_output),
            tool_call_id=f"search_{hash(query)}"
        )
    )


    return tool_messages


mock_responder_output = AnswerQuestion(
    answer="Nagpur climate description...",
    search_queries=[
        'Nagpur average monthly temperature and rainfall data',
        'Extreme weather records for Nagpur temperature',
        'Impact of climate change on Nagpur weather patterns'
    ],
    reflection=Reflection(
        missing="Missing specific data...",
        superfluous="Some redundant info..."
    )
)

conversation_state = [
    HumanMessage(content="What is the weather of Nagpur?"),
    mock_responder_output  
]

# if __name__ == "__main__":
#     print(execute_tools(conversation_state))