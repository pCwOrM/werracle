#!/usr/bin/env python3
"""
Werracle v2.0 Production Announcement Dispatcher & Mail Engine
Uses corporate SMTP (mail.answerr.me:465) to dispatch peer-reviewed release pitches
from ask@answerr.me with automated bounce suppression, spam defense, and rate-limiting.
"""

import sys
import smtplib
import ssl
import time
import json
import os
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

MAIL_CONFIG_PATH = os.path.expanduser("~/.answerr/mail.json")
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "results", "announcement_dispatch_log.json")

def load_mail_credentials():
    smtp_server = os.environ.get("SMTP_SERVER", "mail.answerr.me")
    smtp_port = int(os.environ.get("SMTP_PORT", 465))
    auth_user = os.environ.get("SMTP_USER", "ask@answerr.me")
    auth_pass = os.environ.get("SMTP_PASS", "")

    if os.path.exists(MAIL_CONFIG_PATH):
        try:
            with open(MAIL_CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                smtp_server = cfg.get("smtp_server", smtp_server)
                smtp_port = int(cfg.get("smtp_port", smtp_port))
                auth_user = cfg.get("email", auth_user)
                auth_pass = cfg.get("password", auth_pass)
        except Exception as e:
            print(f"Warning: could not load config from {MAIL_CONFIG_PATH}: {e}")

    return smtp_server, smtp_port, auth_user, auth_pass

SMTP_SERVER, SMTP_PORT, AUTH_USER, AUTH_PASS = load_mail_credentials()

from email.utils import formataddr

SENDER_DISPLAY = formataddr(("Volkan Dagli (ITouch Systems)", AUTH_USER))
REPLY_TO = "ask@answerr.me, vdagli@itouch.com.tr, pcworm@pcworm.net"

# -----------------------------------------------------------------------------
# ANTI-SPAM & BOUNCE SUPPRESSION REGISTRY (AUDITED FROM IMAP LIVE SCAN)
# -----------------------------------------------------------------------------
BOUNCE_SUPPRESSION_LIST = {
    "ai-tips@venturebeat.com",
    "ask@answerr.com",             # Correct corporate host is ask@answerr.me
    "build@base.org",              # Inactive desk
    "contact@alphasignal.ai",      # Undeliverable
    "contact@tinyml.org",          # User unknown
    "editor@weekinethereumnews.com", # Relay access denied
    "editorial@banklesshq.com",    # Mailbox does not exist
    "grants@near.foundation",      # Mailbox unavailable
    "grants@uniswapfoundation.org", # Google group closed to public
    "info@qosf.org",               # Address does not exist
    "jack@importai.net",           # Mail server unreachable / expired
    "news@dlnews.com",             # Mail server unreachable / expired
    "newsletter@thesequence.io",   # Mail server unreachable / expired
    "noreply@answerr.me",
    "pcworm@gmail.com",            # Not author address / bounce
    "pcworm@itouchsystems.com",    # Inactive domain alias
    "solidityweekly@gmail.com",    # Mailbox does not exist
    "tips@coindesk.com",           # Proofpoint reject
    "tips@decrypt.co",             # Undeliverable
}

# Ongoing reviews or paused programs - DO NOT send duplicate cold emails
PAUSED_OR_REVIEWING_LIST = {
    "grants@starknet.org": "Application currently in Pre-Screening review (confirmed 2026-09-23)",
    "research-grants@protocol.ai": "Protocol Labs research grant program currently paused",
}

# -----------------------------------------------------------------------------
# CURATED ANNOUNCEMENT TARGETS (VETTED & ACTIVE)
# -----------------------------------------------------------------------------
TARGET_CHANNELS = {
    "self_test": {
        "name": "Werracle Lead Engineering & Archive",
        "to": ["pcworm@pcworm.net", "ask@answerr.me"],
        "subject": "⚡ Werracle v2.0 Release: Sparse Harmonic Tripod & ZMod 9 Modular Resonance [EVM Benchmarks & 1000-Test Seal]"
    },
    "week_in_ethereum": {
        "name": "Week in Ethereum News (Evan Van Ness)",
        "to": ["editor@weekinethereumnews.com"],
        "subject": "Project Submission: Werracle v2.0 - Zero-Storage On-Chain AI in 32-Byte Slot (22.5k gas on EVM)"
    },
    "solidity_weekly": {
        "name": "Solidity Weekly Newsletter",
        "to": ["solidityweekly@gmail.com"],
        "subject": "Solidity Architecture: Werracle v2.0 - 90% Gas Cut via Native Unchecked Int256 & ZMod 9 Early Escape"
    },
    "ethereum_esp": {
        "name": "Ethereum Foundation Ecosystem Support Program (ESP)",
        "to": ["esp@ethereum.org"],
        "subject": "Grant Inquiry: Werracle v2.0 - Machine-Native On-Chain AI Decisions (Public Good / Open Source)"
    },
    "uniswap_grants": {
        "name": "Uniswap Foundation Grants Desk",
        "to": ["grants@uniswapfoundation.org"],
        "subject": "Grant Inquiry: WerracleFeeHook v2.0 - Dynamic Chaos-Adaptive AMM Fee Governor for Uniswap v4 (36k gas)"
    },
    "dlnews": {
        "name": "DL News / DefiLlama Editorial",
        "to": ["news@dlnews.com"],
        "subject": "DeFi Breakthrough: Werracle v2.0 - Micro-Gas AI Decision Oracle Defending EVM Transactions"
    },
    "bankless": {
        "name": "Bankless Editorial Team",
        "to": ["editorial@banklesshq.com"],
        "subject": "Web3 Innovation: Zero-Storage On-Chain AI Oracle Drops EVM Inference to 22.5k Gas"
    },
    "avalanche_grants": {
        "name": "Avalanche Foundation Grants Desk & Blizzard Fund",
        "to": ["grants@avax.network", "Blizzard@avalabs.org"],
        "subject": "Grant Inquiry: Werracle v2.0 - Machine-Native On-Chain AI Decisions for Avalanche C-Chain & Subnets"
    },
    "solana_grants": {
        "name": "Solana Foundation Grants Program",
        "to": ["grants@solana.org"],
        "subject": "Grant Inquiry: Werracle - High-Throughput Procedural Decision Oracle & Micro-AI Public Good"
    },
    "arbitrum_grants": {
        "name": "Arbitrum Foundation Grants Program",
        "to": ["grants@arbitrum.foundation"],
        "subject": "Grant Inquiry: Werracle v2.0 - Sub-Cent On-Chain AI Decision Oracle on Arbitrum Nitro (22.5k gas)"
    },
    "optimism_grants": {
        "name": "Optimism Foundation Grants Desk",
        "to": ["grants@optimism.io"],
        "subject": "Grant Inquiry: Werracle v2.0 - Public Good Micro-AI Oracle for the Superchain"
    }
}

BODY_EDITORIAL_V2 = """Hello {recipient_name},

We are pleased to announce the release of Werracle v2.0, introducing the Sparse Multi-Scale Harmonic Tripod and ZMod 9 modular resonance dynamics for intra-block, machine-native EVM decisions.

Unlike traditional ML models requiring gigabytes of tensor weight storage or ZK-ML incurring heavy prover latencies, Werracle synthesizes decision boundaries on-the-fly from a compact 24-byte Mandelbrot coordinate triplet (cx, cy, zoom) stored entirely within a single 32-byte EVM storage slot (bytes32).

Key Innovations & Live EVM Benchmarks in v2.0:
• Multi-Scale Harmonic Tripod: Samples across 3 harmonic zoom planes (0.60x Wide Horizon, 1.00x Natural Focus, 1.60x Deep Cusp) with a sparse 12-point cardinal micro-grid.
• ZMod 9 Modular Early Escape (Lean 4 Formalized): Escape boundaries evaluated at modular milestones n in {{3, 6, 9}}. Shocks and flash attacks escape at step 3, slashing gas from 61k down to 44k (attack defense is cheaper than normal queries).
• 90.0% Gas Reduction on Live EVM (Cancun / EIP-150 / EIP-2929 / EIP-3860):
  - Pure Forward Engine: 22,557 gas (down from 226,363 gas baseline)
  - Worst-Case Ceiling: 22,568 gas <= 24,000 gas limit (PASSED with +1,432 gas headroom)
  - Multi-Way Choice Routing: 43,726 gas (2 choices) to 44,680 gas (8 choices)
  - 0 SLOAD Blockchain Resonance Matrix: 3,821 gas (1 token) / 7,443 gas (4-token fusion)
  - Uniswap v4 Dynamic Fee Hook: 36,739 gas end-to-end
• Cryptographically Sealed Integrity: 1,000/1,000 deterministic test battery passed with 100.00% success rate in 287 ms (SHA-256: b58e7e5d3d082b3a3ceee6083e85f80ef59c9dc247144287b696a6f907422d99).
• Strict Privacy by Design: Telemetry is permanently disabled (Zero external network leakage).

Live Ecosystem Resources:
• High-Performance Gateway (Chain ID 4242): https://api.answerr.me:4431/werracle/status
• Interactive Portal & Docs: https://pcworm.github.io/werracle/
• Live Interactive API Docs: https://pcworm.github.io/werracle/apidocs.html
• GitHub Repository (Release v2.0.0): https://github.com/pCwOrM/werracle
• Formal Gas Audit: https://github.com/pCwOrM/werracle/blob/main/docs/EVM_GAS_IDEAL_BENCHMARK_REPORT.md

Developed by ITOUCH BİLİŞİM SİSTEMLERİ LTD. ŞTİ. (Çukurova Teknokent) & Volkan Dağlı.
Patent: TR 2026/016285. License: BSL 1.1.

Direct Contacts:
Volkan Dağlı (pcworm@pcworm.net, vdagli@itouch.com.tr)
Autonomous Engine: ask@answerr.me

We welcome collaboration, security audits, and grant review inquiries with your ecosystem.

Best regards,
Werracle Autonomous Core Team
https://pcworm.github.io/werracle/
"""

def filter_recipients(to_emails):
    valid = []
    skipped = []
    for email_addr in to_emails:
        addr = email_addr.strip().lower()
        if addr in BOUNCE_SUPPRESSION_LIST or addr.endswith(".mai@mail.teknosanat.com.tr"):
            skipped.append((addr, "BOUNCE_BLACKLISTED"))
        elif addr in PAUSED_OR_REVIEWING_LIST:
            skipped.append((addr, PAUSED_OR_REVIEWING_LIST[addr]))
        elif not re.match(r"^[^@]+@[^@]+\.[^@]+$", addr):
            skipped.append((addr, "MALFORMED_SYNTAX"))
        else:
            valid.append(addr)
    return valid, skipped

def send_announcement(target_key="self_test", dry_run=False):
    if target_key not in TARGET_CHANNELS:
        print(f"Unknown target key: '{target_key}'")
        return False

    target = TARGET_CHANNELS[target_key]
    recipient_name = target["name"]
    raw_to = target["to"]
    subject = target["subject"]

    valid_to, skipped = filter_recipients(raw_to)

    if skipped:
        for s_addr, reason in skipped:
            print(f" [SUPPRESSED] Skipped {s_addr} -> Reason: {reason}")

    if not valid_to:
        print(f" [ABORTED] No valid recipients remaining for '{target_key}'.")
        return False

    msg = MIMEMultipart()
    msg["From"] = SENDER_DISPLAY
    msg["To"] = ", ".join(valid_to)
    msg["Reply-To"] = REPLY_TO
    msg["Subject"] = subject

    body = BODY_EDITORIAL_V2.format(recipient_name=recipient_name)
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if dry_run:
        print(f"\n[DRY RUN] Target: {target_key}")
        print(f"  To: {valid_to}")
        print(f"  Subject: {subject}")
        print(f"  Body Preview (First 300 chars):\n  {body[:300].strip()}...\n")
        return True

    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT} for target '{target_key}'...")
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    status_entry = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "target_key": target_key,
        "recipient_name": recipient_name,
        "recipients": valid_to,
        "subject": subject,
        "status": "PENDING"
    }

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(AUTH_USER, AUTH_PASS)
            server.sendmail(AUTH_USER, valid_to, msg.as_string())
        print(f" [DELIVERED] Email successfully sent to: {valid_to} ({recipient_name})")
        status_entry["status"] = "DELIVERED"
        _log_dispatch(status_entry)
        return True
    except Exception as e:
        print(f" [ERROR] Delivery failure for {valid_to}: {e}")
        status_entry["status"] = f"FAILED: {e}"
        _log_dispatch(status_entry)
        return False

