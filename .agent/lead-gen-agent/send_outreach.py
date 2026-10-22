"""
Email sending module for Lead Gen Agent and pipeline agents.
Uses verified Gmail connection to send approved drafts.
"""

import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
CREDS_FILE = ROOT_DIR / "gmail_credentials.json"

def send_agent_email(to_email: str, subject: str, body: str) -> bool:
    if not CREDS_FILE.exists():
        print(f"Error: {CREDS_FILE} does not exist.")
        return False
        
    with open(CREDS_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    sender_email = creds.get("email")
    app_password = creds.get("app_password")

    msg = MIMEMultipart()
    msg["From"] = f"Miami Cold Brew Cart <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"[Lead Gen Agent] Successfully sent email to {to_email}")
        return True
    except Exception as e:
        print(f"[Lead Gen Agent] Error sending email: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python send_outreach.py <to_email> <subject> <body>")
        sys.exit(1)
    to_addr = sys.argv[1]
    subj = sys.argv[2]
    content = sys.argv[3]
    send_agent_email(to_addr, subj, content)
