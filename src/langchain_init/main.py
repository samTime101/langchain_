from dataclasses import dataclass
import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

@dataclass
class Context:
    user_id : str

@dataclass
class ResponseFormat:
    summary : str
    tmpr_celsius : float
    tmpr_fahrenheit : float
    humidity : float

@tool('get_weather', description="return weather info", return_direct=False)
def get_weather(city: str) -> str:
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


@tool('locate_user', description="get user's city based on user's context")
def locate_user(runtime: ToolRuntime[Context]) -> str:
    match runtime.context.user_id:
        case 'samip':
            return 'biratnagar'
        case 'spiderman':
            return 'new york'
        case 'batman':
            return 'kathmandu'
        case _:
            return 'unknown'


model = init_chat_model(model='google_genai:gemini-3.5-flash')

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[get_weather, locate_user],
    system_prompt="you are professional weather man, tell weather info in nepali romaized ",
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}

agent_response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "what is the weather like?"
            }
        ]
    },
    config=config,
    context=Context(user_id="samip")
)

print(agent_response['structured_response'])
print("--")
print(agent_response['structured_response'].summary)
print("--")
print(agent_response['structured_response'].tmpr_celsius)
print("--")
print(agent_response['structured_response'].tmpr_fahrenheit)
print("--")
print(agent_response['structured_response'].summary)



# REMEMBERING THE CONTEXT

agent_response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "is this ususal???"
            }
        ]
    },
    config=config,
    context=Context(user_id="samip")
)


print(agent_response['structured_response'])
print("--")
print(agent_response['structured_response'].summary)
print("--")
print(agent_response['structured_response'].tmpr_celsius)
print("--")
print(agent_response['structured_response'].tmpr_fahrenheit)
print("--")
print(agent_response['structured_response'].summary)

