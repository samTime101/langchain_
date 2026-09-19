import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()

@tool('get_weather', description="return weather info", return_direct=False)
def get_weather(city: str) -> str:
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


agent = create_agent(model='google_genai:gemini-3.5-flash', tools=[get_weather], system_prompt="you are professional weather man, tell weather info in nepali romaized ")

agent_response = agent.invoke({
    'messages' : {'role' :'user', 'content' : 'what is the weather in biratnagar?'}
})

print(agent_response['messages'][-1].content[0]["text"])
