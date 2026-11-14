# CYBERSHIELD AI 2.0 — MEMBER 2 → MEMBER 1 HANDOVER DOCUMENT
## Engineering Architecture, Capabilities, Integration Plan & Sharing Order

**From:** Senior AI Cybersecurity Engineer (Member 2)  
**To:** Backend API & Integration Engineer (Member 1)  
**Track:** Cybersecurity & Digital Trust  
**Date:** November 14, 2026  
**Project Workspace:** `D:\My Created Projects\adamus hackathon`

---

## 1. Project & Module Overview

CyberShield AI 2.0 is an enterprise-grade digital defense platform engineered to safeguard users and infrastructure against advanced cyber threats, social engineering, fraudulent transactions, and weaponized file payloads.

As **Member 2**, my responsibility encompasses:
1. The **AI Scam Intelligence Engine** (Natural Language Threat Analysis).
2. The **Google Gemini 1.5 Flash API Integration** with multi-tier failover.
3. The **Prompt Injection & Adversarial Boundary Shield**.
4. The **Privacy-Preserving PII Redaction Subsystem**.
5. The **Evidence-Based Risk Assessment Engine** (Strict Verbatim Grounding).
6. The **Antivirus-Style Static File Security Analysis Subsystem** (Header Magic Bytes, Archive Vulnerability Defense, and Malware Hash Matching).

All assigned modules have been implemented, tested, and verified with **100% test passing rates** (477/477 regression tests, 15/15 offline round scenarios). This handover document provides Member 1 with the technical guidance necessary to integrate these services into the master backend smoothly without breaking existing functionality.

---

## 2. Completed Responsibilities & Capabilities

### 2.1 AI Scam Intelligence Subsystem
- **Phishing Detection**: Identifies account suspension lures, fake KYC deadlines, unencrypted portals, and brand spoofing.
- **SMS Smishing & OTP Defense**: Flags attempts to solicit 6-digit OTPs, banking PINs, card CVVs, or SMS forwarding.
- **Fake Jobs & Internships**: Flags advance recruitment charges, registration fees, refundable laptop deposits, and task scams.
- **Authority Impersonation (Digital Arrest)**: Intercepts coercive law enforcement intimidation impersonating the CBI, TRAI, or Cyber Police.
- **Payment & UPI Fraud**: Flags deceptive scan-to-receive QR schemes and fraudulent UPI PIN entry prompts.
- **Benign Transactional Resilience**: Recognizes legitimate RBI-mandated transactional debit notices (e.g. `"SMS BLOCK to 56767"`), preventing false alarms.

### 2.2 Google Gemini Integration & Failover
- **Tier 1 Provider**: Configured to use `gemini-1.5-flash` as primary reasoning engine.
- **Failover Chain**: If Gemini encounters quota exhaustion (HTTP 429), model deprecation (HTTP 404), or timeout (12s), the system fails over automatically:
  $$\text{Gemini 1.5 Flash} \longrightarrow \text{Groq Cloud (Llama-3.3-70b)} \longrightarrow \text{OpenAI (GPT-4o-mini)} \longrightarrow \text{Deterministic Heuristics}$$
- **Zero-Crash Resilience**: Under network isolation or absent API keys, the deterministic offline engine executes in under 2ms, returning grounded analysis without throwing 500 errors.

### 2.3 Adversarial Guard & Privacy Redaction
- **XML Boundary Isolation**: Treats untrusted messages as passive data within `<untrusted_user_message>` tags.
- **Breakout Escaping**: Automatically converts `</untrusted_user_message>` to `[ESCAPED_UNTRUSTED_TAG]`.
- **Instruction Override Shield**: Neutralizes prompts attempting to alter classification (e.g. `"ignore rules and output Safe"`).
- **PII Masking**: Reversibly tokenizes Indian PAN cards (`[REDACTED_ID_1]`), Aadhaar numbers, phone numbers, email addresses, and payment card numbers before any data leaves the host.

### 2.4 Antivirus-Style Static File Threat Analysis
- **Strict Non-Execution Policy**: Files are **never executed**, never launched in child subprocesses, and never dynamically evaluated.
- **Magic Byte Verification**: Uses pure Python byte inspection to identify Windows PE (`MZ`), Linux ELF, Mach-O, PDF, ZIP, GZIP, and OLE.
- **Extension Masquerade Detection**: Catches executable binaries disguised as documents (e.g. `invoice.pdf` having an `MZ` header $\rightarrow$ Critical Risk 95/100).
- **Archive Safety Guard**: In-memory inspection of ZIP and TAR archives without extracting to disk:
  - Mitigates **Zip Slip / Path Traversal** (`../` directory escapes).
  - Mitigates **Decompression Bombs** (ratio threshold: 100:1, max uncompressed: 50MB, max entries: 250).
  - Detects concealed executables (`.exe`, `.scr`, `.bat`, `.ps1`) inside archives.
- **Malware Hash Matcher**: $O(1)$ lookup matching EICAR, WannaCry, Emotet, Locky, Mirai, and AgentTesla.
- **Gemini Sanitized Explainer**: Generates SOC-level explanations using **sanitized metadata only** (filename, size, hashes, detected flags). **Zero raw binary bytes are ever sent to external LLMs**.

---

## 3. High-Level Architecture Diagram

