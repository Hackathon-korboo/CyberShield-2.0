# CYBERSHIELD AI 2.0 — MEMBER 2 DEPENDENCIES & CONFIGURATION
## Runtime Environment, Required Packages & Environment Variable Setup

**Author:** Senior Software Integration Engineer (Member 2)  
**Target Recipient:** Backend API & Integration Engineer (Member 1)  
**Date:** November 14, 2026  
**Implementation Workspace:** `backend/`

---

## 1. Required Python Packages & Versions

Member 2's AI and static file security modules run on **Python 3.10+** (tested and verified on Python 3.13.14). The following dependencies are required in the backend virtual environment:

| Package Name | Minimum Version | Verified Production Version | Purpose |
| :--- | :---: | :---: | :--- |
| **`fastapi`** | `>=0.110.0` | `0.115.8` | High-performance asynchronous API framework |
| **`uvicorn`** | `>=0.28.0` | `0.54.0` | ASGI production web server |
| **`pydantic`** | `>=2.7.0` | `2.10.6` | Data validation, type safety, and schema generation |
| **`python-multipart`** | `>=0.0.9` | `0.0.33` | **CRITICAL**: Form-data parsing for `UploadFile` (static file scanning) |
| **`httpx`** | `>=0.27.0` | `0.28.1` | Asynchronous HTTP client for Gemini/Groq/OpenAI APIs |
| **`python-dotenv`** | `>=1.0.0` | `1.0.1` | Environment variable management from `.env` |
| **`sqlalchemy`** | `>=2.0.0` | `2.0.38` | Relational ORM for scan and report persistence |
| **`pytest`** | `>=8.0.0` | `9.1.1` | Test framework |
| **`pytest-asyncio`** | `>=0.23.0` | `1.4.1.post1` | Asynchronous test execution runner |

### Installation Command
From the `backend/` directory, run:
```bash
pip install fastapi>=0.110.0 uvicorn>=0.28.0 pydantic>=2.7.0 python-multipart>=0.0.33 httpx>=0.27.0 python-dotenv>=1.0.0 sqlalchemy>=2.0.0 pytest>=8.0.0 pytest-asyncio>=0.23.0
```

Or using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 2. Environment Variables & AI Provider Configuration

The AI subsystem loads configuration from environment variables defined in `backend/app/core/config.py`.

### 2.1 Configuration Keys Reference

| Variable Name | Default Value | Required? | Description |
| :--- | :---: | :---: | :--- |
| `AI_PROVIDER` | `"gemini"` | Optional | Primary AI provider: `"gemini"`, `"groq"`, `"openai"` |
| `GEMINI_API_KEY` | `""` | Recommended | Google Gemini API key for Tier 1 reasoning (`gemini-1.5-flash`) |
| `GROQ_API_KEY` | `""` | Recommended | Groq Cloud API key for Tier 2 ultra-low-latency failover |
| `OPENAI_API_KEY` | `""` | Optional | OpenAI API key for Tier 3 commercial backup |
| `DATABASE_URL` | `"sqlite:///./cybershield.db"` | Optional | Database connection string for scan and report persistence |
| `JWT_SECRET` | `"changeme..."` | Optional | Backend authentication token secret |

---

## 3. Safe `.env.example` Template (Zero Secrets)

Place this template in your project as `backend/.env.example`. It contains placeholder values and can be safely shared:

```bash
# =============================================================================
# CYBERSHIELD AI 2.0 — BACKEND ENVIRONMENT CONFIGURATION TEMPLATE
# Copy to .env or .env.local and populate with your own credentials.
# NEVER commit files containing real API keys to version control.
# =============================================================================

# Server Settings
APP_NAME=CyberShield AI API
APP_ENV=development
API_V1_PREFIX=/api/v1
HOST=127.0.0.1
PORT=8000

# Primary AI Provider Configuration
# Supported options: gemini (default), groq, openai
AI_PROVIDER=gemini

# Provider 1: Google Gemini (Tier 1 AI Scam Engine & File Explainer)
# Obtain an API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Provider 2: Groq Cloud (Tier 2 Ultra-Low Latency Failover)
# Obtain an API key from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Provider 3: OpenAI (Tier 3 Commercial Fallback)
# Obtain an API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Local Database Persistence (SQLite zero-setup default)
DATABASE_URL=sqlite:///./cybershield.db

# Security & Session Secrets
JWT_SECRET=generate_a_random_32_character_hex_string_here
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 4. Google Gemini Configuration Instructions

1. **Obtain an API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Generate a Gemini API key.
2. **Configure Backend**:
   - In `backend/.env`, set:
     ```bash
     AI_PROVIDER=gemini
     GEMINI_API_KEY=AIzaSy...
     ```
3. **Execution Behavior**:
   - `LLMClient` automatically selects Gemini 1.5 Flash.
   - If the API key is not provided or network is offline, `ScamMessageAnalyzer` and `FileThreatAnalyzer` automatically run their **deterministic offline heuristic engines**, ensuring zero runtime crashes and 100% test reliability.

---

## 5. Execution Instructions for Member 1

### 5.1 Starting the Backend Server
```bash
cd backend
.\venv\Scripts\Activate.ps1   # On Windows (or source venv/bin/activate on Linux/Mac)
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The server will start at: `http://127.0.0.1:8000`  
Swagger API Documentation: `http://127.0.0.1:8000/docs`

### 5.2 Running the Verification Tests
To run the 15 required offline round test scenarios:
```bash
cd backend
pytest tests/test_member2_offline_round.py -v
```

To run the complete 477-test regression suite:
```bash
cd backend
pytest tests -q
```
