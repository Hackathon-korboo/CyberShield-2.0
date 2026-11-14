# CYBERSHIELD AI 2.0 — MEMBER 1 CLONE & SETUP GUIDE
## Step-by-Step Repository Onboarding, Dependency Installation & Integration Guide

**From:** Senior DevOps & Backend Integration Specialist (Member 2)  
**To:** Backend API & Integration Engineer (Member 1)  
**Target Repository:** `https://github.com/Hackathon-korboo/CyberShield-2.0`  
**Date:** November 14, 2026  
**Module:** AI Scam Intelligence, Gemini Integration & Antivirus-Style Static File Security

---

## 1. Overview for Member 1

Welcome! This guide outlines how to clone Member 2's completed deliverables from the CyberShield-2.0 repository, configure the Python environment, install required dependencies (notably `python-multipart`), set up API credentials, and verify that the AI and static file security endpoints operate smoothly.

---

## 2. Step 1: Clone the Repository & Check Out Branch

Clone the official repository to your local development machine:

```bash
git clone https://github.com/Hackathon-korboo/CyberShield-2.0.git
cd CyberShield-2.0
```

Check out Member 2's feature branch (or pull the latest `main` branch if already merged):

```bash
# If using dedicated feature branch:
git checkout feature/member-2-ai-scam-analyzer

# Or if pulling directly on main:
git checkout main
git pull origin main
```

---

## 3. Step 2: Set Up Python Virtual Environment

Create and activate a clean Python 3.10+ virtual environment:

### On Windows (PowerShell):
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### On Linux / macOS:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Step 3: Install Required Dependencies

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

> [!IMPORTANT]
> **Critical Package**: Ensure `python-multipart>=0.0.9` is installed. FastAPI requires this package to parse `multipart/form-data` for the new `POST /scans/file` static analysis endpoint.
> ```bash
> pip install python-multipart>=0.0.33
> ```

---

## 5. Step 4: Configure Environment Variables

Create your local `.env` configuration from the provided template:

```bash
cp .env.example .env
```

Open `backend/.env` and configure your credentials:

```bash
# Set primary AI provider (default is gemini)
AI_PROVIDER=gemini

# Primary Provider (Google Gemini 1.5 Flash)
GEMINI_API_KEY=your_gemini_api_key_here

# Secondary Failover Provider (Groq Cloud) - Optional
GROQ_API_KEY=your_groq_api_key_here

# Tertiary Provider (OpenAI) - Optional
OPENAI_API_KEY=your_openai_api_key_here

# Local SQLite Database Persistence (Default)
DATABASE_URL=sqlite:///./cybershield.db
```

> [!TIP]
> If you do not have a Gemini API key immediately available, the system will automatically fall back to Groq Cloud (if configured) or the **Tier 4 Deterministic Offline Heuristic Engine**, which executes in < 2ms with zero network setup!

---

## 6. Step 5: How to Configure Google Gemini & Fallbacks

1. **Obtain Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and generate a free API key.
2. **Set Variable**: Add `GEMINI_API_KEY=AIzaSy...` in `backend/.env`.
3. **Failover Verification**:
   - If Gemini is ever throttled (HTTP 429) or times out (12s), `LLMClient` catches the error and automatically dispatches the query to Groq Cloud (`llama-3.3-70b-versatile`) without dropping the request or crashing the API.

---

## 7. Step 6: Verify Integration with Automated Tests

Before launching the server, run Member 2's automated test suites to ensure your local environment passes all verifications:

### 1. Run the 15 Required Offline Round Scenarios:
```bash
pytest tests/test_member2_offline_round.py -v
```
*Expected Output: `15 passed in ~2 seconds`.*

### 2. Run the 30-Category Fraud & Injection Test Suite:
```bash
pytest tests/test_member2_ai_engine.py -v
```
*Expected Output: `30 passed in ~2 seconds`.*

### 3. Run the Complete Full-Stack Regression Suite:
```bash
pytest tests -q
```
*Expected Output: `477 passed in ~41 seconds`.*

---

## 8. Step 7: How to Integrate into Member 1's FastAPI Backend

If you are merging Member 2's work into an existing backend router, follow these clean integration points:

### 1. Import Member 2 Services in `backend/app/api/v1/router.py`:
```python
from fastapi import File, UploadFile
from app.services.file_security import FileThreatAnalyzer, FileThreatAnalysisResponse
from app.services.message_analyzer import MessageAnalyzerService
```

### 2. Message Analysis Endpoint (`POST /api/v1/scans/message`):
Member 2's `MessageAnalyzerService` is already integrated. It accepts raw message text, runs PII masking, engages LLM reasoning, validates evidence verbatim, and returns a dictionary mapped directly into your `ScanDetailResponse`.

### 3. Static File Threat Analysis Endpoint (`POST /api/v1/scans/file`):
```python
@router.post(
    "/scans/file",
    response_model=ScanDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Antivirus-Style Static File Threat Analysis",
    tags=["File Security"]
)
async def scan_file_master(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> ScanDetailResponse:
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(contents) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds 25 MB limit.")

    # 1. Execute static inspection (zero execution)
    analysis = FileThreatAnalyzer.scan_file_bytes(contents, file.filename or "file")
    
    # 2. Get contextual explanation via Gemini (sanitized metadata only)
    try:
        explanation = await FileThreatAnalyzer.explain_threat_with_gemini(analysis)
        analysis.ai_contextual_explanation = explanation
    except Exception:
        pass

    # 3. Persist Scan and RiskReport in database (same models as URL and Message scans)
    # ...
```

---

## 9. Step 8: Start the Backend Server

Launch the ASGI server using Uvicorn:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The server will be available at:  
- **API Base**: `http://127.0.0.1:8000`  
- **Swagger Interactive API Docs**: `http://127.0.0.1:8000/docs`  
- **System Diagnostic Status**: `http://127.0.0.1:8000/api/v1/system/status`

---

## 10. Step 9: Final Integration Verification

Test the endpoints using `curl` or PowerShell:

### Test A: Message Analysis
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/scans/message" \
     -H "Content-Type: application/json" \
     -d '{"content": "URGENT: Your account suspended. Share your OTP to unlock."}'
```
*Expected: Risk Level `Critical` or `High`, Score $\ge 70$, with verbatim OTP evidence.*

### Test B: Antivirus-Style Static File Analysis
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/scans/file" \
     -F "file=@sample.pdf"
```
*Expected: Risk Level `Safe` (Score: 5/100) for clean PDF; immediate `Critical` (Score: 95/100) if masquerading an executable header.*
