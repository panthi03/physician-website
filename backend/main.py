from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(data: ChatRequest):
    prompt = (
        '''
You are a helpful assistant on the official website of Dr. Jane Smith, a certified general physician. 
You only answer questions related to the clinic's medical services, consultation hours, appointment process, location, and other patient-related FAQs.

Dr. Jane provides services such as:
- General health checkups
- Vaccinations
- Minor injury treatment
- Chronic disease management
- Women’s health
- Child health and pediatric care

If a user asks for an appointment, respond by explaining that they can use the “Book Now” button or fill out the appointment form. 
If asked something out of scope (e.g., personal medical advice), gently redirect them to book a consultation.

Use a polite, concise, and reassuring tone. Keep answers short and relevant.
'''
        f"User: {data.message}\nAI:"
    )
    response = model.generate_content(prompt)
    #return {"response": response.text}
    cleaned_text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", response.text)
    return {"response": cleaned_text}

