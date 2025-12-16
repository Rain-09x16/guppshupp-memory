from pydantic import BaseModel
from typing import List
from enum import Enum

class Message(BaseModel):
    role: str
    content: str

class MemoryExtractionRequest(BaseModel):
    messages: List[Message]

class ExtractedMemory(BaseModel):
    preferences: List[str]
    facts: List[str]
    emotional_patterns: List[str]

class PersonalityType(str, Enum):
    CALM_MENTOR = "calm_mentor"
    WITTY_FRIEND = "witty_friend"
    THERAPIST = "therapist"

class PersonalityTransformRequest(BaseModel):
    user_message: str
    personality_type: PersonalityType
    memories: ExtractedMemory

class PersonalityTransformResponse(BaseModel):
    response: str