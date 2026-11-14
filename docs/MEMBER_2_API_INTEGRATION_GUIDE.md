# CYBERSHIELD AI 2.0 — MEMBER 2 API INTEGRATION GUIDE
## Python Service Interfaces, REST Contracts, Schemas & Integration Code

**Author:** Senior Software Integration Engineer (Member 2)  
**Target Recipient:** Backend API & Integration Engineer (Member 1)  
**Date:** November 14, 2026  
**Implementation Directory:** `backend/app/services/`

---

## 1. Executive Summary for Member 1

This guide explains how to integrate Member 2's **AI Scam Intelligence Engine** and **Antivirus-Style Static File Security Subsystem** into your backend routes, database persistence pipeline, and error handling framework.

All interfaces documented here are extracted directly from the actual, working production codebase.

---

## 2. Python Service Interfaces & Signatures

### 2.1 High-Level Message Analyzer Service
Located at `backend/app/services/message_analyzer.py`:

```python
class MessageAnalyzerService:
    @classmethod
    async def analyze_message(
        cls, 
        content: str, 
        message_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main analysis method invoked by API routes.
        
        Performs:
        1. Privacy-preserving PII redaction (PAN, Aadhaar, Phone, Card, Email).
        2. Adversarial prompt injection boundary isolation.
        3. Multi-tier LLM reasoning (Gemini -> Groq -> OpenAI -> Heuristics).
        4. Verbatim evidence grounding via EvidenceValidator.
        5. Lossless local token restoration for authorized display.
        
        Returns:
            Dictionary mapped directly into the format required by
            Member 1's ScanDetailResponse and database models:
            {
                "risk_level": "Critical" | "High" | "Medium" | "Low",
                "risk_score": int (0-100),
                "summary": str,
                "evidence": List[str],
                "recommendations": List[str],
                "message_indicators": List[MessageIndicator],
                "engine": str,
                "pii_redacted": bool,
                "redactions_count": int,
                "entity_counts": Dict[str, int]
            }
        """
```

### 2.2 Low-Level Scam Message Analyzer
Located at `backend/app/services/ai_engine/scam_analyzer.py`:

```python
class ScamMessageAnalyzer:
    async def analyze(
        self, 
        request: AnalyzeMessageRequest
    ) -> Tuple[AnalyzeMessageResponse, str]:
        """
        Direct Member 2 engine method.
        
        Args:
            request: AnalyzeMessageRequest(message=str, message_type=MessageTypeEnum)
            
        Returns:
            Tuple of (AnalyzeMessageResponse, engine_identifier_str)
        """
```

### 2.3 Antivirus-Style Static File Threat Analyzer
Located at `backend/app/services/file_security/file_threat_analyzer.py`:

```python
class FileThreatAnalyzer:
    @classmethod
    def scan_file_bytes(
        cls,
        file_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None
    ) -> FileThreatAnalysisResponse:
        """
        Executes strictly non-executing static file threat inspection.
        
        Performs:
        1. Size boundary validation (max 25 MB; rejects 0 bytes).
        2. Cryptographic hashing (MD5, SHA-1, SHA-256, SHA-512).
        3. Magic byte signature inspection vs reported extension (catches extension spoofing).
        4. Non-extracting archive inspection (Zip Slip traversal & Zip Bomb mitigation).
        5. O(1) hash matching against verified malware signatures (EICAR, WannaCry, Emotet, Locky, Mirai).
        6. Printable string heuristic inspection (PowerShell -enc, certutil, reverse shells).
        7. Deterministic risk scoring (0 to 100) and risk classification.
        
        Returns:
            Complete FileThreatAnalysisResponse Pydantic model.
        """

    @classmethod
    async def explain_threat_with_gemini(
        cls,
        analysis: FileThreatAnalysisResponse
    ) -> str:
        """
        Generates contextual threat explanations and containment advice via Google Gemini.
        
        PRIVACY GUARANTEE:
        Sends ONLY sanitized metadata (filename, size, SHA-256, detected flags).
        NEVER transmits raw file bytes or sensitive file content.
        
        Returns:
            Contextual explanation string with fallback to offline heuristics if Gemini is offline.
        """
```

### 2.4 Privacy Redaction Engine
Located at `backend/app/services/nexus/pii_redactor.py`:

