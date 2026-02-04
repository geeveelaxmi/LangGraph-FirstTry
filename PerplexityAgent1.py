from langchain_perplexity import ChatPerplexity
from typing import Annotated,Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    message: Annotated[Sequence[BaseMessage],add_messages]

llm=ChatPerplexity(model="sonar-pro",temperature=0.2)

def call_model(state):
    message=state["message"]
    response=llm.invoke(message)
    return {"message":[response]}

workflow=StateGraph(AgentState)
workflow.add_node("agent",call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent",END)

app=workflow.compile()

user_input=input("Enter a query: ")
output=app.invoke({"message":HumanMessage(content=user_input)})
print(output["message"][1].content)
