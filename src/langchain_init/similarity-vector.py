from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

texts = ['I like kiwi',
'kiwi is my favorite fruit',
'kiwi is a fruit that is green in color',
'mango is a fruit that is yellow in color',
'lenevo is a good laptop',
'apple makes good laptops',
'kiwi cannot fly',
'kiwi is a bird that cannot fly',
'pegion is a bird that can fly',
]

vectorstore = FAISS.from_texts(texts, embeddings)

# print(vectorstore.similarity_search("which fruit is green in color?", k = 7))
print(vectorstore.similarity_search("linux", k = 7))