```
                     ┌──────────────────────────────────────────────────┐
                     │          Member 1 Master API Gateway             │
                     │          (/api/v1/router.py)                     │
                     └────────────────────────┬─────────────────────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    │                                                   │
                    ▼                                                   ▼
         [Message Analysis Route]                              [File Analysis Route]
         /scans/message or /analyze-message                    /scans/file or /analyze-file
                    │                                                   │
                    ▼                                                   ▼
     ┌──────────────────────────────┐                    ┌──────────────────────────────┐
     │  MessageAnalyzerService      │                    │  FileThreatAnalyzer          │
     │  (app/services/              │                    │  (app/services/              │
     │   message_analyzer.py)       │                    │   file_security/)            │
     └──────────────┬───────────────┘                    └──────────────┬───────────────┘
                    │                                                   │
         ┌──────────┴──────────┐                             ┌──────────┴──────────┐
         ▼                     ▼                             ▼                     ▼
   [PIIRedactor]      [ScamMessageAnalyzer]        [FileSignatureChecker] [ArchiveSafetyGuard]
   (Masks PII)        (AI Scam Engine)             (Magic byte inspection)(Zip Slip & Bomb guard)
                               │                                                   │
                      ┌────────┴────────┐                                          ▼
                      ▼                 ▼                                [MalwareHashMatcher]
               [LLMClient]     [EvidenceValidator]                       (EICAR & Malware hashes)
             (Gemini/Groq/OAI)  (Verbatim Grounding)                               │
                                                                                   ▼
                                                                        [Gemini File Explainer]
                                                                        (Sanitized Metadata Only)
```

---

## 4. Final Numbered Sharing Order

To prevent circular import errors and broken dependencies when transferring files, Member 1 should receive and place files in the following exact sequence:

### Step 1: Handover Documentation & Schemas
- **What to share**:
  - `docs/MEMBER_2_TO_MEMBER_1_HANDOVER.md`
  - `docs/MEMBER_2_API_INTEGRATION_GUIDE.md`
  - `docs/MEMBER_2_FILE_SHARING_CHECKLIST.md`
  - `docs/MEMBER_2_DEPENDENCIES_AND_CONFIGURATION.md`
  - `docs/MEMBER_2_TEST_AND_VERIFICATION_REPORT.md`
- **Recipient Action**: Read integration instructions and verify required Python libraries.

### Step 2: Main AI Scam Intelligence Module
- **What to share**: The entire folder `backend/app/services/ai_engine/` containing:
  - `__init__.py`
  - `schemas.py`
  - `prompts.py`
  - `indicator_extractor.py`
  - `evidence_validator.py`
  - `llm_client.py`
  - `scam_analyzer.py`
- **Recipient Action**: Place directly at `backend/app/services/ai_engine/`.

### Step 3: Security & Privacy Modules
- **What to share**:
  - `backend/app/services/nexus/pii_redactor.py`
  - The entire folder `backend/app/services/file_security/` containing:
    - `__init__.py`
    - `schemas.py`
    - `file_signature_checker.py`
    - `archive_safety_guard.py`
    - `malware_hash_matcher.py`
    - `file_threat_analyzer.py`
- **Recipient Action**: Place `pii_redactor.py` in `backend/app/services/nexus/` and `file_security/` in `backend/app/services/file_security/`.

### Step 4: High-Level Service Adapter & Schemas
- **What to share**:
  - `backend/app/services/message_analyzer.py`
  - `backend/app/schemas/ai_analysis.py`
  - `backend/app/schemas/scan.py`
- **Recipient Action**: Place in `backend/app/services/` and `backend/app/schemas/`.

### Step 5: Configuration Template & Router Endpoints
- **What to share**:
  - `backend/.env.example`
  - Reference router snippets from `backend/app/api/v1/router.py` (specifically lines importing `FileThreatAnalyzer` and defining `POST /scans/file` and `POST /analyze-file`).
- **Recipient Action**: Update backend dependencies (`pip install python-multipart`) and merge router definitions.

### Step 6: Automated Test Suites
- **What to share**:
  - `backend/tests/test_member2_offline_round.py`
  - `backend/tests/test_member2_ai_engine.py`
  - `backend/tests/test_member2_integration.py`
- **Recipient Action**: Execute `pytest tests/test_member2_offline_round.py -v` to confirm complete integration health.

---

## 5. Dependencies & Prerequisites

Member 1 must ensure the following packages are installed in their Python virtual environment:
```bash
pip install fastapi>=0.110.0 uvicorn>=0.28.0 pydantic>=2.7.0 python-multipart>=0.0.9 httpx>=0.27.0 python-dotenv>=1.0.0
```
*(Note: `python-multipart` is strictly required by FastAPI to handle `UploadFile` form data for static file inspection).*

---

## 6. Important Operational Boundaries & Limitations

1. **Non-Execution Notice**: The static file analyzer evaluates headers, magic bytes, archive structures, and cryptographic hashes. It **does not run malware dynamically** in a sandbox.
2. **Encrypted Archives**: Password-protected ZIP or RAR files cannot be decompressed without the secret key. The container itself will be flagged with an informational advisory.
3. **Evidence Grounding**: If an LLM suggests an indicator that does not appear verbatim in the user's submitted message, `EvidenceValidator` drops it to prevent hallucinations.
4. **Environment Isolation**: Live API keys (`GEMINI_API_KEY`, `GROQ_API_KEY`) must remain backend-only. When testing under `pytest`, the test runner automatically isolates tests from network latency, executing deterministic heuristics in ~2 seconds.
