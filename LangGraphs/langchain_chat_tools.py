import getpass
import os
import openai
import pandas as pd
print(openai.__version__)


apikey="Open ai your key here"
if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] =  apikey

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated , List
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage


# DataFrame we can replace this with your CSV
data = {
    "order no": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "amount": [9, 3, 5, 7, 9, 10, 9, 4, 5, 5],
    "price": [37, 32, 36, 36, 30, 32, 38, 30, 34, 34],
    "total": [1369, 1056, 1386, 1260, 1080, 1088, 1254, 1170, 1258, 1122]
}
df = pd.DataFrame(data)
print(df.head(5))

class State(TypedDict):
  messages:Annotated[List[dict], add_messages]
  
llm = ChatOpenAI(model ="gpt-3.5-turbo")

#Now we define the tools required for this chatbot

@tool
def ask_order_number() ->str:
  """Asks user to provide an order number from the df that the assistant can look up"""
  return " What if your order number ? (0 to 9 )"

@tool
def ask_amount() ->str: 
  """ Asks user what is the amount , number of items they would like to update"""
  return " What is the New amount ? ( Number of items you want updated )"

@tool
def calculate_and_display(order_no: int, amount: int) -> str:
  """Calculates the total (price * amount), updates the DataFrame, and displays the result."""
  if order_no not in df["order no"].values:
      return f"Order number {order_no} not found."
  price = df.loc[df["order no"] == order_no, "price"].iloc[0]
  total = price * amount
  df.loc[df["order no"] == order_no, "total"] = total
  df.loc[df["order no"] == order_no, "amount"] = amount
  row = df.loc[df["order no"] == order_no].to_dict("records")[0]
  
  print("UPDATED DF")
  print(df.head(5))
  return f"Order {order_no} updated. Total: {total}. Row: {row}"
  
def chatbot(state: State)-> State:
  messages = state["messages"]
  user_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
  print(user_messages)
  
  if len(user_messages)==0:
    print("Did not start no messages")
    return {"messages": [{"role":"assistant", "content" : ask_order_number.invoke({})}]}
  elif len(user_messages) == 1:
    try:
      order_no = int(user_messages[0].content) #convert the number in int
      return{"messages" :[{"role": "assistant", "content": ask_amount.invoke({})}]}
    
    except ValueError:
      return {"messages" : [{"role": "assistant", "content": "Invalid Order Number , Please enter a number between 0 -9"
                             }]}

  elif len(user_messages) >1:
    try:
      order_no = int(user_messages[-2].content)
      amount = int(user_messages[-1].content)
      response = calculate_and_display.invoke({"order_no": order_no , "amount" : amount})
      return {"messages": [{"role": "assistant" , "content": response}]}
    except ValueError: #if message is not a valid int
      return {"messages": [{"rile": "assistant", "content": "Invalid Amount Please enter a number"}]}
  
  return state


#build langgraph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile(checkpointer= MemorySaver())

#Main
def main():
  config = {"configurable" :{"thread_id" : "1"}}
  state = {"messages": []}
  
  while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "q"]:
      print("Goodbye!")
      break
    
    state["messages"].append(HumanMessage(content =user_input))
    for event in graph.stream(state, config, stream_mode="values"):
      if "messages" in event:
        print("messages")
        print(f"Bot: {event['messages'][-1].content}")
    
    state = graph.get_state(config).values
    
if __name__ == "__main__":
  main()
