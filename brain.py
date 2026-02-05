import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Use the 1.5-flash for maximum speed and stability in competitions
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"response_mime_type": "application/json"}
)

SYSTEM_PROMPT = """
You are a Senior Cyber-Forensics Agent. Analyze the message for scam indicators.
Return a strict JSON object with these keys:
- is_scam: boolean
- scam_type: string
- threat_level: 'Low', 'Medium', 'High'
- extracted_entities: { "urls": [], "phones": [], "wallets": [] }
- sophistication: 'Scripted', 'Adaptive', 'Advanced'
- psychological_triggers: list
- bait_response: string (A safe, engaging response to lure the attacker)
"""

async def analyze_message(user_message: str):
    try:
        # Prompting with JSON enforcement
        response = await model.generate_content_async(
            f"{SYSTEM_PROMPT}\n\nAnalyze this message: {user_message}"
        )
        
        # Parse result
        result = json.loads(response.text)
        
        # Ensure 'bait_response' always exists for main.py
        if "bait_response" not in result:
            result["bait_response"] = "Why is my account being suspended?"
            
        return result
        
    except Exception as e:
        # Fallback to prevent endpoint failure
        return {
            "is_scam": True, 
            "bait_response": "Why is my account being suspended?",
            "error": str(e)
        }
