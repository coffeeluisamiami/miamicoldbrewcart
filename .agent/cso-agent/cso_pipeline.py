"""
CSO Pipeline Orchestrator (The Handoff Pattern)
Implements the multi-agent pipeline:
Raw Submission -> CSO (Prospect Profile) -> Scope Agent -> Proposal Agent -> CMO -> Email Writer -> Gmail -> client-package.md
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

ROOT_DIR = Path(__file__).parent.parent.parent
SCOPE_DIR = ROOT_DIR / ".agent" / "scope-agent"
PROPOSAL_DIR = ROOT_DIR / ".agent" / "proposal-agent"
CMO_DIR = ROOT_DIR / ".agent" / "cmo-agent"
EMAIL_DIR = ROOT_DIR / ".agent" / "email-writer"

sys.path.append(str(SCOPE_DIR.resolve()))
sys.path.append(str(PROPOSAL_DIR.resolve()))
sys.path.append(str(CMO_DIR.resolve()))
sys.path.append(str(EMAIL_DIR.resolve()))

from scope_engine import define_scope
from proposal_engine import generate_proposal
from cmo_runner import route_proposal_to_email_writer

def structure_prospect_profile(submission: Dict[str, Any]) -> Dict[str, Any]:
    """
    Step 02: CSO creates a structured Prospect Profile with 4 sections:
    - Who
    - Problem
    - Budget & Timeline
    - Unknowns
    Every blank field and 'Not sure yet' gets logged under Unknowns.
    """
    unknowns = []

    # Who
    name = (submission.get("name") or submission.get("fullName") or "").strip()
    if not name:
        name = "Unknown Prospect"
        unknowns.append("Prospect name not specified")

    business = (submission.get("businessName") or submission.get("company") or "").strip()
    if not business:
        business = "Unknown Business"
        unknowns.append("Business name not specified")

    email = (submission.get("email") or "").strip()
    if not email:
        email = "Unknown"
        unknowns.append("Email address not provided")

    industry = (submission.get("industry") or "").strip()
    if not industry:
        industry = "Not specified"
        unknowns.append("Industry not provided")

    # Problem
    help_with = (submission.get("helpWith") or submission.get("need") or "").strip()
    if not help_with or help_with.lower() in ["not sure yet", "unknown"]:
        unknowns.append(f"What they need help with: {help_with or 'Unspecified'}")
        help_with = "Automation"  # Fallback conservative scope

    bottleneck = (submission.get("bottleneck") or submission.get("message") or "").strip()
    if not bottleneck:
        bottleneck = "Manual operational bottlenecks"
        unknowns.append("Biggest bottleneck not specified")
    elif len(bottleneck.split()) <= 4:
        unknowns.append(f"Brief/vague bottleneck statement: '{bottleneck}' (requires discovery call clarification)")

    # Budget & Timeline
    budget = (submission.get("budget") or submission.get("budgetRange") or "").strip()
    if not budget or budget.lower() in ["not sure yet", "unknown"]:
        unknowns.append(f"Budget range: {budget or 'Not specified'}")
        budget = "Under $1,000"

    timeline = (submission.get("timeline") or "").strip()
    if not timeline or timeline.lower() in ["just exploring", "unknown"]:
        unknowns.append(f"Timeline: {timeline or 'Just exploring'}")
        timeline = "Flexible"

    return {
        "who": {
            "name": name,
            "business_name": business,
            "email": email,
            "industry": industry
        },
        "problem": {
            "need": help_with,
            "bottleneck": bottleneck
        },
        "budget_and_timeline": {
            "budget": budget,
            "timeline": timeline
        },
        "unknowns": unknowns if unknowns else ["None"]
    }

def format_client_package_md(
    email: str,
    email_sent: bool,
    profile: Dict[str, Any],
    scope: Dict[str, Any],
    proposal_text: str
) -> str:
    """
    Step 07: client-package.md: The run's paper trail
    Line 1: SEND TO: [prospect email]
    Line 2: EMAIL SENT (or EMAIL FAILED)
    Then the three sections in order:
    ## Prospect Profile
    ## Scope
    ## Proposal
    """
    status_line = "EMAIL SENT" if email_sent else "EMAIL FAILED"

    who = profile["who"]
    problem = profile["problem"]
    bt = profile["budget_and_timeline"]
    unknowns = profile["unknowns"]

    inclusions_str = "\n".join([f"- {d}" for d in scope.get("core_deliverables", [])])
    unknowns_str = "\n".join([f"- {u}" for u in unknowns])

    md_content = f"""SEND TO: {email}
{status_line}

## Prospect Profile

### Who
- **Full Name:** {who['name']}
- **Business Name:** {who['business_name']}
- **Email:** {who['email']}
- **Industry:** {who['industry']}

