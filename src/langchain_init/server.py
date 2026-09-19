from dataclasses import dataclass
import requests

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherRequest(BaseModel):
    city: str

@dataclass
class ResponseFormat:
    summary: str
    tmpr_celsius: str
    tmpr_fahrenheit: str


@tool("get_weather", description="Get current weather information for a city")
def get_weather(city: str) -> str:
    response = requests.get(
        f"https://wttr.in/{city}?format=j1"
    )

    response.raise_for_status()

    return response.text


model = init_chat_model(
    model="google_genai:gemini-3.5-flash"
)


agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="""
    u r a professional weather assistant.

    when the user asks about weather
    - use the get_weather tool to get the weather
    - explain the weather in nepali romanized language
    - return the temperature in both celsius and fahrenheit
    """,
    response_format=ResponseFormat,
)


@app.post("/weather")
def get_weather_data(data: WeatherRequest):

    city = data.city

    agent_response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"What is the current weather in {city}?"
                }
            ]
        }
    )

    result = agent_response["structured_response"]

    return {
        "city": city,
        "summary": result.summary,
        "temperature_celsius": result.tmpr_celsius,
        "temperature_fahrenheit": result.tmpr_fahrenheit,
    }