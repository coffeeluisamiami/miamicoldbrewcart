"""
Scope Agent Engine - Miami Cold Brew Cart
Defines high-end mobile beverage catering scopes based on structured prospect profile.
Outputs 1-page structured event package scope to feed the Proposal Agent.
"""

import sys
import json
from typing import Dict, Any

def define_scope(profile: Dict[str, Any]) -> Dict[str, Any]:
    name = profile.get("name", "Event Host")
    business = profile.get("businessName") or profile.get("company", "Your Event")
    help_with = profile.get("helpWith") or profile.get("eventType", "Nitro Cold Brew")
    industry = profile.get("industry", "Corporate & Social Events")
    budget = profile.get("budget", "$1,000-$5,000")
    timeline = profile.get("timeline", "1-3 months")
    bottleneck = profile.get("bottleneck") or profile.get("message", "High-speed guest hospitality")

    # Catering Packages Matrix for Miami Cold Brew Cart
    packages = {
        "Nitro Cold Brew": {
            "title": "Signature Nitro Cold Brew & Iced Specialty Bar",
            "deliverables": [
                "Handcrafted wooden mobile cart with dual-tap nitrogen draft system",
                "Single-origin nitrogen-infused cold brew & ceremonial iced matcha on tap",
                "Full artisan syrup station (Tahitian vanilla, lavender honey, salted caramel)",
                "Organic oat, almond, and whole milk options",
                "2 Certified hospitality baristas providing 3 hours of unlimited rapid service",
                "Custom cups, compostable straws, ice service, and turnkey setup & cleanup"
            ],
            "typical_timeline": "3 hours unlimited guest service (1-hour setup prior)",
            "out_of_scope": "Alcoholic beverage pouring (unless coordinated with a licensed venue rider) and additional service hours beyond contract."
        },
        "Espresso Bar": {
            "title": "Full Specialty Espresso & Latte Art Bar",
            "deliverables": [
                "Commercial 2-group Italian espresso machine mounted on boutique coffee cart",
                "Complete hot espresso menu: Cortados, Flat Whites, Cappuccinos, Lattes, and Americanos",
                "Live latte art demonstrations for guests by professional baristas",
                "House-made syrups, leches vegetales (oat, almond), and organic whole milk",
                "3 hours of unlimited barista service with premium ceramic or branded takeaway cups",
                "Dedicated quiet power station and self-contained water filtration"
            ],
            "typical_timeline": "3 hours continuous espresso service",
            "out_of_scope": "Gasoline generators indoors or outdoor setups lacking overhead rain shelter."
        },
        "Matcha & Refreshers": {
            "title": "Ceremonial Matcha & Tropical Refresher Activation",
            "deliverables": [
                "Premium Uji ceremonial-grade matcha whisked fresh to order (iced or warm)",
                "Handcrafted tropical refresher bar: Strawberry Hibiscus, Mango Passionfruit, Yuzu Mint",
                "Boutique cart presentation with tropical Miami floral staging",
                "2 Experienced baristas serving 150+ guests per hour with zero line congestion",
                "All cups, sleeves, eco-straws, and customized menu signage included"
            ],
            "typical_timeline": "3 hours high-throughput beverage activation",
            "out_of_scope": "Full food catering or hot breakfast prep."
        },
        "Hot Chocolate Bar": {
            "title": "Winter Gourmet Hot Chocolate & Warm Beverage Bar",
            "deliverables": [
                "Rich European-style melted chocolate & velvety Swiss cocoa bars",
                "Gourmet toppings: hand-torched artisan marshmallows, crushed peppermint, cinnamon whipped cream",
                "Festive cart dressing and cozy winter display for holiday parties and galas",
                "Full service by 2 dedicated baristas for 3 hours of warm beverage bliss"
            ],
            "typical_timeline": "3 hours holiday event service",
            "out_of_scope": "Outdoor service in unshielded heavy rain."
        }
    }

    # Intelligent mapping from form values or generic keywords to catering packages
    kw = (help_with + " " + bottleneck).lower()
    if "matcha" in kw or "refresher" in kw or "content" in kw:
        selected = packages["Matcha & Refreshers"]
    elif "espresso" in kw or "hot coffee" in kw or "latte" in kw or "lead" in kw:
        selected = packages["Espresso Bar"]
    elif "hot chocolate" in kw or "winter" in kw or "cocoa" in kw or "custom" in kw:
        selected = packages["Hot Chocolate Bar"]
    else:
        # Default & Automation maps to high-speed Nitro Cold Brew
        selected = packages["Nitro Cold Brew"]

    return {
        "client": {
            "name": name,
            "business": business,
            "industry": industry,
            "stated_bottleneck": bottleneck,
            "stated_budget": budget,
            "stated_timeline": timeline
        },
        "recommended_service": selected["title"],
        "core_deliverables": selected["deliverables"],
        "timeline_estimate": selected["typical_timeline"],
        "out_of_scope": selected["out_of_scope"]
    }

if __name__ == "__main__":
    test_profile = {
        "name": "Maria Rodriguez",
        "businessName": "Wynwood Art Gallery",
        "helpWith": "Nitro Cold Brew",
        "industry": "Art & Luxury Events",
        "budget": "$1,000-$5,000",
        "timeline": "1-3 months",
        "bottleneck": "Need to serve 150 attendees fast without long lines during VIP opening"
    }
    print(json.dumps(define_scope(test_profile), indent=2))
