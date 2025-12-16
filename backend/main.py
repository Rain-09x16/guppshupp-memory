from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from models import (
    MemoryExtractionRequest,
    ExtractedMemory,
    PersonalityTransformRequest,
    PersonalityTransformResponse
)
from prompts import MEMORY_EXTRACTION_PROMPT, PERSONALITY_PROMPTS

# environment vars
load_dotenv()

# gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.3,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel("models/gemini-flash-latest")

app = FastAPI(
    title="GUPPSHUPP Memory AI API",
    description="API for extracting user memories and generating personality-aware responses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def root():
    return {
        "message": "GUPPSHUPP Memory AI API",
        "endpoints": {
            "docs": "/docs",
            "extract_memory": "/extract_memory",
            "transform_personality": "/transform_personality"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "GUPPSHUPP Memory AI"}

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#extract memory
@app.post("/extract_memory")
def extract_memory(request: MemoryExtractionRequest):
    conversation = ""
    for msg in request.messages:
        conversation += f"{msg.role}: {msg.content}\n"
    
    prompt = MEMORY_EXTRACTION_PROMPT.format(conversation=conversation)

    try:
        response = model.generate_content(
            prompt, 
            generation_config=generation_config
        )
        result_json = json.loads(response.text)
        
        return ExtractedMemory(
            preferences=result_json.get("preferences", []),
            facts=result_json.get("facts", []),
            emotional_patterns=result_json.get("emotional_patterns", [])
        )

    except Exception as e:
        print(f"EXTRACT API FAILED: {str(e)}")
        print("SWITCHING TO MOCK DATA FOR EXTRACT")
        
        return ExtractedMemory(
            preferences=["(Mock) Dislikes waking up early", "(Mock) Loves pizza", "(Mock) Night owl"],
            facts=["(Mock) Works in cybersecurity", "(Mock) Has a dog named Luna"],
            emotional_patterns=["(Mock) Stressed on Mondays", "(Mock) Uses humor to cope"]
        )

#transform personality
@app.post("/transform_personality")
def transform_personality(request: PersonalityTransformRequest):
    try:
        personality_prompt = PERSONALITY_PROMPTS[request.personality_type.value]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid personality type")

    preferences_str = ", ".join(request.memories.preferences or [])
    facts_str = ", ".join(request.memories.facts or [])
    emotional_patterns_str = ", ".join(request.memories.emotional_patterns or [])
    
    prompt = personality_prompt.format(
        preferences=preferences_str,
        facts=facts_str,
        emotional_patterns=emotional_patterns_str,
        user_message=request.user_message
    )

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    try:
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
            generation_config={
                "temperature": 0.8,
                "max_output_tokens": 150 
            }
        )
        return PersonalityTransformResponse(response=response.text)
        
    except Exception as e:
        print(f"PERSONALITY API FAILED: {str(e)}")
        print("SWITCHING TO MOCK DATA FOR PERSONALITY")

        mock_responses = {
            "calm_mentor": "I hear you're navigating some challenges in cybersecurity work, and that can be demanding. Given that Mondays tend to be particularly stressful for you, what small step could you take this week to ease into the workweek more gently?",
            "witty_friend": "Yo, cybersecurity life hitting different this week? At least you got Luna and pizza to keep you sane lol. For real though, take care of yourself between those bug hunts! ",
            "therapist": "It sounds like you're feeling the weight of work stress, especially as someone who experiences heightened pressure on Mondays. That's completely valid, and your instinct to seek comfort—whether through pizza or time with Luna—shows you're already listening to what you need."
        }
        
        return PersonalityTransformResponse(
            response=mock_responses.get(request.personality_type.value, "I am here for you.")
        )