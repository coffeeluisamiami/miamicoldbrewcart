"""
CMO Agent Runner
Orchestrates marketing goals, delegates content planning to Content Planner Agent,
and routes finished proposal packages to Email Writer Agent for branded Gmail delivery.
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
PLANNER_SCRIPT = Path(__file__).parent.parent / "content-planner-agent" / "content_planner.py"
EMAIL_WRITER_DIR = ROOT_DIR / ".agent" / "email-writer"
sys.path.append(str(EMAIL_WRITER_DIR.resolve()))

try:
    from email_writer import send_proposal_email
except ImportError:
    send_proposal_email = None

def delegate_content_planning(topic: str):
    """Delegates content marketing research to Content Planner Agent."""
    if not PLANNER_SCRIPT.exists():
        raise FileNotFoundError(f"Content Planner tool not found at {PLANNER_SCRIPT}")

    cmd = ["python", str(PLANNER_SCRIPT), "--niche", topic, "--plan"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        try:
            return json.loads(res.stdout)
        except json.JSONDecodeError:
            return {"raw_output": res.stdout}
    return {"error": res.stderr}

def route_proposal_to_email_writer(
    proposal_content: str,
    first_name: str,
    business_name: str,
    email: str,
    bottleneck: str = ""
) -> bool:
    """
    Step 05-06: CMO receives proposal package from CSO and routes to Email Writer.
    Reports send confirmation back to CSO.
    """
    print(f"\n[CMO Agent] Received proposal package for {first_name} ({business_name}) at {email}")
    print(f"[CMO Agent] Routing to specialist: Email Writer (.agent/email-writer/)...")

    bridge_sentence = f"We specifically reviewed your challenge with '{bottleneck or 'operational bottlenecks'}' and designed this engagement to solve it."
    
    if send_proposal_email:
        sent = send_proposal_email(
            to_email=email,
            first_name=first_name,
            business_name=business_name,
            bridge_sentence=bridge_sentence,
            proposal_content=proposal_content
        )
    else:
        # Fallback to subprocess execution
        writer_script = EMAIL_WRITER_DIR / "email_writer.py"
        cmd = ["python", str(writer_script), email, first_name, business_name, proposal_content]
        res = subprocess.run(cmd, capture_output=True, text=True)
        sent = res.returncode == 0

    print(f"[CMO Agent] Email Writer completed dispatch. Status: {'SUCCESS' if sent else 'FAILED'}")
    print(f"[CMO Agent] Reporting confirmation back to CSO: {sent}")
    return sent

def main():
    parser = argparse.ArgumentParser(description="CMO Agent Orchestrator")
    parser.add_argument("--campaign", help="Campaign objective or marketing topic")
    parser.add_argument("--send-proposal", action="store_true", help="Send proposal package")
    parser.add_argument("--email", help="Recipient email")
    parser.add_argument("--first-name", help="Recipient first name")
    parser.add_argument("--business", help="Business name")
    parser.add_argument("--proposal-file", help="Path to proposal content text file")
    args = parser.parse_args()

    if args.send_proposal and args.email:
        content = ""
        if args.proposal_file and Path(args.proposal_file).exists():
            with open(args.proposal_file, "r", encoding="utf-8") as f:
                content = f.read()
        sent = route_proposal_to_email_writer(
            proposal_content=content,
            first_name=args.first_name or "Prospect",
            business_name=args.business or "Your Business",
            email=args.email
        )
        print(f"Result: {sent}")
        return

    topic = args.campaign or "Miami mobile coffee cart corporate activations"
    print(f"\n[CMO Agent] Campaign Objective: \"{topic}\"")
    print(f"[CMO Agent] Delegating content planning to Content Planner Agent at .agent/content-planner-agent/...")
    
    plan = delegate_content_planning(topic)
    print("\n=== [CMO Agent] Marketing Strategy & Content Plan Collected ===")
    print(json.dumps(plan, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
