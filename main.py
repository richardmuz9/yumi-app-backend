import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure .env contains your actual key

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Yumi Backend is live!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptInput(BaseModel):
    prompt: str

@app.post("/api/gpt")
async def chat(input: PromptInput):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],  # Comma added here
            max_tokens=300,
            temperature=0.7
        )
        return {"response": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
