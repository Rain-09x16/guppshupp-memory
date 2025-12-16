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

app = FastAPI()

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
            generation_config={"temperature": 0.8}
        )
        return PersonalityTransformResponse(response=response.text)
        
    except Exception as e:
        print(f"PERSONALITY API FAILED: {str(e)}")
        print("SWITCHING TO MOCK DATA FOR PERSONALITY")

        mock_responses = {
            "calm_mentor": "I understand that work is stressful right now. Remember to take small breaks. How can I help you prioritize?",
            "witty_friend": "Pizza is life! 🍕 Don't let the cybersecurity bugs bite. You got this!",
            "therapist": "It sounds like you need some comfort food. It is okay to prioritize self-care when things are tough."
        }
        
        return PersonalityTransformResponse(
            response=mock_responses.get(request.personality_type.value, "I am here for you.")
        )