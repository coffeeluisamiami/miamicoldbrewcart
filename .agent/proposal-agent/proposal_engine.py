"""
Proposal Agent Engine - Miami Cold Brew Cart
Drafts personalized, high-converting beverage catering proposals for events,
quoting specific client requirements and detailing the mobile cart experience.
"""

import sys
import json
from typing import Dict, Any

def generate_proposal(profile: Dict[str, Any], scope: Dict[str, Any]) -> str:
    name = profile.get("name", "there")
    first_name = name.split(" ")[0]
    business = profile.get("businessName") or profile.get("company", "your upcoming event")
    bottleneck = profile.get("bottleneck") or profile.get("message", "flawless guest hospitality")
    service_title = scope.get("recommended_service", "Signature Mobile Beverage Bar")
    deliverables = scope.get("core_deliverables", [])
    timeline = scope.get("timeline_estimate", "3 hours unlimited service")
    budget = profile.get("budget", "$1,000-$5,000")

    deliv_formatted = "\n".join([f"• {d}" for d in deliverables])

    pitch = f"""Hey {first_name},

Thank you for reaching out about bringing the coffee cart experience to {business}!

We reviewed your event details and noted that your primary priority is:
"{bottleneck}"

Delivering rapid, world-class guest hospitality with zero line congestion is exactly what we specialize in. For {business}, we have engineered our {service_title}.

Here is what your all-inclusive event package includes:

{deliv_formatted}

Service Duration: {timeline} with seamless 1-hour setup and full breakdown included.
Budget Alignment: Fully structured to deliver five-star hospitality well within your {budget} range.

What is Out of Scope:
{scope.get("out_of_scope", "Alcoholic beverage pouring without separate venue rider, and uncontracted extra hours.")}

Next Step:
Let's lock in your date on our calendar before the weekend books up. Click the booking link below or reply directly to this email to reserve your cart setup.

Warm regards,
Marcelo Cardenas
Founder & Event Director
Miami Cold Brew Cart • An Experiential Branch of Luisa Coffee & Miami Coffee Cart
mcardenas.cl@gmail.com
"""
    return pitch

if __name__ == "__main__":
    sample_profile = {
        "name": "Maria Rodriguez",
        "businessName": "Wynwood Art Gallery",
        "bottleneck": "Need to serve 150 attendees fast without long lines during VIP opening",
        "budget": "$1,000-$5,000"
    }
    sample_scope = {
        "recommended_service": "Signature Nitro Cold Brew & Iced Specialty Bar",
        "core_deliverables": [
            "Handcrafted wooden mobile cart with dual-tap nitrogen draft system",
            "Single-origin nitrogen-infused cold brew & ceremonial iced matcha on tap",
            "Full artisan syrup station (Tahitian vanilla, lavender honey, salted caramel)",
            "2 Certified hospitality baristas providing 3 hours of unlimited rapid service"
        ],
        "timeline_estimate": "3 hours unlimited guest service",
        "out_of_scope": "Alcoholic beverage pouring and extra hours beyond contract."
    }
    print(generate_proposal(sample_profile, sample_scope))
