# CYBERSHIELD AI 2.0 — MEMBER 2 ENVIRONMENT SETUP
## Environment Variable Reference, Configuration Templates & Connectivity Verification

**Author:** Senior DevOps & Backend Integration Specialist (Member 2)  
**Target Recipient:** Backend API & Integration Engineer (Member 1)  
**Project Repository:** `https://github.com/Hackathon-korboo/CyberShield-2.0`  
**Date:** November 14, 2026  
**Implementation Directory:** `backend/`

---

## 1. Environment Variables Discovered in Source Code

The following environment variables are parsed in `backend/app/core/config.py` and consumed by Member 2's AI and file security modules:

```bash
# Primary AI Provider Selection
AI_PROVIDER=gemini

# Cognitive Reasoning Provider Keys
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Local Persistence & Server Configuration
DATABASE_URL=sqlite:///./cybershield.db
HOST=127.0.0.1
PORT=8000
APP_ENV=development
JWT_SECRET=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Threat Intelligence Feeds (Optional)
URLHAUS_AUTH_KEY=your_urlhaus_key_here
PHISHTANK_APP_KEY=your_phishtank_key_here
```

---

## 2. Variable Classification & Priority Matrix

| Variable Name | Priority | Default Value | Purpose & Fallback Behavior |
| :--- | :---: | :---: | :--- |
| **`AI_PROVIDER`** | **Mandatory** | `"gemini"` | Defines default AI engine. Accepted values: `gemini`, `groq`, `openai`. |
| **`GEMINI_API_KEY`** | **Recommended** | `""` | Primary API key for Tier 1 Gemini 1.5 Flash. If absent, engine automatically fails over to Groq. |
| **`GROQ_API_KEY`** | **Recommended** | `""` | Secondary API key for Tier 2 Groq Cloud. If absent, engine fails over to OpenAI or Heuristics. |
| **`OPENAI_API_KEY`** | **Optional** | `""` | Commercial backup key for Tier 3 OpenAI. If absent, engine uses Offline Heuristic Engine. |
| **`DATABASE_URL`** | **Optional** | `"sqlite:///./cybershield.db"` | Relational database connection string. Zero setup required with local SQLite. |
| **`JWT_SECRET`** | **Optional** | `"changeme..."` | Secret key for signing authentication tokens. |

---

## 3. Provider Selection & Fallback Rules

1. **Default Engine Selection**:
   - In `backend/app/core/config.py`, `ai_provider` defaults to `"gemini"`.
   - When requests arrive at `POST /scans/message` or `POST /analyze-message`, `LLMClient` initializes with Gemini 1.5 Flash.
2. **Graceful Degradation Protocol**:
   - If `GEMINI_API_KEY` is not found, the client searches for `GROQ_API_KEY`.
   - If `GROQ_API_KEY` is not found, the client searches for `OPENAI_API_KEY`.
   - If no API keys are present, the client activates the **Tier 4 Deterministic Offline Engine**, which executes in < 2ms with zero external network dependency.
3. **Automated Runtime Failover**:
   - If Gemini returns an HTTP 429 (quota exceeded), HTTP 404 (endpoint version mismatch), or times out (12.0s), `LLMClient` catches the exception and immediately dispatches the request to the next available tier without interrupting user requests.

---

## 4. Where to Configure Variables (Member 1 Instructions)

Member 1 must configure environment variables in their local backend directory:

1. **Create the Environment File**:
   ```bash
   cd backend
   cp .env.example .env
   ```
2. **Populate Credentials**:
   Open `backend/.env` in any text editor and paste your credentials:
   ```bash
   AI_PROVIDER=gemini
   GEMINI_API_KEY=AIzaSy...
   GROQ_API_KEY=gsk_...
   ```
3. **Security Rule**:
   Ensure `backend/.env` is never added to version control. It is already included in `.gitignore`.

---

## 5. How to Verify Provider Connectivity

Once Member 1 has populated `backend/.env`, start the backend server and verify provider health via the diagnostic endpoint:

### Step 1: Start Server
```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Step 2: Query System Diagnostic Endpoint
```bash
curl -X GET http://127.0.0.1:8000/api/v1/system/status
```

### Expected JSON Diagnostic Response:
```json
{
  "status": "healthy",
  "database_connected": true,
  "database_type": "sqlite",
  "providers": [
    {
      "provider_name": "Google Gemini 1.5 Flash (Backup AI 1)",
      "category": "AI Scam Engine",
      "configured": true,
      "status": "operational",
      "details": "Backup multimodal threat reasoning engine active.",
      "env_variable": "GEMINI_API_KEY"
    },
    {
      "provider_name": "Groq Cloud Llama-3.3 (Primary AI)",
      "category": "AI Scam Engine",
      "configured": true,
      "status": "operational",
      "details": "Primary ultra-low latency reasoning provider configured.",
      "env_variable": "GROQ_API_KEY"
    }
  ],
  "app_version": "1.0.0",
  "environment": "development"
}
```

---

## 6. Safe `.env.example` Template (Zero Secrets)

Save this template as `backend/.env.example`:

```bash
# =============================================================================
# CYBERSHIELD AI 2.0 — BACKEND ENVIRONMENT CONFIGURATION TEMPLATE
# Copy this file to backend/.env and populate with your own credentials.
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
# Obtain key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Provider 2: Groq Cloud (Tier 2 Ultra-Low Latency Failover)
# Obtain key from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Provider 3: OpenAI (Tier 3 Commercial Fallback)
# Obtain key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Local Database Persistence (SQLite zero-setup default)
DATABASE_URL=sqlite:///./cybershield.db

# Security & Session Secrets
JWT_SECRET=generate_a_random_32_character_hex_string_here
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
