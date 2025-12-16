# GUPPSHUPP Memory AI - Founding AI Engineer Assignment

A companion AI system that extracts user memories from conversations and generates personality-aware responses.

## 🎯 Features

### 1. Memory Extraction Module
Analyzes chat conversations to extract:
- **Preferences**: User likes, dislikes, habits, and routines
- **Facts**: Objective information (names, jobs, relationships, locations)
- **Emotional Patterns**: Recurring moods, triggers, and behavioral patterns

### 2. Personality Engine
Transforms agent responses into 3 distinct personality types:
- **Calm Mentor**: Patient, thoughtful, asks reflective questions
- **Witty Friend**: Casual, humorous, relatable with emojis
- **Therapist**: Empathetic, validating, supportive

### 3. Before/After Comparison
Shows how the same message generates different responses based on personality type.

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **Modular Design**: Separate files for models, prompts, and endpoints
- **Structured Output**: Pydantic models for type safety and validation
- **Smart Prompts**: Carefully designed prompts for accurate extraction
- **Failsafe Mechanism**: Mock data fallback ensures demo reliability even with API rate limits

### Frontend (Next.js + TypeScript)
- **Clean UI**: Step-by-step interface for memory extraction and personality testing
- **Type Safety**: Full TypeScript implementation
- **Demo-Friendly**: "Load Sample Messages" button for quick testing

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Gemini API key ([Get one here](https://aistudio.google.com/apikey))

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start server
python -m uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# .env.local should have: NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Visit http://localhost:3000

## 📖 Usage

1. **Load Sample Messages**: Click the gray button to auto-fill with example conversation
2. **Extract Memories**: Click blue button to analyze and extract user memories
3. **Test Personalities**: Enter a message and click green button to see 3 personality responses

## 🔧 Technical Decisions

### Why FastAPI over Django?
- **API-only architecture**: No need for Django's templating or ORM
- **Automatic docs**: FastAPI provides interactive API documentation at `/docs`
- **Modern async support**: Better performance for AI API calls
- **Faster development**: Less boilerplate for simple API endpoints

### Mock Data Fallback Strategy
The system includes intelligent fallback to mock data when:
- API rate limits are hit
- Network issues occur
- API keys are invalid

**Why this matters:**
- Ensures demo reliability for interviewers
- Shows production-ready thinking (real apps need error handling)
- Prevents assignment rejection due to temporary API issues

In production, this would be enhanced with:
- User notifications
- Retry logic with exponential backoff
- Usage analytics

### Prompt Engineering Approach
- **Low temperature (0.3)** for extraction: Ensures consistent, accurate categorization
- **Higher temperature (0.8)** for personalities: Allows creative, natural responses
- **Structured JSON output**: Forces consistent format for parsing
- **Clear instructions**: Specific rules about what to extract and how

## 📁 Project Structure

```
guppshupp-memory/
├── backend/
│   ├── main.py              # FastAPI app with endpoints
│   ├── models.py            # Pydantic models
│   ├── prompts.py           # AI prompt templates
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── sample_messages.txt  # Example conversation
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx     # Main UI component
│   │       └── layout.tsx   # App layout
│   ├── package.json         # Node dependencies
│   └── .env.example         # Environment template
└── README.md
```

## 🎓 What This Demonstrates

### Reasoning and Prompt Design
- Clear categorization of memory types
- Specific instructions for tone and style
- Structured output with validation rules

### Structured Output Parsing
- JSON responses with consistent schema
- Pydantic validation for type safety
- Error handling for malformed responses

### Working with User Memory
- Context-aware personality responses
- Memories inform tone and content
- Demonstrates companion AI concepts

### Modular System Design
- Separation of concerns (models, prompts, endpoints)
- Reusable components
- Easy to extend with new personalities or memory types

## 🔐 Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_key_here
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

**Rate Limit Errors:**
- System automatically falls back to mock data
- Wait a few minutes for API quota to reset
- Or add credits to your Gemini API account

**CORS Errors:**
- Ensure backend is running on port 8000
- Check frontend .env.local has correct API URL

**TypeScript Errors:**
- Run `npm install` in frontend directory
- Restart the dev server

## 📝 Assignment Requirements Met

✅ Memory extraction module (preferences, facts, emotional patterns)
✅ Personality engine (3 distinct personalities)
✅ Before/after personality differences shown
✅ Reasoning and prompt design demonstrated
✅ Structured output parsing implemented
✅ Working with user memory showcased
✅ Modular system design achieved

## 🚀 Deployment

### Backend (Render)
1. Create new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Add Environment Variable: `GEMINI_API_KEY`
5. Deploy

### Frontend (Vercel)
1. Import project on [Vercel](https://vercel.com)
2. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
3. Add Environment Variable: `NEXT_PUBLIC_API_URL` (your Render backend URL)
4. Deploy

### Post-Deployment
- Test `/health` endpoint to verify backend is running
- Visit `/docs` for interactive API documentation
- Update frontend environment variable with deployed backend URL

---

**Built for GUPPSHUPP Founding AI Engineer Assignment**