```python
class PIIRedactor:
    @classmethod
    def redact(cls, text: str) -> RedactionResult:
        """
        Replaces PAN, Aadhaar, payment cards, phone numbers, and emails
        with opaque tokens: [REDACTED_ID_1], [REDACTED_ACCOUNT_1], etc.
        Maintains local_mapping dictionary in memory for reversible restoration.
        """

    @classmethod
    def restore_evidence(cls, evidence: str, local_mapping: Dict[str, str]) -> str:
        """Restores redacted placeholders in evidence strings for local authorized display."""
```

---

## 3. REST API Contracts & Endpoint Implementations

### Endpoint 1: Master Message Scan
- **Route**: `POST /api/v1/scans/message`
- **Request Body**:
  ```json
  {
    "content": "Dear Customer, your bank account access has been suspended. Please share your 6-digit OTP to unlock: http://secure-login.tk/auth"
  }
  ```
- **Response Structure (`ScanDetailResponse`)**:
  ```json
  {
    "scan_id": "scan_msg_01JAX123...",
    "scan_type": "message",
    "target": "Dear Customer, your bank account access has been suspended...",
    "status": "completed",
    "risk_level": "Critical",
    "risk_score": 88,
    "created_at": "2026-11-14T09:30:00Z",
    "providers_checked": [],
    "report": {
      "report_id": "rep_01JAX123...",
      "summary": "CRITICAL THREAT: Solicits sensitive authentication codes (OTP) and manufactures account suspension fear.",
      "evidence": [
        "Please share your 6-digit OTP",
        "account access has been suspended"
      ],
      "recommendations": [
        "Never disclose one-time passwords (OTPs) or banking credentials over email or SMS.",
        "Block the sender number and report this message to the national cybercrime portal."
      ],
      "report_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "verification_status": "locally_hashed",
      "blockchain_tx": null,
      "created_at": "2026-11-14T09:30:00Z"
    },
    "events": [
      {
        "event_type": "text_analysis",
        "description": "Message processed using engine 'gemini-1.5-flash' with 2 threat indicators.",
        "created_at": "2026-11-14T09:30:00Z"
      }
    ],
    "message_indicators": [
      {
        "category": "possible_credential_theft",
        "severity": "Critical",
        "description": "Demands one-time password (OTP) or authentication security code, a primary vector for account takeover."
      }
    ],
    "analysis_engine": "gemini-1.5-flash"
  }
  ```

---

### Endpoint 2: Antivirus-Style Static File Scan (Master Contract)
- **Route**: `POST /api/v1/scans/file`
- **Content-Type**: `multipart/form-data`
- **Request**: `file: UploadFile`
- **Response Structure (`ScanDetailResponse`)**:
  ```json
  {
    "scan_id": "scan_file_01JAX456...",
    "scan_type": "file",
    "target": "Quarterly_Earnings.pdf",
    "status": "completed",
    "risk_level": "Critical",
    "risk_score": 95,
    "created_at": "2026-11-14T09:35:00Z",
    "providers_checked": [],
    "report": {
      "report_id": "rep_01JAX456...",
      "summary": "CRITICAL EVASION: File 'Quarterly_Earnings.pdf' exhibits extension masquerading. Reported extension '.pdf' obscures an internal 'Windows PE/COFF Executable or DLL (MZ header)'.",
      "evidence": [
        "Extension Mismatch: reported '.pdf' != detected 'Windows PE/COFF Executable or DLL (MZ header)'",
        "Binary Executable Format: Windows PE/COFF Executable or DLL (MZ header)"
      ],
      "recommendations": [
        "STATIC INSPECTION ONLY: This file was not executed. Never execute unknown files in production environments.",
        "Quarantine or permanently delete this file immediately; do not open or double-click.",
        "Block this file's SHA-256 hash across endpoint detection (EDR) and gateway firewalls."
      ],
      "report_hash": "a1b2c3d4e5f6...",
      "verification_status": "locally_hashed",
      "blockchain_tx": null,
      "created_at": "2026-11-14T09:35:00Z"
    },
    "events": [
      {
        "event_type": "file_static_analysis",
        "description": "Static inspection of 'Quarterly_Earnings.pdf' (142050 bytes). Format: Windows PE/COFF Executable or DLL (MZ header). SHA-256: 3a6a9b4d8124b81c...",
        "created_at": "2026-11-14T09:35:00Z"
      }
    ],
    "message_indicators": [
      {
        "category": "Extension Spoofing",
        "severity": "Critical",
        "description": "Extension spoofing detected: File named 'Quarterly_Earnings.pdf' has extension '.pdf' but contains Windows PE/COFF Executable or DLL (MZ header)."
      }
    ],
    "analysis_engine": "CyberShield-Static-AV-v2.0"
  }
  ```

