import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Depends

# from router import router as process_router
from pydantic import BaseModel
from app.ai.gemini import Gemini
from app.auth.dependencies import get_user_identifier
from app.auth.throttling import apply_rate_limit

load_dotenv()
app = FastAPI()


def load_system_prompt():
    try:
        with open("system_prompt.md", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None


system_prompt = load_system_prompt()
gemeni_api_key = os.getenv("GEMINI_API_KEY")

if not gemeni_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variable.")

# Create an instance of the Gemini AI platform, ready to use
ai_platform = Gemini(api_key=gemeni_api_key, system_prompt=system_prompt)


# ---------------- Pydantic Mdels ----------------#
class ChatRequest(BaseModel):
    prompt: str  # We expect a json body like {"prompt": "...."}


class ChatResponse(BaseModel):
    response: str  # We will return a json body like {"response": "...."}


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI for AI application!"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, user_id: str = Depends(get_user_identifier)):
    apply_rate_limit(user_id)
    response_text = ai_platform.chat(prompt=request.prompt)
    return ChatResponse(response=response_text)