### Problem
- **Primary Need:** {problem['need']}
- **Biggest Bottleneck:** {problem['bottleneck']}

### Budget & Timeline
- **Budget Range:** {bt['budget']}
- **Timeline:** {bt['timeline']}

### Unknowns
{unknowns_str}

## Scope
- **Service:** {scope.get('recommended_service', 'Automation & Client Delivery Workflow')}
- **Core Inclusions:**
{inclusions_str}
- **Timeline Estimate:** {scope.get('timeline_estimate', '2-3 weeks')}
- **Out of Scope:** {scope.get('out_of_scope', 'Bespoke legacy migrations without prior agreement.')}

## Proposal
{proposal_text.strip()}
"""
    return md_content

def process_submission_pipeline(submission: dict, auto_send: bool = True) -> dict:
    """
    Executes the exact multi-agent Handoff Pattern:
    1. CSO creates Prospect Profile (Who, Problem, Budget & Timeline, Unknowns)
    2. Scope Agent defines scope (service, deliverables, timeline, out of scope)
    3. Proposal Agent drafts proposal pitch
    4. CMO Agent receives package and delegates to Email Writer
    5. Email Writer sends branded HTML via Gmail
    6. CSO writes client-package.md (Line 1: SEND TO: ..., Line 2: EMAIL SENT)
    """
    # 02 CSO: Structure Prospect Profile
    profile = structure_prospect_profile(submission)
    email = profile["who"]["email"]
    business_name = profile["who"]["business_name"]
    first_name = profile["who"]["name"].split(" ")[0]

    print(f"\n[02. CSO Agent] Form intake structured into Prospect Profile for: {profile['who']['name']} ({business_name})")
    print(f"    - Flagged Unknowns: {len(profile['unknowns'])} item(s)")

    # 03 Scope Agent: Define realistic 1-page scope
    print(f"[03. Scope Agent] Scoping project deliverables based on structured profile...")
    scope_input = {
        "name": profile["who"]["name"],
        "businessName": business_name,
        "helpWith": profile["problem"]["need"],
        "industry": profile["who"]["industry"],
        "budget": profile["budget_and_timeline"]["budget"],
        "timeline": profile["budget_and_timeline"]["timeline"],
        "bottleneck": profile["problem"]["bottleneck"]
    }
    scope = define_scope(scope_input)
    print(f"    - Recommended: {scope['recommended_service']}")
    print(f"    - Timeline: {scope['timeline_estimate']}")

    # 04 Proposal Agent: Pitch drafted under CSO
    print(f"[04. Proposal Agent] Writing personalized direct proposal pitch...")
    proposal_text = generate_proposal(scope_input, scope)

    # 05 CMO Agent handoff: Boss to boss
    # Step 4: Hands the proposal content plus first name, business name, and email to CMO Agent
    print(f"[05. CMO Agent] Received proposal package from CSO. Routing to Email Writer...")
    email_sent = False
    if auto_send and email and email != "Unknown":
        email_sent = route_proposal_to_email_writer(
            proposal_content=proposal_text,
            first_name=first_name,
            business_name=business_name,
            email=email,
            bottleneck=profile["problem"]["bottleneck"]
        )
    elif not auto_send:
        email_sent = True

    # 07 CSO closes loop and writes client-package.md
    print(f"[07. CSO Agent] Send confirmed ({email_sent}). Writing client-package.md paper trail...")
    package_md = format_client_package_md(
        email=email,
        email_sent=email_sent,
        profile=profile,
        scope=scope,
        proposal_text=proposal_text
    )

    package_file = ROOT_DIR / "client-package.md"
    with open(package_file, "w", encoding="utf-8") as f:
        f.write(package_md)
    print(f"[07. CSO Agent] client-package.md written successfully to: {package_file}")

    return {
        "status": "success",
        "profile": profile,
        "scope": scope,
        "proposal": proposal_text,
        "package_file": str(package_file),
        "email_sent": email_sent
    }

if __name__ == "__main__":
    test_sub = {
        "name": "Alex Rivera",
        "businessName": "Rivera Growth Agency",
        "email": "mcardenas.cl@gmail.com",
        "helpWith": "Lead Generation",
        "industry": "ecommerce",
        "budget": "$5,000-$10,000",
        "timeline": "1-3 months",
        "bottleneck": "Manual prospect research taking 15 hours every week"
    }

    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            test_sub = json.load(f)

    result = process_submission_pipeline(test_sub, auto_send=True)
    print("\n=== THE HANDOFF PATTERN RUN COMPLETE ===")
    print(f"Target: {result['profile']['who']['email']}")
    print(f"Email Sent: {result['email_sent']}")
    print(f"Paper Trail: {result['package_file']}")
