import os
import time
import logging
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import ORJSONResponse
from dotenv import load_dotenv
from brain import analyze_message

# 1. SETUP & LOGGING
load_dotenv()
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [SAAVI-SHIELD-LOG] - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize with ORJSON for maximum speed
app = FastAPI(
    title="SAAVI-Shield Agentic Honeypot",
    default_response_class=ORJSONResponse
)

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
        "version": "2.1.0-Universal",
        "engine": "Gemini-3-Flash-Ready"
    }

@app.post("/test-honeypot")
async def evaluate(request: Request, x_api_key: str = Header(None)):
    # AUTHENTICATION
    EXPECTED_KEY = os.getenv("MY_HONEYPOT_KEY")
    if not x_api_key or x_api_key != EXPECTED_KEY:
        logger.warning(f"Unauthorized access attempt from {request.client.host}")
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    # UNIVERSAL DATA CATCHER
    scam_text = ""
    try:
        # Try to parse as JSON first
        body = await request.json()
        if isinstance(body, dict):
            # Grab the first string value it finds (flexible for any key name)
            scam_text = next((str(v) for v in body.values() if isinstance(v, str)), "")
        elif isinstance(body, str):
            scam_text = body
    except:
        # If not JSON, read raw body bytes (handles plain text)
        raw_body = await request.body()
        scam_text = raw_body.decode("utf-8")

    # Final validation of text content
    if not scam_text or len(scam_text.strip()) < 2:
        logger.error("Empty request body received")
        raise HTTPException(status_code=422, detail="INVALID_REQUEST_BODY: No text found")

    # INTELLIGENCE GATHERING
    try:
        intelligence = await analyze_message(scam_text)
        
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
            "error": "Intelligence engine timeout, but endpoint is active."
        }
