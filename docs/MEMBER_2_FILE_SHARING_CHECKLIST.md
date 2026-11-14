# CYBERSHIELD AI 2.0 — MEMBER 2 FILE SHARING CHECKLIST
## Step-by-Step Manual Transfer Guide for Member 1 Integration

**Author:** Senior Software Integration Engineer (Member 2)  
**Target Recipient:** Backend API & Integration Engineer (Member 1)  
**Date:** November 14, 2026  
**Source Directory:** `D:\My Created Projects\adamus hackathon`

---

## 1. Overview & Transfer Instructions

This checklist is designed for **manual copying and pasting** of completed Member 2 files. No automatic scripts, git pushes, or network uploads should be performed. 

Follow this guide to transfer files either as **entire directory blocks** (recommended for cohesive modules) or as **individual files**, verifying each item against the checkboxes below.

---

## 2. Directory Block Transfers (Recommended)

### Directory Block 1: Main AI Scam Engine
- **Source Folder**: `backend/app/services/ai_engine/`
- **Destination Folder in Member 1**: `backend/app/services/ai_engine/`
- **Method**: Copy entire folder.
- **Classification**: **MANDATORY**
- **Files Contained** (7 files):
  - [ ] `__init__.py` — Package export definitions.
  - [ ] `schemas.py` — Pydantic models for scam requests, responses, and indicators.
  - [ ] `prompts.py` — System prompts with XML data boundaries and JSON formatting rules.
  - [ ] `indicator_extractor.py` — Regex extractors for URLs, emails, phone numbers, and domains.
  - [ ] `evidence_validator.py` — Verbatim quote validator eliminating AI hallucinations.
  - [ ] `llm_client.py` — Multi-provider client (Gemini 1.5 Flash $\rightarrow$ Groq $\rightarrow$ OpenAI $\rightarrow$ Heuristics).
  - [ ] `scam_analyzer.py` — Core scam reasoning orchestrator, prompt injection defense, and heuristic engine.

### Directory Block 2: Antivirus-Style Static File Security Subsystem
- **Source Folder**: `backend/app/services/file_security/`
- **Destination Folder in Member 1**: `backend/app/services/file_security/`
- **Method**: Copy entire folder.
- **Classification**: **MANDATORY**
- **Files Contained** (6 files):
  - [ ] `__init__.py` — Package export definitions.
  - [ ] `schemas.py` — Pydantic models for file threat analysis, risk levels, and indicators.
  - [ ] `file_signature_checker.py` — Magic byte signature inspector and extension spoofing detector.
  - [ ] `archive_safety_guard.py` — Safe non-extracting archive inspector (Zip Slip and Zip Bomb defense).
  - [ ] `malware_hash_matcher.py` — $O(1)$ cryptographic hash matcher (EICAR, WannaCry, Emotet, Locky, Mirai).
  - [ ] `file_threat_analyzer.py` — Static inspection orchestrator and Gemini contextual explainer.

---

## 3. Individual File Transfers

### Category A: Core Security & Service Adapters
- [ ] **File Path**: `backend/app/services/nexus/pii_redactor.py`  
  - **Destination**: `backend/app/services/nexus/pii_redactor.py`  
  - **Priority**: **MANDATORY**  
  - **Why Needed**: Redacts PAN, Aadhaar, phone, card, and email tokens before LLM dispatch; provides local reversible mapping.  
  - **Method**: Copy individually.

- [ ] **File Path**: `backend/app/services/message_analyzer.py`  
  - **Destination**: `backend/app/services/message_analyzer.py`  
  - **Priority**: **MANDATORY**  
  - **Why Needed**: High-level adapter bridging Member 2's `AnalyzeMessageResponse` to Member 1's `ScanDetailResponse` and database schemas.  
  - **Method**: Copy individually.

### Category B: Shared API Schemas
- [ ] **File Path**: `backend/app/schemas/ai_analysis.py`  
  - **Destination**: `backend/app/schemas/ai_analysis.py`  
  - **Priority**: **SUPPORTING**  
  - **Why Needed**: Contains request/response models for `/analyze-message` endpoints.  
  - **Method**: Copy individually.

- [ ] **File Path**: `backend/app/schemas/scan.py`  
  - **Destination**: `backend/app/schemas/scan.py`  
  - **Priority**: **SUPPORTING**  
  - **Why Needed**: Contains master unified scan schemas (`ScanDetailResponse`, `MessageIndicator`, `RiskReportSchema`).  
  - **Method**: Inspect and verify compatibility (ensure `MessageIndicator` and `ScanDetailResponse` match).

### Category C: Configuration & Routing Snippets
- [ ] **File Path**: `backend/app/core/config.py`  
  - **Destination**: `backend/app/core/config.py`  
  - **Priority**: **SUPPORTING**  
  - **Why Needed**: Includes `ai_provider: str = "gemini"` setting and smart environment loading logic that prevents live API calls during unit tests.  
  - **Method**: Inspect and merge changes into Member 1's configuration.

