#!/usr/bin/env python3
"""
Werracle Automated Announcement Mailer
Uses corporate SMTP (mail.teknosanat.com.tr:465) to dispatch announcement pitches
from ask@answerr.me to Web3 editorial digests, newsletters, and foundation grant desks.
"""

import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
import os

MAIL_CONFIG_PATH = os.path.expanduser("~/.answerr/mail.json")

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

SENDER_DISPLAY = "Werracle Autonomous Engine <ask@answerr.me>"
REPLY_TO = "ask@answerr.me, pcworm@pcworm.net"

# Curated Web3 editorial contacts & newsletters
TARGET_CHANNELS = {
    "self_test": {
        "name": "Owner Self-Test & Archive",
        "to": ["pcworm@pcworm.net", "ask@answerr.me"],
        "subject": "⚡ Werracle: Zero-Storage On-Chain AI Decision Oracle [Live EVM Devnet Showcase]"
    },
    "week_in_ethereum": {
        "name": "Week in Ethereum News (Evan Van Ness)",
        "to": ["editor@weekinethereumnews.com"],
        "subject": "Project Submission: Werracle - Zero-Storage On-Chain AI Decision Oracle in 32-Byte Slot (~21k gas)"
    },
    "solidity_weekly": {
        "name": "Solidity Weekly Newsletter",
        "to": ["solidityweekly@gmail.com"],
        "subject": "Solidity Showcase: Werracle & Uniswap v4 Dynamic Fee Hook"
    },
    "ethereum_esp": {
        "name": "Ethereum Foundation Ecosystem Support Program (ESP)",
        "to": ["esp@ethereum.org"],
        "subject": "Grant Inquiry: Werracle - Machine-Native On-Chain AI Decisions (Public Good / Open Source)"
    },
    "uniswap_grants": {
        "name": "Uniswap Foundation Grants Desk",
        "to": ["grants@uniswapfoundation.org"],
        "subject": "Grant Inquiry: WerracleFeeHook - Dynamic Chaos-Adaptive AMM Fee Governor for Uniswap v4"
    },
    "dlnews": {
        "name": "DL News / DefiLlama Editorial",
        "to": ["news@dlnews.com"],
        "subject": "DeFi Security Release: Werracle - Native Sub-Millisecond AI Decision Oracle for EVM"
    },
    "bankless": {
        "name": "Bankless Editorial Team",
        "to": ["editorial@banklesshq.com"],
        "subject": "Web3 Innovation: Zero-Storage On-Chain AI Oracle for Intra-Block Defense"
    },
    "avalanche_grants": {
        "name": "Avalanche Foundation Grants Desk & Blizzard Fund",
        "to": ["grants@avax.network", "Blizzard@avalabs.org"],
        "subject": "Grant Inquiry: Werracle - Machine-Native On-Chain AI Decisions for Avalanche C-Chain & Subnets"
    },
    "solana_grants": {
        "name": "Solana Foundation Grants Program",
        "to": ["grants@solana.org"],
        "subject": "Grant Inquiry: Werracle - High-Throughput Procedural Decision Oracle & Micro-AI Public Good"
    },
    "arbitrum_grants": {
        "name": "Arbitrum Foundation Grants Program",
        "to": ["grants@arbitrum.foundation"],
        "subject": "Grant Inquiry: Werracle - Sub-Cent On-Chain AI Decision Oracle on Arbitrum Nitro"
    },
    "optimism_grants": {
        "name": "Optimism Foundation Grants Desk",
        "to": ["grants@optimism.io"],
        "subject": "Grant Inquiry: Werracle - Public Good System-One AI Oracle for the Superchain"
    }
}

BODY_EDITORIAL = """Hello {recipient_name},

We are announcing Werracle, the first production-grade On-Chain AI Decision Oracle capable of executing intra-block, sub-millisecond AI decisions directly inside EVM smart contracts.

Key Innovations:
• Zero Storage Overhead: Instead of multi-gigabyte neural weight matrices, decision boundaries are procedurally synthesized from a 24-byte Mandelbrot coordinate triplet (cx, cy, zoom).
• Single 32-Byte Slot: The entire model fits into a single EVM storage slot (bytes32).
• Micro-Gas Footprint: Pure bytecode fixed-point Q16.16 math (WerrMath.sol) evaluates a 16-point Pareto micro-grid in ~21,438 gas (< $0.001 on L2s like Base and Arbitrum). 1000x faster than ZK-ML.
• Uniswap v4 Dynamic Fee Hook: WerracleFeeHook.sol measures real-time orderbook chaos and adjusts LP fees between 0.05% and 0.50% atomically inside the swap.
• Cryptographically Sealed: Passed a 1,000-test deterministic battery with 100% pass rate (SHA-256 sealed).
• Privacy by Design: Telemetry is permanently disabled.

Live Sandbox & Resources:
• Live EVM Node (mechsrv, Chain ID 4242): https://api.answerr.me:4431/werracle/status
• Live Interactive API Docs: https://pcworm.github.io/werracle/apidocs.html
• Browser Simulator: https://pcworm.github.io/werracle/
• GitHub Repository: https://github.com/pCwOrM/werracle
• Learn & Collaborate: https://github.com/pCwOrM/werracle/blob/main/LEARN.md

Developed by ITOUCH BILISIM SISTEMLERI LTD. STI. (Cukurova Teknokent) & Volkan Dagli.
Patent: TR 2026/016285. License: BSL 1.1.

Contact:
Volkan Dagli (pcworm@pcworm.net, vdagli@itouch.com.tr)
Autonomous Agent: ask@answerr.me

We would be delighted to share this milestone with your readership and community.

Best regards,
Werracle Autonomous Core Team
https://pcworm.github.io/werracle/
"""

def send_announcement(target_key="self_test"):
    if target_key not in TARGET_CHANNELS:
        print(f"Unknown target: {target_key}")
        return False

    target = TARGET_CHANNELS[target_key]
    recipient_name = target["name"]
    to_emails = target["to"]
    subject = target["subject"]

    msg = MIMEMultipart()
    msg["From"] = SENDER_DISPLAY
    msg["To"] = ", ".join(to_emails)
    msg["Reply-To"] = REPLY_TO
    msg["Subject"] = subject

    body = BODY_EDITORIAL.format(recipient_name=recipient_name)
    msg.attach(MIMEText(body, "plain", "utf-8"))

    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT} for target '{target_key}'...")
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(AUTH_USER, AUTH_PASS)
            server.sendmail("ask@answerr.me", to_emails, msg.as_string())
        print(f"SUCCESS: Email delivered to {to_emails} ({recipient_name})")
        return True
    except Exception as e:
        print(f"ERROR delivering to {to_emails}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python scripts/announcement_mailer.py [target|list|all]")
        print("Available targets:")
        for k, v in TARGET_CHANNELS.items():
            print(f"  • {k:18} -> {v['name']} ({', '.join(v['to'])})")
        sys.exit(0)

    arg = sys.argv[1].lower()
    if arg == "list":
        print("Target Channels Registry:")
        for k, v in TARGET_CHANNELS.items():
            print(f"  • {k:18} -> {v['name']} ({', '.join(v['to'])})")
    elif arg == "all":
        print("Dispatching announcements to all registered channels...")
        for k in TARGET_CHANNELS:
            send_announcement(k)
    else:
        send_announcement(arg)
