from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(model="google_genai:gemini-3.5-flash")
model_response = model.invoke("Hello I am Samip")

print(model_response.content[0]["text"])