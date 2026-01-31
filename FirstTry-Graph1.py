from typing import Dict,TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message:str
    name:str

def greeting_node(state:AgentState)->AgentState:
    """Simple function that gives a greeting message"""
    state["message"]="Hello "+state["name"]+"!. You are doing a great job learning lanGraph"

    return state

graph=StateGraph(AgentState)
graph.add_node("greeter",greeting_node)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app=graph.compile()

result=app.invoke({"name":"Viji"})
print(result)
