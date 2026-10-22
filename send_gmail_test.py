"""
Gmail Sender for Antigravity & AI Pipeline
Sends automated proposals and test emails from mcardenas.cl@gmail.com
"""

import sys
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "gmail_credentials.json"

def send_email(to_email: str, subject: str, body: str) -> bool:
    if not CONFIG_PATH.exists():
        print(f"Error: Credentials file not found at {CONFIG_PATH}")
        return False
        
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    sender_email = creds.get("email", "mcardenas.cl@gmail.com")
    app_password = creds.get("app_password", "").replace(" ", "")
    
    if not app_password:
        print("Error: app_password is empty in gmail_credentials.json")
        return False

    msg = MIMEMultipart()
    msg["From"] = f"Miami Cold Brew Cart <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        print(f"Connecting to Gmail SMTP server for {sender_email}...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"SUCCESS: Email sent to {to_email}!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = "Pipeline test"
    body = f"The Gmail connection works. Verification timestamp: {today_str}"
    
    # Test send to own email
    target = "mcardenas.cl@gmail.com"
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    send_email(target, subject, body)
