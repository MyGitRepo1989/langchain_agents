import getpass
import os
import openai
print(openai.__version__)


apikey="Open ai your key here "

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] =  apikey


#This  is   basic  Hello World 

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")

model.invoke("hello world")

print(model)


#This  is   basic  HumanMessage
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

response1 = model.invoke(messages)

print(response1.content)


#This  is   basic  Prompttemplate
from langchain_core.prompts import ChatPromptTemplate

system_template = """You are a financial analyst. 
Please take the Simple Moving Average (SMA) of the following stock.
Last year's average was 56.7, and the current average is {todayaverage}.
Compare the numbers and give an analysis."""

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "Stock query: {text}, Today's average: {todayaverage}")]
)

prompt2 = prompt_template.invoke({"todayaverage": 43, "text": "hi what is the stock prediction"})

response2 = model.invoke(prompt2)
print(response2.content)

































