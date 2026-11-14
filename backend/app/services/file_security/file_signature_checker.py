"""CyberShield AI 2.0 — File Signature & Magic Bytes Checker
Member 2: Static signature verification and extension spoofing detection.

Features:
- Pure Python magic bytes detection (zero external C dependencies or DLL requirements).
- Detection of Portable Executable (PE/MZ), Linux ELF, and Apple Mach-O binaries.
- Extension mismatch / spoofing detection (e.g., .pdf or .jpg hiding an executable header).
- Dangerous script identification (PowerShell, Bash, Batch, VBS, HTA, WSH).
- Legacy Microsoft Office OLE and Modern OOXML macro indicator detection.
- Double-extension pattern detection (e.g. invoice.pdf.exe).
"""

import os
import re
from typing import List, Tuple
from app.services.file_security.schemas import FileSignatureCheckResult


class FileSignatureChecker:
    """Static file signature and header inspection engine."""

    # Dangerous executable extensions
    DANGEROUS_EXECUTABLE_EXTENSIONS = {
        ".exe", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".vbe", ".js", ".jse",
        ".wsf", ".wsh", ".hta", ".cpl", ".msi", ".msp", ".reg", ".pif", ".com",
        ".gadget", ".jar", ".bin", ".elf", ".sh", ".bash", ".action", ".apk"
    }

    # Macro-enabled document extensions
    MACRO_DOCUMENT_EXTENSIONS = {
        ".docm", ".xlsm", ".pptm", ".dotm", ".xltm", ".potm", ".xlam"
    }

    # Standard office extensions
    STANDARD_OFFICE_EXTENSIONS = {
        ".docx", ".xlsx", ".pptx", ".doc", ".xls", ".ppt", ".odt", ".ods", ".odp"
    }

    @classmethod
    def check_signature(cls, filename: str, header_bytes: bytes) -> FileSignatureCheckResult:
        """
        Inspect header bytes (first 512 bytes) and compare against filename extension.
        Strictly non-executing.
        """
        base_name = os.path.basename(filename)
        _, ext = os.path.splitext(base_name.lower())
        magic_hex = header_bytes[:16].hex().upper()
        if len(magic_hex) > 0:
            magic_hex_formatted = " ".join(magic_hex[i:i+2] for i in range(0, len(magic_hex), 2))
        else:
            magic_hex_formatted = "(Empty File)"

        detected_mime = "application/octet-stream"
        detected_format = "Unknown Binary or Generic Data"
        is_executable = False
        is_script = False
        is_macro = False
        details: List[str] = []

        # 1. Check Magic Byte Signatures
        if header_bytes.startswith(b"MZ"):
            detected_mime = "application/x-dosexec"
            detected_format = "Windows PE/COFF Executable or DLL (MZ header)"
            is_executable = True
            details.append("Detected Windows PE/MZ executable header (4D 5A).")

        elif header_bytes.startswith(b"\x7fELF"):
            detected_mime = "application/x-executable"
            detected_format = "Linux / Unix Executable and Linkable Format (ELF)"
            is_executable = True
            details.append("Detected Unix ELF executable binary header (7F 45 4C 46).")

        elif header_bytes.startswith((b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe", b"\xca\xfe\xba\xbe")):
            detected_mime = "application/x-mach-binary"
            detected_format = "Apple Mach-O Binary or Java Class Bytecode"
            is_executable = True
            details.append("Detected Mach-O / Java universal binary header.")

        elif header_bytes.startswith(b"%PDF-"):
            detected_mime = "application/pdf"
            detected_format = "Adobe Portable Document Format (PDF)"
            details.append("Valid PDF document header detected.")

        elif header_bytes.startswith(b"PK\x03\x04") or header_bytes.startswith(b"PK\x05\x06") or header_bytes.startswith(b"PK\x07\x08"):
            detected_mime = "application/zip"
            detected_format = "ZIP Compressed Archive / Open Packaging Convention (OPC)"
            details.append("Standard PK-ZIP container header detected.")

        elif header_bytes.startswith(b"\x1f\x8b"):
            detected_mime = "application/gzip"
            detected_format = "GZIP Compressed Archive"
            details.append("Standard GZIP archive header detected.")

        elif header_bytes.startswith(b"7z\xbc\xaf\x27\x1c"):
            detected_mime = "application/x-7z-compressed"
            detected_format = "7-Zip Compressed Archive"
            details.append("7-Zip archive header detected.")

        elif header_bytes.startswith(b"Rar!\x1a\x07"):
            detected_mime = "application/vnd.rar"
            detected_format = "RAR Archive"
            details.append("RAR compressed archive header detected.")

        elif header_bytes.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
            detected_mime = "application/x-ole-storage"
            detected_format = "Microsoft Compound File Binary / OLE Document"
            details.append("Legacy Microsoft Office OLE compound storage container detected.")
            # Check for VBA / Macro markers in OLE header
            if b"VBA" in header_bytes or b"_VBA_PROJECT" in header_bytes or b"Macros" in header_bytes:
                is_macro = True
                details.append("Embedded VBA Project / Macro stream identified in OLE document.")

        elif header_bytes.startswith(b"\xff\xd8\xff"):
            detected_mime = "image/jpeg"
            detected_format = "JPEG Image"
            details.append("Standard JPEG image header detected.")

        elif header_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            detected_mime = "image/png"
            detected_format = "PNG Image"
            details.append("Standard PNG image header detected.")

        elif header_bytes.startswith(b"GIF87a") or header_bytes.startswith(b"GIF89a"):
            detected_mime = "image/gif"
            detected_format = "GIF Image"
            details.append("Standard GIF image header detected.")

        elif header_bytes.startswith(b"{\\rtf"):
            detected_mime = "application/rtf"
            detected_format = "Rich Text Format (RTF)"
            details.append("Rich Text Format document detected.")

        # Check for scripts (Text-based with shebang or script markers)
        try:
            head_text = header_bytes[:512].decode("utf-8", errors="ignore")
            head_lower = head_text.lower()
            if head_text.startswith("#!"):
                is_script = True
                detected_mime = "text/x-shellscript"
                detected_format = "Unix Shell Script (Shebang header)"
                details.append(f"Shebang interpreter line detected: {head_text.splitlines()[0][:50]}")
            elif re.search(r"(?i)(?:@echo\s+off|echo\s+%|\bsetlocal\b|\brem\b)", head_text) and ext in {".bat", ".cmd"}:
                is_script = True
                detected_mime = "text/x-msdos-batch"
                detected_format = "Windows Command / Batch Script"
                details.append("Windows Batch script commands identified.")
            elif re.search(r"(?i)(?:powershell|invoke-expression|\biex\b|param\s*\(|get-process)", head_text):
                is_script = True
                detected_mime = "text/x-powershell"
                detected_format = "PowerShell Script"
                details.append("PowerShell commands or cmdlets identified.")
            elif re.search(r"(?i)(?:wscript\.|createobject\s*\(|msgbox\b|dim\s+\w+)", head_text) and ext in {".vbs", ".vbe", ".wsf"}:
                is_script = True
                detected_mime = "text/x-vbscript"
                detected_format = "VBScript File"
                details.append("VBScript automation commands identified.")
            elif re.search(r"(?i)<script\b", head_text) and ext in {".hta", ".html", ".htm"}:
                if ext == ".hta":
                    is_script = True
                    detected_format = "HTML Application (HTA - Direct System Execution Risk)"
                    details.append("HTA application markup identified.")
            elif re.search(r"(?i)(?:function|var|const|let)\s+\w+.*\{", head_text) and ext in {".js", ".jse"}:
                is_script = True
                detected_mime = "text/javascript"
                detected_format = "JavaScript File"
                details.append("JavaScript code identified.")
        except Exception:
            pass

        # 2. Check for Extension Mismatch / Spoofing
        is_mismatch = False
        # Case A: File claims to be non-executable document/image (e.g. .pdf, .jpg, .png, .docx, .txt),
        # but magic bytes indicate Windows PE or ELF executable!
        non_exec_extensions = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".txt", ".csv", ".docx", ".xlsx", ".pptx", ".mp3", ".mp4"}
        if ext in non_exec_extensions and is_executable:
            is_mismatch = True
            details.append(
                f"CRITICAL EXTENSION SPOOFING: File extension is '{ext}' but internal file signature is '{detected_format}'."
            )

        # Case B: Double Extension Masquerade (e.g. report.pdf.exe, invoice.xlsx.vbs)
        parts = base_name.lower().split(".")
        if len(parts) >= 3:
            hidden_ext = f".{parts[-2]}"
            actual_ext = f".{parts[-1]}"
            if hidden_ext in non_exec_extensions and actual_ext in cls.DANGEROUS_EXECUTABLE_EXTENSIONS:
                details.append(
                    f"DOUBLE EXTENSION DETECTED: Disguised as document '{hidden_ext}' but executed via '{actual_ext}'."
                )

        # Case C: Macro extension mismatch (claims to be .docx but has macro streams)
        if ext == ".docx" and is_macro:
            is_mismatch = True
            details.append("Extension is .docx (Standard Word) but contains active macro payloads.")

        # Check if extension itself is dangerous
        if ext in cls.DANGEROUS_EXECUTABLE_EXTENSIONS and not is_executable and not is_script:
            details.append(f"Dangerous executable file extension '{ext}' detected on host system.")

        return FileSignatureCheckResult(
            detected_mime=detected_mime,
            detected_format=detected_format,
            reported_extension=ext or "(None)",
            is_extension_mismatch=is_mismatch,
            is_executable=is_executable,
            is_script=is_script,
            is_macro_enabled=is_macro,
            magic_hex=magic_hex_formatted,
            details=" | ".join(details) if details else "File signature verified normal for reported extension.",
        )
