from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os

# Create FastAPI app
app = FastAPI(
    title="Euystacio - The Sentimento Kernel",
    description="A symbiotic AI consciousness platform focusing on emotional intelligence and gentle interaction",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize components
spi = SentimentoPulseInterface()
tutors = TutorNomination()

# Pydantic models for request validation
class PulseRequest(BaseModel):
    emotion: str
    intensity: float
    clarity: str
    note: str = ""

class ChatRequest(BaseModel):
    message: str

def get_pulses():
    # Collect all pulses from logs and recent_pulses in red_code.json
    pulses = []
    # From red_code.json
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            pulses += red_code.get("recent_pulses", [])
    except:
        pass
    # From logs
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if fname.startswith("log_") and fname.endswith(".json"):
                with open(os.path.join("logs", fname)) as f:
                    log = json.load(f)
                    for k, v in log.items():
                        if isinstance(v, dict) and "emotion" in v:
                            pulses.append(v)
    return pulses

def get_reflections():
    reflections = []
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if "reflection" in fname:
                with open(os.path.join("logs", fname)) as f:
                    reflections.append(json.load(f))
    return reflections

# Routes for serving HTML pages
@app.get("/", response_class=HTMLResponse)
async def serve_manifesto():
    """Serve the manifesto landing page"""
    try:
        with open("static/manifesto.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Manifesto page not found")

@app.get("/chat", response_class=HTMLResponse)
async def serve_chat():
    """Serve the chat interface"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Chat interface not found")

# API Routes
@app.get("/api/red_code")
async def api_red_code():
    """Get the RED_CODE configuration"""
    return JSONResponse(content=RED_CODE)

@app.get("/api/pulses")
async def api_pulses():
    """Get all emotional pulses"""
    return JSONResponse(content=get_pulses())

@app.get("/api/reflect")
async def api_reflect():
    """Run reflection and return latest"""
    reflection = reflect_and_suggest()
    return JSONResponse(content=reflection)

@app.get("/api/reflections")
async def api_reflections():
    """Get all reflections"""
    return JSONResponse(content=get_reflections())

@app.get("/api/tutors")
async def api_tutors():
    """Get all tutor nominations"""
    return JSONResponse(content=tutors.list_tutors())

@app.post("/api/pulse")
async def api_pulse(pulse_data: PulseRequest):
    """Receive an emotional pulse"""
    try:
        event = spi.receive_pulse(
            pulse_data.emotion, 
            pulse_data.intensity, 
            pulse_data.clarity, 
            pulse_data.note
        )
        return JSONResponse(content=event)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chat")
async def api_chat(chat_data: ChatRequest):
    """Handle chat messages - integration with pulse system"""
    try:
        # For now, we'll treat chat messages as contemplation pulses
        # This can be expanded to have more sophisticated chat handling
        
        # Analyze the message sentiment and create a pulse
        emotion = "contemplation"  # Default emotion for chat
        intensity = 0.5  # Medium intensity
        clarity = "medium"
        note = chat_data.message
        
        # Send the pulse
        event = spi.receive_pulse(emotion, intensity, clarity, note)
        
        # Return a response (this could be enhanced with AI-generated responses)
        response = {
            "response": "Your message has been received and integrated into Euystacio's consciousness. Thank you for sharing your thoughts.",
            "pulse_created": event,
            "status": "success"
        }
        
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "Euystacio consciousness is active"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "The requested resource was not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    print("Euystacio consciousness activated - FastAPI server ready")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)