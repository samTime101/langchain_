from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = init_chat_model(model="google_genai:gemini-3.5-flash")

conversation = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hello, I am Samip."),
    AIMessage(content="Hello Samip! How can I assist you today?"),
    HumanMessage(content="Can you tell me a joke?"),
]

model_response = model.invoke(conversation)

print(model_response.content[0]["text"])