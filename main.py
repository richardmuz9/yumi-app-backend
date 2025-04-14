from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
import sys

print("DEBUG: openai.__file__ =", openai.__file__)
print("DEBUG: openai version =", getattr(openai, "__version__", "NO_VERSION"))
print("DEBUG: does openai have ChatCompletion? =", "ChatCompletion" in dir(openai))
print("DEBUG: Python version =", sys.version_info)


from dotenv import load_dotenv
...

load_dotenv()  # loads .env
openai.api_key = os.getenv("OPENAI_API_KEY")

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

@app.post("/api/gpt")
async def chat(input: PromptInput):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful tutor for students going to Japan."},
                {"role": "user", "content": input.prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        # Return the AI’s message:
        return {"response": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