- [ ] **File Path**: `backend/app/api/v1/router.py`  
  - **Destination**: `backend/app/api/v1/router.py`  
  - **Priority**: **SUPPORTING (MERGE ONLY)**  
  - **Why Needed**: Contains endpoint registrations for:
    - `POST /scans/file` (Master `ScanDetailResponse` upload endpoint with DB persistence).
    - `POST /analyze-file` (Direct Member 2 `FileThreatAnalysisResponse` endpoint).
  - **Method**: **DO NOT OVERWRITE ENTIRE FILE BLINDLY**. Extract and merge lines defining `POST /scans/file` and `POST /analyze-file`.

- [ ] **File Path**: `backend/.env.example`  
  - **Destination**: `backend/.env.example`  
  - **Priority**: **SUPPORTING**  
  - **Why Needed**: Provides a sanitized environment variable template documenting required keys (`GEMINI_API_KEY`, `GROQ_API_KEY`, etc.) with zero real secrets.  
  - **Method**: Copy individually.

- [ ] **File Path**: `backend/requirements.txt`  
  - **Destination**: `backend/requirements.txt`  
  - **Priority**: **SUPPORTING**  
  - **Why Needed**: Documents required dependencies, including `python-multipart` needed for file upload processing.  
  - **Method**: Ensure `python-multipart>=0.0.9` is present in Member 1's virtual environment.

---

## 4. Test Suite Transfers

- [ ] **File Path**: `backend/tests/test_member2_offline_round.py`  
  - **Destination**: `backend/tests/test_member2_offline_round.py`  
  - **Priority**: **TESTING**  
  - **Why Needed**: Automated test suite executing all 15 required offline round test scenarios. Member 1 must run this to verify integration.  
  - **Method**: Copy individually.

- [ ] **File Path**: `backend/tests/test_member2_ai_engine.py`  
  - **Destination**: `backend/tests/test_member2_ai_engine.py`  
  - **Priority**: **TESTING**  
  - **Why Needed**: Comprehensive suite of 30 unit tests validating fraud categories, adversarial injection defense, and PII masking.  
  - **Method**: Copy individually.

- [ ] **File Path**: `backend/tests/test_member2_integration.py`  
  - **Destination**: `backend/tests/test_member2_integration.py`  
  - **Priority**: **TESTING**  
  - **Why Needed**: Integration tests verifying that `/analyze-message` seamlessly responds to both Member 1 and Member 2 contracts.  
  - **Method**: Copy individually.

---

## 5. Documentation Transfers

- [ ] **File Path**: `docs/OFFLINE_MEMBER_2_AUDIT.md`  
- [ ] **File Path**: `docs/OFFLINE_MEMBER_2_IMPLEMENTATION_REPORT.md`  
- [ ] **File Path**: `docs/OFFLINE_MEMBER_2_GEMINI_REPORT.md`  
- [ ] **File Path**: `docs/OFFLINE_MEMBER_2_FILE_SECURITY_REPORT.md`  
- [ ] **File Path**: `docs/OFFLINE_MEMBER_2_TEST_RESULTS.md`  
- [ ] **File Path**: `docs/MEMBER_2_TO_MEMBER_1_HANDOVER.md`  
- [ ] **File Path**: `docs/MEMBER_2_API_INTEGRATION_GUIDE.md`  
- [ ] **File Path**: `docs/MEMBER_2_DEPENDENCIES_AND_CONFIGURATION.md`  
- [ ] **File Path**: `docs/MEMBER_2_TEST_AND_VERIFICATION_REPORT.md`  
- [ ] **File Path**: `docs/MEMBER_2_FINAL_SHARING_SUMMARY.md`  
  - **Destination**: `docs/`  
  - **Priority**: **DOCUMENTATION**  
  - **Method**: Copy all markdown reports into Member 1's `docs/` folder.

---

## 6. SENSITIVE FILES — NEVER SHARE

Verify that the following files are **STRICTLY EXCLUDED** from manual copying:
- [x] **DO NOT SHARE**: `API.env` (Contains real live API credentials).
- [x] **DO NOT SHARE**: `backend/.env.local` or `.env` (Contains private environment secrets).
- [x] **DO NOT SHARE**: `backend/cybershield.db` (Local SQLite database with historical records).
- [x] **DO NOT SHARE**: `backend/venv/` (Local Python virtual environment).
- [x] **DO NOT SHARE**: `backend/**/__pycache__/` (Compiled Python bytecode).

---

## 7. Verification Checklist After Transfer

Once Member 1 has copied all mandatory and supporting files:
1. [ ] Activate Member 1's virtual environment: `source venv/bin/activate` or `.\venv\Scripts\Activate.ps1`.
2. [ ] Install required dependencies: `pip install python-multipart`.
3. [ ] Run the 15-scenario verification suite: `pytest tests/test_member2_offline_round.py -v`.
4. [ ] Confirm that all 15 scenarios pass with 0 failures.
5. [ ] Run full regression suite: `pytest tests -q`.
6. [ ] Confirm that all 477 tests pass with 0 regressions.
