import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()  # load environment variables from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptInput(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Yumi Backend is live!"}

@app.post("/api/gpt")
async def chat(input: PromptInput):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful tutor for students going to Japan."},
                {"role": "user", "content": input.prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        # Check if the API returned an error:
        if "error" in result:
            return {"error": result["error"]}
        return {"response": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
