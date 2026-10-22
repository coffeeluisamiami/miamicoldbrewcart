"""
CSO Agent Runner
Orchestrates sales goals, manages business profile, delegates outbound tasks
to Lead Gen Agent (.agent/lead-gen-agent/), and coordinates client delivery pipeline
across Scope Agent (.agent/scope-agent/), Proposal Agent (.agent/proposal-agent/),
and CMO Agent (.agent/cmo-agent/).
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

PROFILE_PATH = Path(__file__).parent / "business_profile.json"
LEAD_GEN_SCRIPT = Path(__file__).parent.parent / "lead-gen-agent" / "research_prospect.py"
PIPELINE_MODULE = Path(__file__).parent / "cso_pipeline.py"

sys.path.append(str(Path(__file__).parent.resolve()))
try:
    from cso_pipeline import process_submission_pipeline
except ImportError:
    process_submission_pipeline = None

def load_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_profile(business: str, icp: str, offer: str):
    data = {
        "business": business,
        "ideal_customer_profile": icp,
        "offer": offer
    }
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data

def delegate_research(target_query: str):
    """Invokes the Lead Gen Agent script to perform public web research."""
    if not LEAD_GEN_SCRIPT.exists():
        raise FileNotFoundError(f"Lead Gen tool not found at {LEAD_GEN_SCRIPT}")
        
    cmd = [
        "python",
        str(LEAD_GEN_SCRIPT),
        "--search",
        target_query
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        try:
            return json.loads(res.stdout)
        except json.JSONDecodeError:
            return {"raw_output": res.stdout}
    return {"error": res.stderr}

def main():
    parser = argparse.ArgumentParser(description="CSO Agent Orchestrator")
    parser.add_argument("--goal", help="Sales goal or target directive")
    parser.add_argument("--init", action="store_true", help="Initialize or update business profile")
    parser.add_argument("--submission", help="Path to JSON submission file or JSON string")
    parser.add_argument("--test-pipeline", action="store_true", help="Run full client delivery pipeline test")
    args = parser.parse_args()

    # Client Delivery Pipeline Upgrade
    if args.test_pipeline or args.submission:
        if args.submission:
            if Path(args.submission).exists():
                with open(args.submission, "r", encoding="utf-8") as f:
                    sub_data = json.load(f)
            else:
                sub_data = json.loads(args.submission)
        else:
            sub_data = {
                "name": "Alex Rivera",
                "businessName": "Rivera Growth Agency",
                "email": "mcardenas.cl@gmail.com",
                "helpWith": "Lead Generation",
                "industry": "ecommerce",
                "budget": "$5,000-$10,000",
                "timeline": "1-3 months",
                "bottleneck": "Manual prospect research taking 15 hours every week"
            }
        
        print("\n=== [CSO Agent] Running Client Delivery Pipeline ===")
        if process_submission_pipeline:
            result = process_submission_pipeline(sub_data, auto_send=True)
            print(f"[CSO Agent] Pipeline execution completed. Email sent: {result['email_sent']}")
            print(f"[CSO Agent] client-package.md generated at: {result['package_file']}")
        return

    # Original Session 09 Functionality (Preserved)
    profile = load_profile()
    if not profile or args.init:
        print("=== CSO Agent Onboarding ===")
        print("Business profile not configured. Please supply your details:")
        biz = input("1. What is your business? ").strip()
        icp = input("2. Who is your ideal customer (ICP)? ").strip()
        offer = input("3. What is your core offer? ").strip()
        profile = save_profile(biz, icp, offer)
        print("\n[CSO] Profile saved successfully!\n")

    if args.goal:
        print(f"\n[CSO Agent] Processing Goal: \"{args.goal}\"")
        print(f"[CSO Agent] ICP: {profile['ideal_customer_profile']}")
        print(f"[CSO Agent] Delegating research to Lead Gen Agent at .agent/lead-gen-agent/...")
        
        target_query = f"{args.goal} {profile['ideal_customer_profile']}"
        intel = delegate_research(target_query)
        
        print("\n=== [CSO Agent] Results Collected from Lead Gen Agent ===")
        print(json.dumps(intel, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
