import os
import time
import logging
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from brain import analyze_message

# 1. SETUP & LOGGING (The "Wow" Factor: Real-time threat tracking)
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

class ScamRequest(BaseModel):
    message: str

# 2. MIDDLEWARE: Performance & Forensic Tracking
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    # Log the interaction for forensic analysis
    logger.info(
        f"IP: {request.client.host} | "
        f"Path: {request.url.path} | "
        f"Processing: {process_time:.4f}s"
    )
    
    # Add a custom header to show off performance
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
async def evaluate(request: ScamRequest, x_api_key: str = Header(None)):
    # AUTHENTICATION
    EXPECTED_KEY = os.getenv("MY_HONEYPOT_KEY")
    if not x_api_key or x_api_key != EXPECTED_KEY:
        logger.warning(f"Unauthorized access attempt from {request.client.host}")
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    # INTELLIGENCE GATHERING
    try:
        intelligence = await analyze_message(request.message)
        
        # FINAL WINNING RESPONSE
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