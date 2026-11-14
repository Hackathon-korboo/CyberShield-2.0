# CYBERSHIELD AI 2.0 — MEMBER 2 → MEMBER 1 FILE MANIFEST
## Shareable File Inventory & Integration Priority Matrix

**Author:** Senior Software Integration Engineer (Member 2)  
**Recipient:** Backend API & Integration Engineer (Member 1)  
**Project Workspace:** `D:\My Created Projects\adamus hackathon`  
**Date:** November 14, 2026  
**Scope:** AI Scam Intelligence, Gemini Integration, PII Redaction, and Antivirus-Style Static File Security

---

### Classification Legend:
- **MANDATORY (A)**: Essential backend service modules that Member 1 must copy to run the AI engine and file security analyzer.
- **SUPPORTING (B)**: Schemas, service wrappers, and environment configuration templates needed for clean architecture.
- **TESTING (C)**: Automated test suites verifying real runtime behavior across 15 offline round scenarios and regression tests.
- **OPTIONAL (D)**: Verification scripts and standalone empirical test tools.
- **DO NOT SHARE (E)**: Sensitive credential files, live `.env` files, virtual environments, local caches, and compiled bytecode.

---

## 1. Complete File Manifest Table

| No. | Exact File Path (Relative to Project Root) | File Name | Purpose | Priority | Share? |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **01** | `backend/app/services/ai_engine/__init__.py` | `__init__.py` | Package export definitions for AI Scam Analyzer module | MANDATORY | **YES** |
| **02** | `backend/app/services/ai_engine/schemas.py` | `schemas.py` | Pydantic data contracts for scam requests, responses, and indicators | MANDATORY | **YES** |
| **03** | `backend/app/services/ai_engine/prompts.py` | `prompts.py` | XML-isolated system prompts, output constraints, and boundary markers | MANDATORY | **YES** |
| **04** | `backend/app/services/ai_engine/indicator_extractor.py` | `indicator_extractor.py` | Passive extraction of URLs, emails, phone numbers, and domains | MANDATORY | **YES** |
| **05** | `backend/app/services/ai_engine/evidence_validator.py` | `evidence_validator.py` | Grounding filter enforcing verbatim quotes to eliminate AI hallucinations | MANDATORY | **YES** |
| **06** | `backend/app/services/ai_engine/llm_client.py` | `llm_client.py` | Multi-tier provider client (Gemini 1.5 Flash $\rightarrow$ Groq $\rightarrow$ OpenAI $\rightarrow$ Heuristics) | MANDATORY | **YES** |
| **07** | `backend/app/services/ai_engine/scam_analyzer.py` | `scam_analyzer.py` | Core scam reasoning orchestrator, prompt injection defense, and heuristic rules | MANDATORY | **YES** |
| **08** | `backend/app/services/nexus/pii_redactor.py` | `pii_redactor.py` | Zero-trust PII masking engine (PAN, Aadhaar, Cards, Phone, Email) with local token map | MANDATORY | **YES** |
| **09** | `backend/app/services/message_analyzer.py` | `message_analyzer.py` | High-level service wrapper adapting Member 2 contracts to Member 1's `ScanDetailResponse` | MANDATORY | **YES** |
| **10** | `backend/app/services/file_security/__init__.py` | `__init__.py` | Package export definitions for Static File Security module | MANDATORY | **YES** |
| **11** | `backend/app/services/file_security/schemas.py` | `schemas.py` | Pydantic data contracts for file threat analysis, risk levels, and indicators | MANDATORY | **YES** |
| **12** | `backend/app/services/file_security/file_signature_checker.py` | `file_signature_checker.py` | Pure Python magic byte checker, binary header parser, and extension spoofing detector | MANDATORY | **YES** |
| **13** | `backend/app/services/file_security/archive_safety_guard.py` | `archive_safety_guard.py` | Non-extracting archive inspector mitigating Zip Slip traversal and Decompression Bombs | MANDATORY | **YES** |
| **14** | `backend/app/services/file_security/malware_hash_matcher.py` | `malware_hash_matcher.py` | $O(1)$ in-memory cryptographic hash matching (EICAR, WannaCry, Emotet, Locky, Mirai) | MANDATORY | **YES** |
| **15** | `backend/app/services/file_security/file_threat_analyzer.py` | `file_threat_analyzer.py` | Main static file threat orchestrator and sanitized Gemini contextual explainer | MANDATORY | **YES** |
| **16** | `backend/app/schemas/ai_analysis.py` | `ai_analysis.py` | Unified API schema definitions for message analysis endpoints | SUPPORTING | **YES** |
| **17** | `backend/app/schemas/scan.py` | `scan.py` | Unified scan models (`ScanDetailResponse`, `MessageIndicator`, `RiskReportSchema`) | SUPPORTING | **YES** |
| **18** | `backend/app/core/config.py` | `config.py` | Settings loader with smart test isolation and Gemini prioritization (`ai_provider="gemini"`) | SUPPORTING | **YES** |
| **19** | `backend/app/api/v1/router.py` | `router.py` | Reference FastAPI router registering `/scans/message`, `/scans/file`, `/analyze-file` | SUPPORTING | **YES** |
| **20** | `backend/.env.example` | `.env.example` | Sanitized environment variable template with zero secret values | SUPPORTING | **YES** |
| **21** | `backend/requirements.txt` | `requirements.txt` | Python dependency specification including `fastapi`, `pydantic`, `python-multipart` | SUPPORTING | **YES** |
| **22** | `backend/tests/test_member2_offline_round.py` | `test_member2_offline_round.py` | Comprehensive test suite covering all 15 required offline round test scenarios | TESTING | **YES** |
| **23** | `backend/tests/test_member2_ai_engine.py` | `test_member2_ai_engine.py` | 30 unit tests validating fraud categories, adversarial injection, and PII masking | TESTING | **YES** |
| **24** | `backend/tests/test_member2_integration.py` | `test_member2_integration.py` | Integration test validating Member 1 API endpoint backward compatibility | TESTING | **YES** |
| **25** | `docs/OFFLINE_MEMBER_2_AUDIT.md` | `OFFLINE_MEMBER_2_AUDIT.md` | Audit of existing vs offline architecture, gap analysis, and security principles | DOCUMENTATION | **YES** |
| **26** | `docs/OFFLINE_MEMBER_2_IMPLEMENTATION_REPORT.md` | `OFFLINE_MEMBER_2_IMPLEMENTATION_REPORT.md` | Detailed architectural breakdown of AI engine and static file threat analysis | DOCUMENTATION | **YES** |
| **27** | `docs/OFFLINE_MEMBER_2_GEMINI_REPORT.md` | `OFFLINE_MEMBER_2_GEMINI_REPORT.md` | Gemini API configuration, XML prompt design, rate-limit backoff, and failover telemetry | DOCUMENTATION | **YES** |
| **28** | `docs/OFFLINE_MEMBER_2_FILE_SECURITY_REPORT.md` | `OFFLINE_MEMBER_2_FILE_SECURITY_REPORT.md` | Technical report on magic bytes, archive limits, hash matching, and non-execution bounds | DOCUMENTATION | **YES** |
| **29** | `docs/OFFLINE_MEMBER_2_TEST_RESULTS.md` | `OFFLINE_MEMBER_2_TEST_RESULTS.md` | Full automated test execution log (15/15 passed in 2.13s, 477/477 regression passed) | DOCUMENTATION | **YES** |
| **30** | `backend/verify_member2_rigorous.py` | `verify_member2_rigorous.py` | Standalone CLI script testing live API credentials, failover, and PII masking | OPTIONAL | **YES** |
| **31** | `API.env` | `API.env` | Live development file containing active API credentials | CRITICAL | **DO NOT SHARE** |
| **32** | `backend/.env.local` | `.env.local` | Local developer environment configuration | SENSITIVE | **DO NOT SHARE** |
| **33** | `backend/cybershield.db` | `cybershield.db` | Local SQLite database containing historical development scan records | DATA STORE | **DO NOT SHARE** |
| **34** | `backend/venv/` | `venv/` (Folder) | Host-specific Python virtual environment binaries and site-packages | SYSTEM / BIN | **DO NOT SHARE** |
| **35** | `backend/**/__pycache__/` | `__pycache__/` | Compiled Python bytecode (`.pyc` files) | COMPILER CACHE | **DO NOT SHARE** |

---

## 2. Shareability Summary by Category

- **Total Files in Repository**: Entire full-stack project.
- **Files Selected for Handover Package**: **30 files** (15 Mandatory, 6 Supporting, 3 Testing, 5 Documentation, 1 Optional).
- **Files Strictly Excluded (DO NOT SHARE)**: **5 categories** (`API.env`, `.env.local`, SQLite databases, `.venv/`, `__pycache__/`).
- **Folders That Can Be Transferred as Whole Units**:
  1. `backend/app/services/ai_engine/` (7 files)
  2. `backend/app/services/file_security/` (6 files)