---

### Endpoint 3: Direct File Analysis (Member 2 Contract)
- **Route**: `POST /api/v1/analyze-file`
- **Content-Type**: `multipart/form-data`
- **Request**: `file: UploadFile`
- **Response Structure (`FileThreatAnalysisResponse`)**:
  ```json
  {
    "analysis_type": "Static File Threat Analysis (Non-Execution / Static Inspection Only)",
    "filename": "eicar_test.com",
    "file_size_bytes": 68,
    "hashes": {
      "md5": "c637d527c86186464879dc45e7816c53",
      "sha1": "3395856ce81f2b7382dee72602f798b642f14140",
      "sha256": "13db60afb914a2ee9b3649d1947d58046d1a9e9b8e4114d80b1d5c142b4ed7fa",
      "sha512": "..."
    },
    "risk_level": "Critical",
    "risk_score": 100,
    "signature_analysis": {
      "detected_mime": "application/octet-stream",
      "detected_format": "Unknown Binary or Generic Data",
      "reported_extension": ".com",
      "is_extension_mismatch": false,
      "is_executable": false,
      "is_script": false,
      "is_macro_enabled": false,
      "magic_hex": "58 35 4F 21 50 25 40 41 50 5B 34 5C 50 5A 58 35",
      "details": "Dangerous executable file extension '.com' detected on host system."
    },
    "archive_analysis": null,
    "malware_match": {
      "is_matched": true,
      "threat_family": "EICAR-Standard-AV-Test-File",
      "malware_type": "Test Signature",
      "matched_hash_type": "sha256",
      "description": "Standard European Institute for Computer Antivirus Research harmless test signature."
    },
    "indicators": [
      {
        "category": "Known Malware",
        "severity": "Critical",
        "description": "Cryptographic hash matched verified malicious signature: EICAR-Standard-AV-Test-File (Test Signature)",
        "verbatim_evidence": "Matched SHA256: 13db60afb914a2ee9b3649d1947d58046d1a9e9b8e4114d80b1d5c142b4ed7fa",
        "confidence": 1.0
      }
    ],
    "evidence": [
      "Hash Match: EICAR-Standard-AV-Test-File [SHA256]"
    ],
    "summary": "CRITICAL THREAT: File 'eicar_test.com' matched known malware signature 'EICAR-Standard-AV-Test-File' (Test Signature).",
    "ai_contextual_explanation": "[GEMINI Contextual Assessment]\nThis file matches the standard EICAR antivirus test signature...",
    "recommendations": [
      "STATIC INSPECTION ONLY: This file was not executed. Never execute unknown files in production environments.",
      "Quarantine or permanently delete this file immediately; do not open or double-click."
    ],
    "engine": "CyberShield-Static-AV-v2.0",
    "analyzed_at": "2026-11-14T09:35:00Z"
  }
  ```

---

## 4. How Member 1 Should Integrate the Endpoints

In `backend/app/api/v1/router.py`:
1. **Import the Services & Schemas**:
   ```python
   from fastapi import File, UploadFile
   from app.services.file_security import FileThreatAnalyzer, FileThreatAnalysisResponse
   from app.services.message_analyzer import MessageAnalyzerService
   ```

2. **Add the Endpoint Decorators**:
   Member 1 can simply keep the implementations provided in `backend/app/api/v1/router.py` lines 730–950, which already handle:
   - File size validation (`len(contents) == 0` $\rightarrow$ 400 Bad Request, `> 25MB` $\rightarrow$ 413 Payload Too Large).
   - Dynamic hashing and static analysis.
   - Database record creation (`Scan`, `ScanEvent`, `RiskReport`).
   - Cryptographic canonical report hashing via `ReportVerifier`.
   - Threat Relationship Graph ingestion via `ThreatGraphService`.

3. **Database Schema Compatibility**:
   Member 2's implementation reuses the existing `Scan` and `RiskReport` SQLAlchemy models:
   - `scan_type` set to `"file"` or `"message"`.
   - `target` stores filename or first 100 characters of the message.
   - `evidence` and `recommendations` stored as JSON text strings in `RiskReport`.
   - **Zero database migrations or schema alterations required**.
