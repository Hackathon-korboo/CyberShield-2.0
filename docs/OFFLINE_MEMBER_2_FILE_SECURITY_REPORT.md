# CYBERSHIELD AI 2.0 — OFFLINE HACKATHON FILE SECURITY REPORT
## Member 2: Antivirus-Style Static File Threat Analysis & Archive Vulnerability Guard

**Author:** Senior AI Cybersecurity Engineer (Member 2)  
**Hackathon Track:** Cybersecurity & Digital Trust  
**Date:** November 14, 2026  
**Implementation Directory:** `D:\My Created Projects\adamus hackathon\backend\app\services\file_security`

---

## 1. System Objective & Operational Paradigm

The **Antivirus-Style Static File Threat Analyzer** is an offline security component introduced in CyberShield AI 2.0 to protect against malicious file payloads, weaponized documents, and disguised executables.

### Inviolable Static Analysis Guarantee
```
┌────────────────────────────────────────────────────────────────────────┐
│                        CRITICAL SECURITY NOTICE                        │
│                                                                        │
│   Analysis Type: Static File Threat Analysis (Non-Execution Only)      │
│   Target files are NEVER executed, NEVER launched in subprocesses,     │
│   and NEVER evaluated dynamically. All assessments are performed       │
│   strictly via header byte inspection, archive metadata parsing,       │
│   and cryptographic fingerprint matching.                             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technical Inspection Pipeline

The static inspection engine evaluates uploaded files (up to 25 MB) through 5 sequential forensic gates:

```
[Uploaded File Stream]
         │
         ▼
[Gate 1: Boundary & Hash Gate]
  ├─ Validates size > 0 and <= 25 MB
  └─ Streams MD5, SHA-1, SHA-256, SHA-512
         │
         ▼
[Gate 2: Signature & Magic Byte Gate]
  ├─ Inspects first 1024 bytes (MZ, ELF, Mach-O, PDF, PK-ZIP, OLE, RTF)
  ├─ Compares header magic bytes against reported file extension
  └─ Flags Extension Masquerading (e.g. executable disguised as .pdf)
         │
         ▼
[Gate 3: Malware Hash Matching Gate]
  ├─ O(1) memory lookup against verified malware database
  └─ Matches EICAR, WannaCry, Emotet, Locky, Mirai, AgentTesla
         │
         ▼
[Gate 4: Archive Safety Gate (If Container)]
  ├─ Reads ZIP central directory / TAR headers (Zero extraction)
  ├─ Mitigates Zip Slip / Path Traversal ('../' escaping)
  ├─ Enforces Decompression Bomb thresholds (100:1 ratio, 50MB, 250 files)
  └─ Detects embedded executables (.exe, .scr, .bat, .ps1)
         │
         ▼
[Gate 5: Static String & Heuristic Gate]
  ├─ Scans printable strings (First 1MB)
  ├─ Identifies encoded PowerShell (`-enc`), certutil, bitsadmin
  └─ Detects process injection Win32 APIs & ransomware note patterns
         │
         ▼
