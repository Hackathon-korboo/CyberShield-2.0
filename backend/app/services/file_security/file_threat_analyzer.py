"""CyberShield AI 2.0 — Static File Threat Analyzer
Member 2: Antivirus-style static inspection engine with Gemini contextual explanation.

Strict Guarantees:
- Strictly static inspection (NEVER executes files or evaluates dynamic code).
- Zero raw bytes or sensitive payloads transmitted to LLMs (Sanitized Metadata Only).
- Evidence-grounded scoring based on verified magic bytes, hash signatures, and archive structure.
- Multi-tier AI explanation with deterministic offline fallback.
"""

import hashlib
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from app.core.config import settings
from app.services.ai_engine.llm_client import LLMClient
from app.services.file_security.archive_safety_guard import ArchiveSafetyGuard
from app.services.file_security.file_signature_checker import FileSignatureChecker
from app.services.file_security.malware_hash_matcher import MalwareHashMatcher
from app.services.file_security.schemas import (
    ArchiveInspectionResult,
    FileHashMetadata,
    FileIndicator,
    FileRiskLevel,
    FileSignatureCheckResult,
    FileThreatAnalysisResponse,
    FileThreatCategory,
    MalwareMatchResult,
)

logger = logging.getLogger("cybershield.file_threat_analyzer")


