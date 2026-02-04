import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with the latest 2026 stable engine
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# ADVANCED PROMPT: Added psychological markers for extra "Wow Factor"
SYSTEM_PROMPT = """
You are a Senior Cyber-Forensics Agent. Analyze the message for scam indicators.
Return ONLY a strict JSON object with these keys:
- is_scam: boolean
- scam_type: string (Phishing, Pig Butchering, Romance, Tech Support, etc.)
- threat_level: 'Low', 'Medium', 'High'
- extracted_entities: { "urls": [], "phones": [], "wallets": [] }
- sophistication: 'Scripted', 'Adaptive', 'Advanced'
- psychological_triggers: list (e.g., 'Fear', 'Urgency', 'Authority', 'Greed')
- bait_response: string (A safe, engaging response to lure the attacker)
"""

async def analyze_message(user_message: str):
    try:
        # Changed to async call for "Beast Mode" performance
        response = await model.generate_content_async(
            f"{SYSTEM_PROMPT}\n\nAnalyze this message: {user_message}"
        )
        
        # Robust JSON cleaning (handles cases where LLM adds extra text)
        text_content = response.text.strip()
        if "```json" in text_content:
            text_content = text_content.split("```json")[1].split("```")[0].strip()
        elif "```" in text_content:
            text_content = text_content.split("```")[1].split("```")[0].strip()
            
        return json.loads(text_content)
        
    except Exception as e:
        # Fallback for the API layer to ensure the honeypot never "crashes"
        return {
            "is_scam": False, 
            "error": "Forensic Analysis Timeout",
            "details": str(e),
            "threat_level": "Unknown"
        }