#!/usr/bin/env python3
"""
Inspect ask@answerr.me mailbox to discover bounce notices, delivery failure reports,
and past sent messages to compile an automated suppression / blacklist of dead addresses.
"""

import sys
import imaplib
import ssl
import json
import os
import re
import email
from email.header import decode_header

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

MAIL_CONFIG_PATH = os.path.expanduser("~/.answerr/mail.json")

def decode_mime_words(s):
    if not s:
        return ""
    decoded_fragments = decode_header(s)
    parts = []
    for frag, enc in decoded_fragments:
        if isinstance(frag, bytes):
            try:
                parts.append(frag.decode(enc or 'utf-8', errors='ignore'))
            except Exception:
                parts.append(frag.decode('utf-8', errors='ignore'))
        else:
            parts.append(str(frag))
    return "".join(parts)

def inspect_mailbox():
    if not os.path.exists(MAIL_CONFIG_PATH):
        print(f"Error: {MAIL_CONFIG_PATH} not found.")
        return

    with open(MAIL_CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    host = cfg.get("imap_server", "mail.answerr.me")
    port = int(cfg.get("imap_port", 993))
    user = cfg.get("email", "ask@answerr.me")
    password = cfg.get("password")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    mail = imaplib.IMAP4_SSL(host, port, ssl_context=ctx)
    mail.login(user, password)

    bounced_emails = set()
    bounce_reports = []

    folders = ["INBOX", "Junk E-mail", "Sent Items"]
    for folder in folders:
        status, count = mail.select(f'"{folder}"')
        if status != "OK":
            continue
        typ, data = mail.search(None, "ALL")
        msg_ids = data[0].split()
        print(f"\n=======================================================")
        print(f" Folder: {folder} (Total Messages: {len(msg_ids)})")
        print(f"=======================================================")

        # Scan all messages in this folder
        for num in msg_ids:
            typ, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    raw_email = response_part[1]
                    msg = email.message_from_bytes(raw_email)
                    subj = decode_mime_words(msg.get("Subject", ""))
                    from_ = decode_mime_words(msg.get("From", ""))
                    date_ = msg.get("Date", "")
                    to_ = decode_mime_words(msg.get("To", ""))

                    is_bounce = False
                    lower_subj = subj.lower()
                    lower_from = from_.lower()

                    if any(term in lower_from for term in ["mailer-daemon", "postmaster", "mail delivery subsystem"]):
                        is_bounce = True
                    if any(term in lower_subj for term in ["delivery status notification", "failure notice", "undeliverable", "returned mail", "rejected"]):
                        is_bounce = True

                    body_text = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get("Content-Disposition"))
                            if ctype == "text/plain" and "attachment" not in cdispo:
                                try:
                                    body_text += part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                except Exception:
                                    pass
                    else:
                        try:
                            body_text = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                        except Exception:
                            pass

                    if is_bounce:
                        # Extract email addresses from failure notice
                        found_emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', body_text)
                        targets = [e.lower() for e in found_emails if e.lower() not in ["ask@answerr.me", "mailer-daemon", "postmaster"]]
                        for t in targets:
                            bounced_emails.add(t)
                        bounce_reports.append({
                            "folder": folder,
                            "id": num.decode(),
                            "from": from_,
                            "subject": subj,
                            "date": date_,
                            "detected_targets": targets[:3]
                        })
                        print(f" [BOUNCE] From: {from_} | Subj: {subj} | Failed Targets: {targets[:3]}")
                    else:
                        print(f" [MSG] Date: {date_} | From: {from_[:30]} | Subj: {subj[:50]}")

    print("\n=======================================================")
    print(" SUMMARY OF BOUNCED / FAILING TARGETS:")
    print("=======================================================")
    for b in sorted(bounced_emails):
        print(f" ❌ {b}")

    print("\n=======================================================")
    print(" NOTABLE REPLIES RECEIVED:")
    print("=======================================================")
    status, count = mail.select('"INBOX"')
    for mid in [b'5', b'6']:
        try:
            typ, data = mail.fetch(mid, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            subj = decode_mime_words(msg.get("Subject", ""))
            from_ = decode_mime_words(msg.get("From", ""))
            print(f"\n[REPLY ID {mid.decode()}] From: {from_} | Subj: {subj}")
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
            print("--- Excerpt ---")
            print(body.strip()[:500])
            print("---------------")
        except Exception as e:
            print(f"Error reading mid {mid}: {e}")

    mail.logout()

    return bounced_emails, bounce_reports

if __name__ == "__main__":
    inspect_mailbox()

