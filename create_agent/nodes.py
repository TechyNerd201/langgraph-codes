from dotenv import load_dotenv
from langgraph.prebuilt import ToolExecutor
from agent_reason_agent import react_agent_runnable, tools
from react_state import AgentState


load_dotenv()

def reason_node(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {'agent_outcome': agent_outcome}

tool_executor = ToolExecutor(tools)

def act_node(state: AgentState):
    agent_outcome = state['agent_outcome']
    output = tool_executor.invoke(agent_outcome)
    return {"intermediate_steps": [{agent_action, str(output)}]}