[Deterministic Risk Scoring & Gemini Contextual Explanation]
```

---

## 3. Forensic Modules & Threat Detection Algorithms

### 3.1 Magic Bytes & Extension Spoofing (`file_signature_checker.py`)
- **Pure Python Header Inspection**: Eliminates external native C library dependencies (`libmagic` / Windows DLL issues), providing 100% portable inspection across Windows 11, Linux, and macOS.
- **Recognized Formats**:
  - `MZ` (`4D 5A`): Windows PE Executable, DLL, Screensaver (`.exe`, `.dll`, `.scr`, `.sys`, `.cpl`).
  - `\x7fELF` (`7F 45 4C 46`): Unix/Linux Executable and Linkable Format binary.
  - `\xfe\xed\xfa\xce` / `\xca\xfe\xba\xbe`: Apple Mach-O binary and Java universal class.
  - `%PDF-` (`25 50 44 46`): Adobe Portable Document Format.
  - `PK\x03\x04` (`50 4B 03 04`): PK-ZIP Compressed Archive and modern OOXML documents (`.docx`, `.xlsx`).
  - `\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1`: Legacy Microsoft Compound File Binary (OLE).
- **Extension Spoofing Detection**:
  - A file named `Quarterly_Report.pdf` containing an `MZ` header is flagged with **Critical Extension Spoofing** (Score: 95/100).
  - Double extension masquerades (`invoice.pdf.exe`) are detected and isolated.
- **Embedded Macro Detection**: Scans OLE structures for active VBA project streams (`_VBA_PROJECT`, `Macros`).

### 3.2 Non-Extracting Archive Safety Guard (`archive_safety_guard.py`)
Standard archive extraction tools are vulnerable to directory traversal and denial-of-service. CyberShield's `ArchiveSafetyGuard` guarantees:
1. **Zero-Disk Extraction**: Inspects archive headers purely in memory via Python's `zipfile` and `tarfile` metadata interfaces.
2. **Path Traversal / Zip Slip Defense**:
   - Inspects entry paths for `../`, `..\\`, absolute paths (`/etc/passwd`, `C:\Windows\System32`), and null byte poisons (`\x00`).
   - If detected, flags the archive as **Critical Risk (Score: 92/100)** and prevents unpacking.
3. **Decompression Bomb Mitigation**:
   - Computes uncompressed-to-compressed ratio: if $> 100:1$, flags as a potential decompression bomb.
   - Restricts total uncompressed size to **50 MB** and total entry count to **250 entries**.
4. **Embedded Executable Inspection**:
   - Recursively inspects entry filenames for concealed dangerous extensions (`.exe`, `.scr`, `.bat`, `.cmd`, `.ps1`, `.vbs`, `.hta`, `.cpl`, `.msi`).

### 3.3 Malware Hash Matcher (`malware_hash_matcher.py`)
Computes four standard cryptographic hashes: MD5, SHA-1, SHA-256, and SHA-512. The engine performs $O(1)$ lookups against verified signatures:

| Threat Family | Malware Classification | Sample Hash (SHA-256) | Detection Action |
| :--- | :--- | :--- | :--- |
| **EICAR-Standard-AV-Test-File** | Universal AV Test Signature | `13db60afb914a2ee9b3649d1...` | Immediate 100 Critical |
| **Ransomware.WannaCry** | SMBv1 Worm & Ransomware | `ed01ebfbc9eb5bbea545af4d...` | Immediate 100 Critical |
| **Trojan.Emotet.Heur** | Banking Trojan & Dropper | `a935be9deca7a1c73ec56a47...` | Immediate 100 Critical |
| **Ransomware.Locky** | Extortion Ransomware | `8c2579dfdd1844b256bc6be8...` | Immediate 100 Critical |
| **Botnet.Mirai.LinuxELF** | IoT / Linux Botnet | `e0a3597c23bc9ee492df823d...` | Immediate 100 Critical |
| **Spyware.AgentTesla** | Credential Stealer & RAT | `b9a3b6d51bb4c4f346b3f71d...` | Immediate 100 Critical |

---

## 4. Deterministic Risk Scoring Formula

The static risk score is calculated deterministically on a $0 - 100$ scale:
$$\text{Score} = \max(\text{Rule Penalties}) + \text{Evidence Weights} - \text{Legitimacy Credits}$$

| Condition | Calibrated Score | Discrete Risk Level |
| :--- | :--- | :--- |
| **Known Malware Hash Matched** | **100** | **Critical** |
| **Extension Spoofing (PE in .pdf/.jpg)** | **95** | **Critical** |
| **Archive Zip Slip / Path Traversal** | **92** | **Critical** |
| **Archive Decompression Bomb** | **85** | **High** |
| **Archive Concealing Executable** | **80** | **High** |
| **Compiled Binary Header (MZ / ELF)** | **75** | **High** |
| **Script Payload (.vbs, .hta, .ps1)** | **70** | **High** |
| **Embedded Macro Document (.docm)** | **65** | **Medium** |
| **Clean Benign Document / Image** | **5** | **Safe** |

---

## 5. Explicit Limitations & Boundaries

To adhere to scientific rigor and ethical cybersecurity standards:
1. **Static vs. Dynamic Execution**: Static analysis cannot observe runtime behavioral indicators (e.g. memory injection during execution, dynamic command-and-control beacons, runtime API unhooking).
2. **Encrypted Archives**: Archives protected by strong AES passwords cannot have their internal file contents inspected without the decryption key; the container itself is flagged with an informational advisory.
3. **Advanced Polymorphic Payloads**: Heavily packed or mutated zero-day binaries may bypass static hash lookups, requiring correlation with Stage 3 URL/domain threat intelligence.