class FileThreatAnalyzer:
    """Orchestrator for antivirus-style static file threat analysis."""

    MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB

    # Suspicious strings / API patterns in raw binaries or scripts
    SUSPICIOUS_STRINGS_PATTERNS = [
        (re.compile(r"(?i)\b(?:powershell(?:\.exe)?\s+-[eE](?:nc|ncodedcommand))\b"), "Encoded PowerShell Command Execution", FileThreatCategory.MALICIOUS_SCRIPT, "High"),
        (re.compile(r"(?i)\b(?:certutil(?:\.exe)?\s+-urlcache|-split\s+-f)\b"), "Certutil In-Memory Binary Download Technique", FileThreatCategory.MALICIOUS_SCRIPT, "High"),
        (re.compile(r"(?i)\b(?:bitsadmin(?:\.exe)?\s+/transfer)\b"), "BITSAdmin Background Binary Download Technique", FileThreatCategory.MALICIOUS_SCRIPT, "Medium"),
        (re.compile(r"(?i)\b(?:VirtualAlloc|WriteProcessMemory|CreateRemoteThread)\b"), "Process Injection Win32 API references", FileThreatCategory.SUSPICIOUS_STRINGS, "High"),
        (re.compile(r"(?i)\b(?:URLDownloadToFileA|InternetOpenUrlA)\b"), "Remote Download Win32 API references", FileThreatCategory.SUSPICIOUS_STRINGS, "Medium"),
        (re.compile(r"(?i)\b(?:IsDebuggerPresent|CheckRemoteDebuggerPresent)\b"), "Anti-Debugging Defense Evasion API references", FileThreatCategory.SUSPICIOUS_STRINGS, "Medium"),
        (re.compile(r"(?i)(?:your\s+files\s+(?:have\s+been|are)\s+encrypted|pay\s+(?:the\s+)?ransom|decrypt(?:or)?\s+tool)"), "Ransomware Extortion Note Patterns", FileThreatCategory.KNOWN_MALWARE, "Critical"),
        (re.compile(r"(?i)\b(?:bash\s+-i\s+>&|nc\s+-e\s+/bin/(?:ba)?sh|/dev/tcp/\d+\.\d+\.\d+\.\d+/\d+)"), "Unix Reverse Shell Command Construction", FileThreatCategory.MALICIOUS_SCRIPT, "Critical"),
    ]

    @classmethod
    def compute_hashes(cls, data: bytes) -> FileHashMetadata:
        """Compute MD5, SHA-1, SHA-256, and SHA-512 hashes in a single pass."""
        md5 = hashlib.md5(data).hexdigest()
        sha1 = hashlib.sha1(data).hexdigest()
        sha256 = hashlib.sha256(data).hexdigest()
        sha512 = hashlib.sha512(data).hexdigest()
        return FileHashMetadata(md5=md5, sha1=sha1, sha256=sha256, sha512=sha512)

    @classmethod
    def scan_file_bytes(
        cls,
        file_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None
    ) -> FileThreatAnalysisResponse:
        """
        Execute full static file inspection.
        Returns complete structured threat analysis with deterministic scoring.
        """
        file_size = len(file_bytes)
        sanitized_filename = os.path.basename(filename).strip() or "unnamed_upload"

        # 1. Validation checks
        if file_size == 0:
            return cls._build_malformed_response(
                sanitized_filename,
                "File is completely empty (0 bytes). Cannot perform static threat analysis."
            )

        if file_size > cls.MAX_FILE_SIZE_BYTES:
            return cls._build_malformed_response(
                sanitized_filename,
                f"File size ({file_size} bytes) exceeds maximum allowable limit of {cls.MAX_FILE_SIZE_BYTES} bytes (25 MB)."
            )

        # 2. Compute Hashes
        hashes = cls.compute_hashes(file_bytes)

        # 3. Magic Bytes & Signature Analysis
        header_sample = file_bytes[:1024]
        sig_result = FileSignatureChecker.check_signature(sanitized_filename, header_sample)

        # 4. Known Malware Hash Matching
        malware_match = MalwareHashMatcher.match(
            sha256=hashes.sha256,
            md5=hashes.md5,
            sha1=hashes.sha1
        )

        # 5. Archive Safety Inspection (if archive)
        archive_result: Optional[ArchiveInspectionResult] = None
        if (
            sig_result.detected_mime in {"application/zip", "application/gzip", "application/x-7z-compressed", "application/vnd.rar"}
            or sanitized_filename.lower().endswith((".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"))
        ):
            archive_result = ArchiveSafetyGuard.inspect(file_bytes, sanitized_filename)

        # 6. Static String & Heuristic Indicators (First 1MB printable strings)
        string_sample = file_bytes[:1024 * 1024].decode("latin-1", errors="ignore")
        indicators: List[FileIndicator] = []
        evidence_list: List[str] = []

        # Indicator A: Known Malware Hash Match
        if malware_match.is_matched:
            indicators.append(FileIndicator(
                category=FileThreatCategory.KNOWN_MALWARE,
                severity="Critical",
                description=f"Cryptographic hash matched verified malicious signature: {malware_match.threat_family} ({malware_match.malware_type})",
                verbatim_evidence=f"Matched {malware_match.matched_hash_type.upper()}: {getattr(hashes, malware_match.matched_hash_type)}",
                confidence=1.0,
            ))
            evidence_list.append(f"Hash Match: {malware_match.threat_family} [{malware_match.matched_hash_type.upper()}]")

        # Indicator B: Extension Spoofing / Mismatch
        if sig_result.is_extension_mismatch:
            indicators.append(FileIndicator(
                category=FileThreatCategory.EXTENSION_SPOOFING,
                severity="Critical",
                description=f"Extension spoofing detected: File named '{sanitized_filename}' has extension '{sig_result.reported_extension}' but contains {sig_result.detected_format}.",
                verbatim_evidence=f"Magic bytes: {sig_result.magic_hex[:23]} -> {sig_result.detected_mime}",
                confidence=0.98,
            ))
            evidence_list.append(f"Extension Mismatch: reported '{sig_result.reported_extension}' != detected '{sig_result.detected_format}'")

        # Indicator C: Executable File Detection
        if sig_result.is_executable:
            indicators.append(FileIndicator(
                category=FileThreatCategory.SUSPICIOUS_EXECUTABLE,
                severity="High",
                description=f"Binary executable headers identified: {sig_result.detected_format}",
                verbatim_evidence=f"Header signature: {sig_result.magic_hex[:11]}",
                confidence=0.95,
            ))
            evidence_list.append(f"Binary Executable Format: {sig_result.detected_format}")

        # Indicator D: Script Interpreter / Shebang Detection
        if sig_result.is_script:
            indicators.append(FileIndicator(
                category=FileThreatCategory.MALICIOUS_SCRIPT,
                severity="High" if sig_result.reported_extension in {".vbs", ".hta", ".ps1", ".bat"} else "Medium",
                description=f"Directly executable system script identified: {sig_result.detected_format}",
                verbatim_evidence=f"Script markers: {sig_result.details}",
                confidence=0.92,
            ))
            evidence_list.append(f"Script Payload: {sig_result.detected_format}")

        # Indicator E: Macro Enabled Document
        if sig_result.is_macro_enabled:
            indicators.append(FileIndicator(
                category=FileThreatCategory.OFFICE_MACRO,
                severity="High",
                description="Embedded VBA Macro code streams detected inside document structure.",
                verbatim_evidence="VBA Project / Macro signature in compound document header",
                confidence=0.90,
            ))
            evidence_list.append("Embedded VBA Project / Macro Stream Detected")

        # Indicator F: Archive Vulnerabilities (Zip Slip & Zip Bomb)
        if archive_result and archive_result.is_archive:
            if archive_result.has_path_traversal:
                indicators.append(FileIndicator(
                    category=FileThreatCategory.ARCHIVE_PATH_TRAVERSAL,
                    severity="Critical",
                    description=f"Archive contains {len(archive_result.traversal_entries)} path traversal entries ('../') attempting filesystem escape.",
                    verbatim_evidence=f"Traversal target: {archive_result.traversal_entries[0]}",
                    confidence=1.0,
                ))
                evidence_list.append(f"Zip Slip / Path Traversal: '{archive_result.traversal_entries[0]}'")

            if archive_result.is_decompression_bomb:
                indicators.append(FileIndicator(
                    category=FileThreatCategory.ARCHIVE_DECOMPRESSION_BOMB,
                    severity="High",
                    description=f"Archive violates safe decompression limits: compression ratio {archive_result.compression_ratio}:1, total uncompressed {archive_result.total_uncompressed_bytes} bytes.",
                    verbatim_evidence=f"Ratio: {archive_result.compression_ratio}:1 | Entries: {archive_result.total_entries}",
                    confidence=0.95,
                ))
                evidence_list.append(f"Decompression Bomb Risk: ratio {archive_result.compression_ratio}:1")

            if archive_result.embedded_executables:
                indicators.append(FileIndicator(
                    category=FileThreatCategory.ARCHIVE_EMBEDDED_EXECUTABLE,
                    severity="High",
                    description=f"Archive conceals {len(archive_result.embedded_executables)} executable payload(s) inside compressed container.",
                    verbatim_evidence=f"Embedded file: {archive_result.embedded_executables[0]}",
                    confidence=0.95,
                ))
                evidence_list.append(f"Embedded Executable in Archive: '{archive_result.embedded_executables[0]}'")

        # Indicator G: Suspicious API / String patterns
        for pattern, desc, cat, sev in cls.SUSPICIOUS_STRINGS_PATTERNS:
            match = pattern.search(string_sample)
            if match:
                matched_str = match.group(0)[:60]
                indicators.append(FileIndicator(
                    category=cat,
                    severity=sev,
                    description=f"{desc} identified in static string inspection.",
                    verbatim_evidence=f"Pattern: '{matched_str}'",
                    confidence=0.88,
                ))
                evidence_list.append(f"Static Pattern: {desc} ('{matched_str}')")

        # 7. Calculate Deterministic Risk Score (0 - 100)
        risk_score, risk_level = cls._calculate_risk_score(
            malware_match=malware_match,
            sig_result=sig_result,
            archive_result=archive_result,
            indicators=indicators,
        )

        # 8. Generate Summary & Recommendations
        summary = cls._generate_summary(
            filename=sanitized_filename,
            risk_level=risk_level,
            risk_score=risk_score,
            malware_match=malware_match,
            sig_result=sig_result,
            archive_result=archive_result,
            indicators=indicators,
        )

        recommendations = cls._generate_recommendations(
            risk_level=risk_level,
            malware_match=malware_match,
            sig_result=sig_result,
            archive_result=archive_result,
        )

        # Add signature evidence
        if not evidence_list:
            evidence_list.append(f"File Header: {sig_result.detected_format}")
            evidence_list.append(f"SHA-256 Fingerprint: {hashes.sha256[:16]}...")

        return FileThreatAnalysisResponse(
            analysis_type="Static File Threat Analysis (Non-Execution / Static Inspection Only)",
            filename=sanitized_filename,
            file_size_bytes=file_size,
            hashes=hashes,
            risk_level=risk_level,
            risk_score=risk_score,
            signature_analysis=sig_result,
            archive_analysis=archive_result,
            malware_match=malware_match,
            indicators=indicators,
            evidence=evidence_list,
            summary=summary,
            ai_contextual_explanation=None,  # Populated via async Gemini explainer
            recommendations=recommendations,
            engine="CyberShield-Static-AV-v2.0",
        )

    @classmethod
    async def explain_threat_with_gemini(
        cls,
        analysis: FileThreatAnalysisResponse
    ) -> str:
        """
        Generates a contextual threat explanation using Google Gemini (with multi-tier failover).
        PRIVACY GUARANTEE: Only sanitized metadata, cryptographic hashes, and indicator summaries
        are sent to Gemini. Raw binary data or file bytes are NEVER transmitted.
        """
        # Prepare sanitized metadata payload for LLM
        sanitized_metadata = {
            "filename": analysis.filename,
            "file_size_bytes": analysis.file_size_bytes,
            "sha256": analysis.hashes.sha256,
            "detected_mime": analysis.signature_analysis.detected_mime,
            "detected_format": analysis.signature_analysis.detected_format,
            "reported_extension": analysis.signature_analysis.reported_extension,
            "is_extension_mismatch": analysis.signature_analysis.is_extension_mismatch,
            "is_executable": analysis.signature_analysis.is_executable,
            "is_script": analysis.signature_analysis.is_script,
            "is_macro_enabled": analysis.signature_analysis.is_macro_enabled,
            "is_malware_hash_matched": analysis.malware_match.is_matched,
            "threat_family": analysis.malware_match.threat_family,
            "static_risk_score": analysis.risk_score,
            "static_risk_level": analysis.risk_level.value,
            "detected_threat_indicators": [
                {"category": ind.category.value, "severity": ind.severity, "description": ind.description}
                for ind in analysis.indicators
            ],
        }

        prompt = (
            "You are CyberShield AI's Senior Malware Analyst. Provide an evidence-grounded threat explanation "
            "for the following static file security report. Follow strict cybersecurity principles: "
            "1. Ground all claims solely in the provided technical metadata.\n"
            "2. Never claim dynamic execution behavior since this was a purely static analysis.\n"
            "3. Explain the security implications of any detected flags (e.g. extension spoofing, known hashes, embedded macros, archive vulnerabilities).\n"
            "4. Provide concise, actionable containment and remediation advice.\n\n"
            f"FILE_STATIC_METADATA_JSON:\n{json.dumps(sanitized_metadata, indent=2)}\n\n"
            "Provide your assessment in 2-3 concise paragraphs."
        )

        try:
            llm_client = LLMClient()
            response_text, provider = await llm_client.generate(prompt=prompt)
            if response_text and len(response_text.strip()) > 30:
                return f"[{provider.upper()} Contextual Assessment]\n{response_text.strip()}"
        except Exception as exc:
            logger.warning("Gemini file explanation failed (%s). Using deterministic heuristic explanation.", str(exc))

        # Deterministic offline contextual explanation fallback
        return cls._generate_offline_explanation(analysis)

    @classmethod
    def _calculate_risk_score(
        cls,
        malware_match: MalwareMatchResult,
        sig_result: FileSignatureCheckResult,
        archive_result: Optional[ArchiveInspectionResult],
        indicators: List[FileIndicator],
    ) -> Tuple[int, FileRiskLevel]:
        """Calculates quantitative risk score (0-100) and discrete risk level."""
        # 1. Known malware hash match -> Immediate 100 Critical
        if malware_match.is_matched:
            return 100, FileRiskLevel.CRITICAL

        # 2. Extension spoofing (PE or ELF disguised as doc/image) -> Critical
        if sig_result.is_extension_mismatch and sig_result.is_executable:
            return 95, FileRiskLevel.CRITICAL

        # 3. Archive Zip Slip / Path Traversal -> Critical
        if archive_result and archive_result.has_path_traversal:
            return 92, FileRiskLevel.CRITICAL

        # 4. Decompression Bomb -> High
        if archive_result and archive_result.is_decompression_bomb:
            return 85, FileRiskLevel.HIGH

        # 5. Archive with embedded executables -> High
        if archive_result and archive_result.embedded_executables:
            return 80, FileRiskLevel.HIGH

        # 6. Binary executable files -> High
        if sig_result.is_executable:
            return 75, FileRiskLevel.HIGH

        # 7. Script files (.vbs, .ps1, .bat) -> Medium to High
        if sig_result.is_script:
            if sig_result.reported_extension in {".vbs", ".hta", ".ps1", ".bat"}:
                return 70, FileRiskLevel.HIGH
            return 55, FileRiskLevel.MEDIUM

        # 8. Macro enabled documents -> Medium
        if sig_result.is_macro_enabled:
            return 65, FileRiskLevel.MEDIUM

        # 9. Dangerous extension alone without recognized binary header
        if sig_result.reported_extension in FileSignatureChecker.DANGEROUS_EXECUTABLE_EXTENSIONS:
            return 60, FileRiskLevel.MEDIUM

        # 10. Suspicious static strings detected
        if indicators:
            max_sev = max(ind.severity for ind in indicators)
            if max_sev == "Critical":
                return 88, FileRiskLevel.CRITICAL
            if max_sev == "High":
                return 65, FileRiskLevel.MEDIUM
            return 40, FileRiskLevel.LOW

        # Clean file
        return 5, FileRiskLevel.SAFE

    @classmethod
    def _generate_summary(
        cls,
        filename: str,
        risk_level: FileRiskLevel,
        risk_score: int,
        malware_match: MalwareMatchResult,
        sig_result: FileSignatureCheckResult,
        archive_result: Optional[ArchiveInspectionResult],
        indicators: List[FileIndicator],
    ) -> str:
        """Constructs human-readable technical summary."""
        if malware_match.is_matched:
            return (
                f"CRITICAL THREAT: File '{filename}' matched known malware signature '{malware_match.threat_family}' "
                f"({malware_match.malware_type}). Cryptographic fingerprint matches verified malicious database."
            )

        if sig_result.is_extension_mismatch:
            return (
                f"CRITICAL EVASION: File '{filename}' exhibits extension masquerading. Reported extension "
                f"'{sig_result.reported_extension}' obscures an internal '{sig_result.detected_format}'."
            )

        if archive_result and archive_result.has_path_traversal:
            return (
                f"CRITICAL VULNERABILITY: Archive '{filename}' contains Zip Slip / Path Traversal entries "
                f"attempting to overwrite arbitrary system files outside extraction directory."
            )

        if archive_result and archive_result.is_decompression_bomb:
            return (
                f"HIGH THREAT: Archive '{filename}' exhibits decompression bomb characteristics with an abnormal "
                f"compression ratio of {archive_result.compression_ratio}:1, posing denial-of-service risks."
            )

        if sig_result.is_executable:
            return (
                f"HIGH RISK: File '{filename}' is a compiled executable ({sig_result.detected_format}). "
                "Direct execution of untrusted binaries can lead to arbitrary code execution."
            )

        if sig_result.is_script:
            return (
                f"ELEVATED RISK: File '{filename}' is an executable script ({sig_result.detected_format}). "
                "Can invoke system shell commands and automated scripts."
            )

        if sig_result.is_macro_enabled:
            return (
                f"MEDIUM RISK: File '{filename}' contains embedded VBA macro streams, frequently leveraged "
                "in malicious Office document drop techniques."
            )

        return (
            f"CLEAN / BENIGN: File '{filename}' verified as legitimate '{sig_result.detected_format}'. "
            "No known malicious hashes, executable masquerades, or archive anomalies detected."
        )

    @classmethod
    def _generate_recommendations(
        cls,
        risk_level: FileRiskLevel,
        malware_match: MalwareMatchResult,
        sig_result: FileSignatureCheckResult,
        archive_result: Optional[ArchiveInspectionResult],
    ) -> List[str]:
        """Provides actionable, prioritized remediation guidance."""
        recs = [
            "STATIC INSPECTION ONLY: This file was not executed. Never execute unknown files in production environments."
        ]

        if risk_level in {FileRiskLevel.CRITICAL, FileRiskLevel.HIGH}:
            recs.append("Quarantine or permanently delete this file immediately; do not open or double-click.")
            recs.append("Block this file's SHA-256 hash across endpoint detection (EDR) and gateway firewalls.")

            if sig_result.is_extension_mismatch:
                recs.append("Alert the security team to social engineering / masquerading payload delivery.")
            if archive_result and archive_result.has_path_traversal:
                recs.append("Do NOT use standard archive extractors; path traversal entries will overwrite disk paths.")
            if archive_result and archive_result.is_decompression_bomb:
                recs.append("Discard archive to avoid disk space exhaustion and host denial-of-service.")
            if sig_result.is_macro_enabled:
                recs.append("Disable Office macro execution in Microsoft Office Trust Center.")
        elif risk_level == FileRiskLevel.MEDIUM:
            recs.append("Inspect file contents in an isolated sandbox before transferring to end users.")
            recs.append("Verify sender identity via out-of-band communication before running scripts.")
        else:
            recs.append("File exhibits standard structure for its format. Routine security precautions apply.")

        return recs

    @classmethod
    def _generate_offline_explanation(cls, analysis: FileThreatAnalysisResponse) -> str:
        """Deterministic offline threat narrative when LLM is unavailable."""
        return (
            f"[OFFLINE Threat Forensics Engine]\n"
            f"File '{analysis.filename}' ({analysis.file_size_bytes} bytes) was evaluated using pure static heuristics. "
            f"Risk Level: {analysis.risk_level.value} (Score: {analysis.risk_score}/100).\n"
            f"Identified format: {analysis.signature_analysis.detected_format}. "
            f"Observed technical flags: {len(analysis.indicators)} indicator(s) logged. "
            f"Zero dynamic execution was performed during this security audit."
        )

    @classmethod
    def _build_malformed_response(cls, filename: str, reason: str) -> FileThreatAnalysisResponse:
        """Constructs safe error response for malformed or oversized uploads."""
        hashes = FileHashMetadata(
            md5="0" * 32,
            sha1="0" * 40,
            sha256="0" * 64,
            sha512=None
        )
        sig = FileSignatureCheckResult(
            detected_mime="application/x-unknown",
            detected_format="Malformed or Rejected File",
            reported_extension=os.path.splitext(filename)[1] or "(None)",
            is_extension_mismatch=False,
            is_executable=False,
            is_script=False,
            is_macro_enabled=False,
            magic_hex="(None)",
            details=reason,
        )
        return FileThreatAnalysisResponse(
            analysis_type="Static File Threat Analysis (Non-Execution / Static Inspection Only)",
            filename=filename,
            file_size_bytes=0,
            hashes=hashes,
            risk_level=FileRiskLevel.HIGH,
            risk_score=75,
            signature_analysis=sig,
            archive_analysis=None,
            malware_match=MalwareMatchResult(is_matched=False),
            indicators=[
                FileIndicator(
                    category=FileThreatCategory.OVERSIZED_OR_MALFORMED,
                    severity="High",
                    description=reason,
                    verbatim_evidence=reason,
                    confidence=1.0,
                )
            ],
            evidence=[reason],
            summary=f"REJECTED FILE: {reason}",
            ai_contextual_explanation=f"[Static Guard Notice] File upload could not be processed: {reason}",
            recommendations=[
                "Upload valid, non-empty files within the 25 MB boundary.",
                "Ensure archive containers are not truncated or corrupt.",
            ],
            engine="CyberShield-Static-AV-v2.0",
        )