def _log_dispatch(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    history = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append(entry)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python scripts/announcement_mailer.py [target|list|all|dry-run-all]")
        print("Available targets:")
        for k, v in TARGET_CHANNELS.items():
            valid, skipped = filter_recipients(v['to'])
            print(f"  • {k:18} -> {v['name']} (Active: {valid}, Suppressed: {[s[0] for s in skipped]})")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "list":
        print("=" * 70)
        print(" TARGET CHANNELS & SUPPRESSION STATUS")
        print("=" * 70)
        for k, v in TARGET_CHANNELS.items():
            valid, skipped = filter_recipients(v['to'])
            supp_str = f" | Suppressed: {[s[0] for s in skipped]}" if skipped else ""
            print(f" • {k:18} -> {v['name']} ({', '.join(valid)}){supp_str}")
    elif cmd == "dry-run-all":
        print("=" * 70)
        print(" SIMULATING ANNOUNCEMENT DISPATCH (DRY RUN)")
        print("=" * 70)
        for k in TARGET_CHANNELS:
            send_announcement(k, dry_run=True)
    elif cmd == "all":
        print("=" * 70)
        print(" DISPATCHING ANNOUNCEMENTS (RATE-LIMITED: 3s DELAY)")
        print("=" * 70)
        for idx, k in enumerate(TARGET_CHANNELS):
            send_announcement(k, dry_run=False)
            if idx < len(TARGET_CHANNELS) - 1:
                time.sleep(3.0)  # Gentle rate limit to avoid SMTP flooding
    else:
        is_dry = "--dry-run" in sys.argv
        send_announcement(cmd, dry_run=is_dry)
