from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(model="google_genai:gemini-3.5-flash")

for chunk in model.stream("Hello what is javascript"):
    print(chunk.text, end="", flush=True)

