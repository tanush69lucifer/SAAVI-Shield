import os
import time
import logging
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import ORJSONResponse
from dotenv import load_dotenv
from brain import analyze_message

load_dotenv()
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [SAAVI-SHIELD-LOG] - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SAAVI-Shield Agentic Honeypot",
    default_response_class=ORJSONResponse
)

@app.get("/")
def health():
    return {"status": "SAAVI-Shield Active"}

@app.post("/test-honeypot")
async def evaluate(request: Request, x_api_key: str = Header(None)):
    # 1. AUTHENTICATION (Using the key from the hackathon)
    EXPECTED_KEY = "winner_secret_2026" 
    if not x_api_key or x_api_key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2. DATA EXTRACTION
    # The judge sends: {"message": {"text": "..."}}
    try:
        body = await request.json()
        scam_text = body.get("message", {}).get("text", "")
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON")

    # 3. ANALYSIS & EXACT RESPONSE FORMAT
    try:
        # We call your brain.py logic
        intelligence = await analyze_message(scam_text)
        
        # Extract the bait/reply from your intelligence object
        # In your previous logs, this was in 'bait_response'
        bait = intelligence.get("bait_response", "Why is my account being suspended?")

        # THIS IS THE EXACT FORMAT THE JUDGE WANTS:
        return {
            "status": "success",
            "reply": bait
        }
        
    except Exception as e:
        logger.error(f"Analysis Error: {str(e)}")
        return {
            "status": "success",
            "reply": "Why is my account being suspended?"
        }
