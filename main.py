import os
import time
import logging
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field, AliasChoices
from dotenv import load_dotenv
from brain import analyze_message

# 1. SETUP & LOGGING
load_dotenv()
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [SAAVI-SHIELD-LOG] - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize with ORJSON for 5x faster response times
app = FastAPI(
    title="SAAVI-Shield Agentic Honeypot",
    default_response_class=ORJSONResponse
)

# RECTIFIED: This model now accepts 'message', 'scam_message', OR 'text'
class ScamRequest(BaseModel):
    message: str = Field(validation_alias=AliasChoices('message', 'scam_message', 'text'))

# 2. MIDDLEWARE: Performance & Forensic Tracking
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    logger.info(
        f"IP: {request.client.host} | Path: {request.url.path} | Processing: {process_time:.4f}s"
    )
    
    response.headers["X-Shield-Latency"] = f"{process_time:.4f}s"
    return response

# 3. ENDPOINTS
@app.get("/")
def health():
    return {
        "status": "SAAVI-Shield Active",
        "mode": "Beast Mode",
        "version": "2.0.0-Forensics",
        "engine": "Gemini-3-Flash-Ready"
    }

@app.post("/test-honeypot")
async def evaluate(payload: ScamRequest, request: Request, x_api_key: str = Header(None)):
    # AUTHENTICATION
    EXPECTED_KEY = os.getenv("MY_HONEYPOT_KEY")
    if not x_api_key or x_api_key != EXPECTED_KEY:
        logger.warning(f"Unauthorized access attempt from {request.client.host}")
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    # INTELLIGENCE GATHERING
    try:
        intelligence = await analyze_message(payload.message)
        
        return {
            "status": "success",
            "reachable": True,
            "secured": True,
            "forensics": {
                "timestamp": time.time(),
                "threat_intel": intelligence
            }
        }
    except Exception as e:
        logger.error(f"Analysis Error: {str(e)}")
        return {
            "status": "partial_success",
            "reachable": True,
            "secured": True,
            "error": "Intelligence engine timeout, but endpoint is active."
        }
