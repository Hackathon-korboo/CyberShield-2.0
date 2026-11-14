"""CyberShield AI 2.0 — Archive Safety Guard
Member 2: Non-extracting static archive vulnerability inspector.

Features:
- Pure metadata inspection (NEVER extracts files to disk).
- Path Traversal / Zip Slip defense (checks for '../', '..\\', absolute roots, null bytes).
- Decompression bomb / Zip bomb mitigation:
  * Maximum compression ratio enforcement (threshold 100:1).
  * Maximum total uncompressed size limit (50 MB).
  * Maximum entry count limit (250 entries).
- Embedded executable and script detection within archive archives.
- Support for standard ZIP archives (and TAR archives if applicable).
"""

import io
import os
import tarfile
import zipfile
from typing import List, Tuple
from app.services.file_security.schemas import ArchiveInspectionResult


class ArchiveSafetyGuard:
    """Safe static inspector for compressed archives without disk extraction."""

    # Safety Thresholds
    MAX_UNCOMPRESSED_BYTES = 50 * 1024 * 1024  # 50 MB
    MAX_ENTRY_COUNT = 250                      # Max 250 entries
    MAX_COMPRESSION_RATIO = 100.0              # 100:1 ratio

    # Dangerous executable extensions embedded inside archives
    DANGEROUS_EXTENSIONS = {
        ".exe", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".vbe", ".js",
        ".jse", ".wsf", ".wsh", ".hta", ".cpl", ".msi", ".jar", ".pif",
        ".com", ".sh", ".bash", ".elf", ".bin"
    }

    @classmethod
    def inspect(cls, file_bytes: bytes, filename: str) -> ArchiveInspectionResult:
        """
        Inspect archive metadata safely from memory bytes.
        Does NOT write or extract any files to the filesystem.
        """
        file_size = len(file_bytes)
        lower_name = filename.lower()

        # Check if file is ZIP
        if file_bytes.startswith(b"PK\x03\x04") or file_bytes.startswith(b"PK\x05\x06") or lower_name.endswith(".zip"):
            return cls._inspect_zip(file_bytes, file_size)

        # Check if file is TAR
        if lower_name.endswith((".tar", ".tar.gz", ".tgz")) or (file_size >= 512 and file_bytes[257:262] == b"ustar"):
            return cls._inspect_tar(file_bytes, file_size)

        return ArchiveInspectionResult(
            is_archive=False,
            total_entries=0,
            total_uncompressed_bytes=0,
            compression_ratio=1.0,
            has_path_traversal=False,
            traversal_entries=[],
            is_decompression_bomb=False,
            embedded_executables=[],
            inspected_safely_without_extraction=True,
        )

    @classmethod
    def _inspect_zip(cls, file_bytes: bytes, compressed_size: int) -> ArchiveInspectionResult:
        """Inspect ZIP central directory records safely."""
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes), mode="r") as zf:
                infolist = zf.infolist()
                total_entries = len(infolist)
                total_uncompressed = 0
                has_path_traversal = False
                traversal_entries: List[str] = []
                embedded_execs: List[str] = []
                is_bomb = False

                if total_entries > cls.MAX_ENTRY_COUNT:
                    is_bomb = True

                for info in infolist:
                    entry_name = info.filename
                    total_uncompressed += info.file_size

                    # 1. Path traversal / Zip Slip check
                    if cls._is_path_traversal(entry_name):
                        has_path_traversal = True
                        traversal_entries.append(entry_name)

                    # 2. Individual file compression ratio check
                    if info.compress_size > 0:
                        single_ratio = info.file_size / float(info.compress_size)
                        if single_ratio > cls.MAX_COMPRESSION_RATIO:
                            is_bomb = True

                    # 3. Check for dangerous embedded executables
                    _, ext = os.path.splitext(entry_name.lower())
                    if ext in cls.DANGEROUS_EXTENSIONS:
                        embedded_execs.append(entry_name)

                # Overall compression ratio
                safe_comp_size = max(compressed_size, 1)
                overall_ratio = round(total_uncompressed / float(safe_comp_size), 2)
                if overall_ratio > cls.MAX_COMPRESSION_RATIO or total_uncompressed > cls.MAX_UNCOMPRESSED_BYTES:
                    is_bomb = True

                return ArchiveInspectionResult(
                    is_archive=True,
                    total_entries=total_entries,
                    total_uncompressed_bytes=total_uncompressed,
                    compression_ratio=overall_ratio,
                    has_path_traversal=has_path_traversal,
                    traversal_entries=traversal_entries,
                    is_decompression_bomb=is_bomb,
                    embedded_executables=embedded_execs,
                    inspected_safely_without_extraction=True,
                )
        except zipfile.BadZipFile:
            return ArchiveInspectionResult(
                is_archive=True,
                total_entries=0,
                total_uncompressed_bytes=0,
                compression_ratio=1.0,
                has_path_traversal=False,
                traversal_entries=[],
                is_decompression_bomb=False,
                embedded_executables=[],
                inspected_safely_without_extraction=True,
            )

    @classmethod
    def _inspect_tar(cls, file_bytes: bytes, compressed_size: int) -> ArchiveInspectionResult:
        """Inspect TAR header records safely."""
        try:
            with tarfile.open(fileobj=io.BytesIO(file_bytes), mode="r:*") as tf:
                members = tf.getmembers()
                total_entries = len(members)
                total_uncompressed = 0
                has_path_traversal = False
                traversal_entries: List[str] = []
                embedded_execs: List[str] = []
                is_bomb = False

                if total_entries > cls.MAX_ENTRY_COUNT:
                    is_bomb = True

                for member in members:
                    entry_name = member.name
                    total_uncompressed += member.size

                    if cls._is_path_traversal(entry_name):
                        has_path_traversal = True
                        traversal_entries.append(entry_name)

                    _, ext = os.path.splitext(entry_name.lower())
                    if ext in cls.DANGEROUS_EXTENSIONS:
                        embedded_execs.append(entry_name)

                safe_comp_size = max(compressed_size, 1)
                overall_ratio = round(total_uncompressed / float(safe_comp_size), 2)
                if overall_ratio > cls.MAX_COMPRESSION_RATIO or total_uncompressed > cls.MAX_UNCOMPRESSED_BYTES:
                    is_bomb = True

                return ArchiveInspectionResult(
                    is_archive=True,
                    total_entries=total_entries,
                    total_uncompressed_bytes=total_uncompressed,
                    compression_ratio=overall_ratio,
                    has_path_traversal=has_path_traversal,
                    traversal_entries=traversal_entries,
                    is_decompression_bomb=is_bomb,
                    embedded_executables=embedded_execs,
                    inspected_safely_without_extraction=True,
                )
        except Exception:
            return ArchiveInspectionResult(
                is_archive=True,
                total_entries=0,
                total_uncompressed_bytes=0,
                compression_ratio=1.0,
                has_path_traversal=False,
                traversal_entries=[],
                is_decompression_bomb=False,
                embedded_executables=[],
                inspected_safely_without_extraction=True,
            )

    @classmethod
    def _is_path_traversal(cls, entry_name: str) -> bool:
        """Detect directory traversal sequences or absolute paths."""
        if "\x00" in entry_name:
            return True
        norm = entry_name.replace("\\", "/")
        if norm.startswith("/") or norm.startswith("~"):
            return True
        # Check Windows drive letters like C:/ or C:\
        if len(norm) >= 2 and norm[1] == ":" and norm[0].isalpha():
            return True
        parts = norm.split("/")
        return ".." in parts
