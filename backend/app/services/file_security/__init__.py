"""CyberShield AI 2.0 — File Security Module
Member 2: Antivirus-Style Static File Threat Analysis and Gemini Explainer.
"""

from app.services.file_security.archive_safety_guard import ArchiveSafetyGuard
from app.services.file_security.file_signature_checker import FileSignatureChecker
from app.services.file_security.file_threat_analyzer import FileThreatAnalyzer
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

__all__ = [
    "ArchiveInspectionResult",
    "ArchiveSafetyGuard",
    "FileHashMetadata",
    "FileIndicator",
    "FileRiskLevel",
    "FileSignatureChecker",
    "FileSignatureCheckResult",
    "FileThreatAnalysisResponse",
    "FileThreatAnalyzer",
    "FileThreatCategory",
    "MalwareHashMatcher",
    "MalwareMatchResult",
]
