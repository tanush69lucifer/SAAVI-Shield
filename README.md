# 🛡️ SAAVI-Shield: Agentic AI Honeypot

**SAAVI-Shield** is a high-intelligence, agentic honeypot API designed to detect, analyze, and neutralize social engineering threats in real-time. Built for maximum resilience and forensic depth, it transforms passive detection into active threat intelligence.

## 🚀 Key Features
- **Agentic Intelligence**: Utilizes Gemini 3.0 Flash (2026 Engine) for deep psychological profiling of scammers.
- **Forensic Extraction**: Automatically isolates URLs, phone numbers, and crypto wallets from malicious payloads.
- **Beast Mode Performance**: Implemented with **FastAPI** and **ORJSON** for sub-millisecond serialization and high-concurrency handling.
- **Threat Actor Profiling**: Identifies psychological triggers (Fear, Urgency, Authority) to categorize attacker sophistication.

## 🛠️ Tech Stack
- **Framework**: FastAPI (Asynchronous Server Gateway Interface).
- **AI Engine**: Google Gemini 2.5/3.0 Flash.
- **Validation**: Pydantic v2 (Strict Data Modeling).
- **Performance**: ORJSON & Structured Logging.

## 🚦 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt'''
2. Environment Setup
Create a .env file:

Plaintext
GEMINI_API_KEY=your_key_here
MY_HONEYPOT_KEY=your_secret_tester_key
3. Run the Shield
Bash
uvicorn main:app --host 0.0.0.0 --port 8000
📊 API Specification
Endpoint: POST /test-honeypot

Headers: X-API-KEY: <your_key>

Payload: {"message": "string"}

Developed for the 2026 Emergency Detection & Response Challenge.
### **Final Checklist Before Your Post:**
1. **`requirements.txt`**: Run `pip freeze > requirements.txt` to lock in your libraries.
2. **`.gitignore`**: Create a file named `.gitignore` and add `.env` inside it so you don't leak your keys.
