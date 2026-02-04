from langchain_perplexity import ChatPerplexity
from typing import Annotated,Sequence,List,Union
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    message: Annotated[List[Union[HumanMessage,AIMessage]],add_messages]

llm=ChatPerplexity(model="sonar-pro",temperature=0.2)

def call_model(state:AgentState)->AgentState:
    message=state["message"]
    response=llm.invoke(message)
    print(f"\nAI: {response.content}")
    state["message"].append(AIMessage(content=response.content))
    return state

workflow=StateGraph(AgentState)
workflow.add_node("agent",call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent",END)

app=workflow.compile()
conversation_history=[]

user_input=input("Enter a query: ")
while(user_input!="Exit"):
    conversation_history.append(HumanMessage(content=user_input))
    output=app.invoke({"message":conversation_history})
    conversation_history=output["message"]
    user_input=input("Enter a query: ")


