"""
Email Writer Agent - Miami Cold Brew Cart
Specialist under the CMO Agent.
Formats proposals into high-converting branded HTML emails with inline CSS
and dispatches them using the verified Gmail connection.
"""

import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
CREDS_FILE = ROOT_DIR / "gmail_credentials.json"

def build_branded_html_email(
    first_name: str,
    business_name: str,
    bridge_sentence: str,
    proposal_content: str,
    sender_name: str = "Marcelo Cardenas",
    tagline: str = "Miami Cold Brew Cart • Luxury Mobile Coffee & Barista Catering",
    sender_email: str = "mcardenas.cl@gmail.com",
    calendar_link: str = "https://miamicoldbrewcart.web.app/#book-event"
) -> str:
    # Format proposal content lines into HTML paragraphs and bullet list
    formatted_body = ""
    for block in proposal_content.strip().split("\n\n"):
        if block.startswith("•") or "\n•" in block:
            items = [line.strip().replace("•", "").strip() for line in block.split("\n") if line.strip()]
            formatted_body += "<ul style='margin: 14px 0; padding-left: 22px; line-height: 1.7; color: #334155;'>"
            for item in items:
                formatted_body += f"<li style='margin-bottom: 8px;'><strong>•</strong> {item}</li>"
            formatted_body += "</ul>"
        else:
            formatted_body += f"<p style='margin: 14px 0; line-height: 1.65; color: #334155; font-size: 15px;'>{block.replace(chr(10), '<br>')}</p>"

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Your Event Proposal from Miami Cold Brew Cart</title>
</head>
<body style="margin: 0; padding: 0; background-color: #faf5ee; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #faf5ee; padding: 36px 16px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 620px; background-color: #ffffff; border-radius: 16px; overflow: hidden; border: 1px solid #e7dfd5; box-shadow: 0 10px 30px rgba(78, 42, 12, 0.08);">
          
          <!-- (1) Branded Colored Header Banner -->
          <tr>
            <td style="background: linear-gradient(135deg, #78350f 0%, #ea580c 50%, #f59e0b 100%); padding: 36px 30px; text-align: left;">
              <span style="display: inline-block; background-color: rgba(255,255,255,0.2); color: #ffffff; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; padding: 4px 10px; border-radius: 20px; margin-bottom: 10px;">Event Catering Proposal</span>
              <h1 style="margin: 0; font-size: 26px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px;">Miami Cold Brew Cart</h1>
              <p style="margin: 6px 0 0; font-size: 13px; color: #fed7aa; font-weight: 500;">In Partnership with Luisa Coffee & Miami Coffee Cart</p>
            </td>
          </tr>

          <!-- Body Content Area -->
          <tr>
            <td style="padding: 34px 30px;">
              <!-- (2) Personalized opening -->
              <p style="margin: 0 0 14px; font-size: 17px; font-weight: 800; color: #1e1b18;">
                Hi {first_name}, thank you for inquiring about {business_name}!
              </p>

              <!-- (3) One-sentence bridge -->
              <div style="background-color: #fffbeb; border-left: 4px solid #ea580c; padding: 14px 18px; margin-bottom: 24px; border-radius: 6px;">
                <p style="margin: 0; font-size: 14px; font-weight: 600; color: #92400e; line-height: 1.5;">
                  ☕ {bridge_sentence}
                </p>
              </div>

              <!-- (4) Clean HTML proposal content -->
              <div style="color: #334155;">
                {formatted_body}
              </div>

              <!-- (5) Highlighted Call-To-Action Box -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 32px 0 24px; background: linear-gradient(135deg, #fff7ed 0%, #fef3c7 100%); border: 2px solid #fed7aa; border-radius: 14px; text-align: center; padding: 26px 20px;">
                <tr>
                  <td>
                    <h3 style="margin: 0 0 8px; font-size: 19px; font-weight: 900; color: #78350f;">Ready to reserve your event date?</h3>
                    <p style="margin: 0 0 18px; font-size: 14px; color: #92400e;">Dates fill quickly in South Florida. Lock in your mobile coffee bar setup today.</p>
                    <a href="{calendar_link}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #ea580c 0%, #d97706 100%); color: #ffffff; font-size: 15px; font-weight: 800; text-decoration: none; padding: 13px 32px; border-radius: 10px; box-shadow: 0 6px 18px rgba(234, 88, 12, 0.35);">Lock In Your Event Date &rarr;</a>
                  </td>
                </tr>
              </table>

              <!-- (6) Footer -->
              <div style="border-top: 1px solid #e7dfd5; padding-top: 22px; margin-top: 28px; text-align: left;">
                <p style="margin: 0; font-size: 15px; font-weight: 800; color: #1e1b18;">Jessica</p>
                <p style="margin: 2px 0 0; font-size: 13px; color: #78350f; font-weight: 600;">Coffee Specialist & Event Producer &bull; Miami Cold Brew Cart</p>
                <p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">
                  Email: <a href="mailto:cart@luisacoffee.com" style="color: #ea580c; text-decoration: none; font-weight: 600;">cart@luisacoffee.com</a> &bull; 
                  Phone: <a href="tel:+17865302517" style="color: #78350f; text-decoration: none;">+1 (786) 530-2517</a> &bull; 
                  <a href="https://luisacoffee.com" target="_blank" style="color: #78350f; text-decoration: none;">Luisa Coffee</a>
                </p>
                <p style="margin: 12px 0 0; font-size: 11px; color: #a8a29e; font-style: italic;">Specialty Cold Brew, Espresso, Matcha & Warm Refreshers serving Miami, Brickell, Coral Gables, Wynwood and Fort Lauderdale.</p>
              </div>

            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
    return html

def send_proposal_email(
    to_email: str,
    first_name: str,
    business_name: str,
    bridge_sentence: str,
    proposal_content: str,
    sender_name: str = "Marcelo Cardenas"
) -> bool:
    if not CREDS_FILE.exists():
        print(f"Error: {CREDS_FILE} not found.")
        return False

    with open(CREDS_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)

    sender_email = creds.get("email")
    app_password = creds.get("app_password")

    subject = f"Your proposal from {sender_name} -- {business_name}"
    html_content = build_branded_html_email(
        first_name=first_name,
        business_name=business_name,
        bridge_sentence=bridge_sentence,
        proposal_content=proposal_content,
        sender_name=sender_name,
        sender_email=sender_email
    )

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    plain_text = f"Hi {first_name},\n\n{bridge_sentence}\n\n{proposal_content}\n\nBest,\n{sender_name}\nMiami Cold Brew Cart"
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"[Email Writer] Successfully dispatched Miami Cold Brew Cart proposal to {to_email}!")
        return True
    except Exception as e:
        print(f"[Email Writer] Failed to send email: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python email_writer.py <email> <first_name> <business_name> <proposal_text_or_file>")
        sys.exit(1)

    dest_email = sys.argv[1]
    f_name = sys.argv[2]
    b_name = sys.argv[3]
    prop_arg = sys.argv[4]

    if Path(prop_arg).exists():
        with open(prop_arg, "r", encoding="utf-8") as f:
            proposal_body = f.read()
    else:
        proposal_body = prop_arg

    bridge = f"We reviewed your request for high-end coffee catering and prepared this custom package for {b_name}."
    send_proposal_email(dest_email, f_name, b_name, bridge, proposal_body)
