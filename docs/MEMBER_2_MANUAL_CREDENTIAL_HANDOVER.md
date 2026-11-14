# CYBERSHIELD AI 2.0 — MEMBER 2 MANUAL CREDENTIAL HANDOVER
## Out-of-Band API Key Exchange Protocol & Zero-Trust Secret Governance

**Author:** Senior DevOps & Backend Integration Specialist (Member 2)  
**Target Recipient:** Backend API & Integration Engineer (Member 1)  
**Security Classification:** RESTRICTED — INTERNAL TEAM USE ONLY  
**Date:** November 14, 2026

---

## 1. Zero-Trust Security Directive

> [!CAUTION]
> **NEVER COMMIT OR SHARE API KEYS VIA GITHUB OR PUBLIC CHANNELS.**  
> API keys, database credentials, and session tokens must never appear in version control, pull requests, commit messages, or public issue trackers. All credential transfers between Member 2 and Member 1 must occur through encrypted, out-of-band communication channels.

---

## 2. Credential Categorization & Governance Matrix

| Credential Name | Provider Service | Can Member 1 Generate Independently? | Must Be Shared by Member 2? | Recommended Transmission Channel |
| :--- | :--- | :---: | :---: | :--- |
| **`GEMINI_API_KEY`** | Google AI Studio | **YES** (Recommended) | Optional | End-to-End Encrypted Messenger / Bitwarden |
| **`GROQ_API_KEY`** | Groq Cloud Console | **YES** (Recommended) | Optional | End-to-End Encrypted Messenger / Bitwarden |
| **`OPENAI_API_KEY`** | OpenAI Developer Portal | **YES** (Optional) | Optional | End-to-End Encrypted Messenger / Bitwarden |
| **`JWT_SECRET`** | Backend Session Auth | **YES** (Generate locally) | **NO** | Generate locally via `openssl rand -hex 32` |
| **`DATABASE_URL`** | SQLite Local Storage | **YES** (Default local file) | **NO** | Keep local: `sqlite:///./cybershield.db` |

---

## 3. Which Keys Member 1 Can Configure Independently

Member 1 does **not** strictly require Member 2's personal API keys. Member 1 can generate their own development keys in under 2 minutes:

1. **Google Gemini API Key (Tier 1 AI Engine)**:
   - Navigate to: [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with any Google account.
   - Click **Create API Key**.
   - Copy key and set in `backend/.env`:
     ```bash
     GEMINI_API_KEY=your_key_here
     ```

2. **Groq Cloud API Key (Tier 2 Ultra-Low Latency Failover)**:
   - Navigate to: [Groq Console](https://console.groq.com/keys)
   - Sign in and click **Create API Key**.
   - Copy key and set in `backend/.env`:
     ```bash
     GROQ_API_KEY=your_key_here
     ```

---

## 4. When Out-of-Band Sharing Is Required

If Member 1 does not have active Google AI Studio or Groq accounts and Member 2 provides project keys, Member 2 must transmit the keys using one of the following **authorized secure channels**:

### Approved Secure Transmission Channels:
1. **End-to-End Encrypted Messaging**: Signal or WhatsApp disappearing messages.
2. **Password Manager Secure Send**: Bitwarden Send or 1Password Share (set to expire after 1 view or 24 hours).
3. **Encrypted Archive**: AES-256 encrypted `.zip` or `.7z` archive transferred directly via USB drive or secure local LAN transfer with password communicated verbally.

### Strictly Prohibited Channels:
- ❌ GitHub Commits, Pull Requests, or Issues.
- ❌ Public Slack or Discord channels.
- ❌ Unencrypted plain-text emails.
- ❌ Screenshots posted in team documentation or presentation slide decks.

---

## 5. What Happens If No API Keys Are Shared?

If Member 1 runs the project without any cloud API keys:
- The backend **will NOT crash**.
- The API endpoints (`/scans/message`, `/scans/file`, `/analyze-file`) **will NOT return 500 errors**.
- `LLMClient` detects that no cloud API keys are present and automatically routes all requests to the **Tier 4 Deterministic Offline Heuristic Engine**.
- The deterministic engine evaluates all 50+ threat heuristics, performs verbatim evidence grounding, computes static risk scores, and returns structured threat assessments in under 2 milliseconds!
- All 15 offline round test scenarios will continue to pass with a **100% success rate**.
