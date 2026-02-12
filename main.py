from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import requests
from bs4 import BeautifulSoup





load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


emmbeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("faiss_index", emmbeddings,allow_dangerous_deserialization=True)


def search_memory(query):
    results = vectorstore.similarity_search(query, k=5)
    return [result.page_content for result in results]

with open("system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

with open("core_memory.txt","r",encoding="utf-8") as f:
    core_memory=f.read()



##def web_search(query):
   ## headers = {"User-Agent": "Mozilla/5.0"}
    ##url = f"https://html.duckduckgo.com/html?q={query}"
   ## res = requests.get(url, headers=headers)
   ## soup=BeautifulSoup(res.text,"html.parser")

    ##links=[]
    ##for a in soup.find_all("a",href=True):
      ##  text=a.get_text(strip=True)
      ##  href=a['href']
       # if text and href.startswith("http"):
          #  links.append(f"{text}-{href}")
    #if not links:
    #    return "No results found."
    #return "\n".join(links[:5])        



full_prompt=system_prompt +"\n\n"+core_memory

 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

  


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input")
    related_memories = search_memory(user_input)

    messages=[{"role":"system","content":full_prompt}]
    messages.append({"role":"user","content":user_input})

   
    

    for mem in related_memories:
        messages.append({"role":"user","content":f"Relevant memory: {mem}"})

        messages.append({"role":"user","content":user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=1.0,
        top_p=0.95,
        frequency_penalty=0.6,
        presence_penalty=0.2,
    )
    return {"response": response.choices[0].message.content}
