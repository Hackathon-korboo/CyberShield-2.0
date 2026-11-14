"""CyberShield AI 2.0 — File Security Schemas
Member 2: Antivirus-Style Static File Threat Analysis Models.

Strictly non-executing static analysis schemas.
Guarantees clean separation between observed evidence, static risk scoring,
and AI-assisted contextual interpretation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FileRiskLevel(str, Enum):
    SAFE = "Safe"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class FileThreatCategory(str, Enum):
    CLEAN = "Clean"
    KNOWN_MALWARE = "Known Malware"
    EXTENSION_SPOOFING = "Extension Spoofing"
    SUSPICIOUS_EXECUTABLE = "Suspicious Executable"
    MALICIOUS_SCRIPT = "Malicious Script"
    OFFICE_MACRO = "Office Macro / OLE Vulnerability"
    ARCHIVE_PATH_TRAVERSAL = "Archive Path Traversal (Zip Slip)"
    ARCHIVE_DECOMPRESSION_BOMB = "Decompression Bomb (Zip Bomb)"
    ARCHIVE_EMBEDDED_EXECUTABLE = "Archive Embedded Executable"
    OBFUSCATED_PAYLOAD = "Obfuscated / Encoded Payload"
    SUSPICIOUS_STRINGS = "Suspicious System / Network Strings"
    OVERSIZED_OR_MALFORMED = "Oversized or Malformed File"
    UNKNOWN = "Unknown"


class FileIndicator(BaseModel):
    category: FileThreatCategory = Field(..., description="Classification category of the indicator")
    severity: str = Field(..., description="Severity level: Info, Low, Medium, High, Critical")
    description: str = Field(..., description="Detailed explanation of the technical indicator")
    verbatim_evidence: str = Field(..., description="Verbatim observed evidence (magic bytes, string, entry, or hash)")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence in the detected indicator")


class FileHashMetadata(BaseModel):
    md5: str = Field(..., description="MD5 cryptographic hash")
    sha1: str = Field(..., description="SHA-1 cryptographic hash")
    sha256: str = Field(..., description="SHA-256 cryptographic hash")
    sha512: Optional[str] = Field(default=None, description="SHA-512 cryptographic hash")


class FileSignatureCheckResult(BaseModel):
    detected_mime: str = Field(..., description="Detected MIME type based on magic bytes inspection")
    detected_format: str = Field(..., description="Identified file format / container")
    reported_extension: str = Field(..., description="Extension reported in filename")
    is_extension_mismatch: bool = Field(default=False, description="Whether the file extension does not match magic bytes")
    is_executable: bool = Field(default=False, description="Whether the file contains executable binary headers")
    is_script: bool = Field(default=False, description="Whether the file contains script interpreters/shebangs")
    is_macro_enabled: bool = Field(default=False, description="Whether the document contains embedded VBA/OLE macros")
    magic_hex: str = Field(..., description="Leading header bytes formatted as hexadecimal")
    details: str = Field(..., description="Technical summary of signature analysis")


class ArchiveInspectionResult(BaseModel):
    is_archive: bool = Field(default=False, description="Whether the file is an archive (.zip, .tar, etc.)")
    total_entries: int = Field(default=0, description="Total number of files/entries in the archive")
    total_uncompressed_bytes: int = Field(default=0, description="Calculated total uncompressed size in bytes")
    compression_ratio: float = Field(default=1.0, description="Ratio of uncompressed size to compressed file size")
    has_path_traversal: bool = Field(default=False, description="Detected zip slip / path traversal entries ('../')")
    traversal_entries: List[str] = Field(default_factory=list, description="List of entries containing path traversal")
    is_decompression_bomb: bool = Field(default=False, description="Whether the archive exceeds safe compression limits")
    embedded_executables: List[str] = Field(default_factory=list, description="List of executable files embedded inside archive")
    inspected_safely_without_extraction: bool = Field(
        default=True,
        description="Confirms archive was inspected purely via central directory metadata without disk extraction"
    )


class MalwareMatchResult(BaseModel):
    is_matched: bool = Field(default=False, description="Whether file hash matched known malware database")
    threat_family: Optional[str] = Field(default=None, description="Known threat family if matched (e.g. EICAR, WannaCry)")
    malware_type: Optional[str] = Field(default=None, description="Classification (Ransomware, Trojan, Botnet, Test)")
    matched_hash_type: Optional[str] = Field(default=None, description="Which hash matched (sha256, md5, sha1)")
    description: Optional[str] = Field(default=None, description="Reference information about the identified threat")


class FileThreatAnalysisResponse(BaseModel):
    analysis_type: str = Field(
        default="Static File Threat Analysis (Non-Execution / Static Inspection Only)",
        description="Explicit notice confirming file was never executed or evaluated dynamically"
    )
    filename: str = Field(..., description="Sanitized original filename")
    file_size_bytes: int = Field(..., description="File size in bytes")
    hashes: FileHashMetadata = Field(..., description="Cryptographic fingerprints")
    risk_level: FileRiskLevel = Field(..., description="Overall static risk classification")
    risk_score: int = Field(..., ge=0, le=100, description="Deterministic risk score from 0 (Clean) to 100 (Critical)")
    signature_analysis: FileSignatureCheckResult = Field(..., description="Magic byte signature inspection details")
    archive_analysis: Optional[ArchiveInspectionResult] = Field(default=None, description="Archive inspection if applicable")
    malware_match: MalwareMatchResult = Field(..., description="Hash matching against known malware database")
    indicators: List[FileIndicator] = Field(default_factory=list, description="Detailed technical threat indicators")
    evidence: List[str] = Field(default_factory=list, description="Verbatim observed evidence strings and flags")
    summary: str = Field(..., description="Human-readable static threat summary")
    ai_contextual_explanation: Optional[str] = Field(
        default=None,
        description="Gemini-generated contextual explanation based strictly on sanitized technical metadata"
    )
    recommendations: List[str] = Field(default_factory=list, description="Actionable mitigation and remediation steps")
    engine: str = Field(..., description="Engine identifier and provider chain")
    analyzed_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of analysis completion")
