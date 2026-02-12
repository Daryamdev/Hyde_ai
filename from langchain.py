from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import json


load_dotenv()
JSON_FILE = "core_quotes.json"
VECTOR_DIR = "faiss_index"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 30

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    lines = json.load(f)

documents = []
for line in lines:
    text=line.get("text","").strip()
    role=line.get("role","").strip()
    if role in("user","assistant") and text and not text.lower().startswith("uploaded image"):
        documents.append(Document(page_content=text))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)
split_docs = splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(split_docs, embeddings)

vectorstore.save_local(VECTOR_DIR)

print(f"✅ saved to file '{VECTOR_DIR}' and ready for use")
