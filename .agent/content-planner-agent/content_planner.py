"""
Playwright-powered public niche and trend research tool for Content Planner Agent.
Studies public posts, YouTube channels, and social pages without ever signing in.
"""

import sys
import json
import argparse
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright

def research_niche_trends(niche_query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Searches public discussions, viral hooks, and competitor posts for a niche using DuckDuckGo HTML search.
    """
    search_url = f"https://html.duckduckgo.com/html/?q={niche_query.replace(' ', '+')}+viral+posts+content+ideas"
    trends = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        try:
            page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(1500)
            
            results = page.locator(".result")
            count = min(results.count(), max_results)
            
            for i in range(count):
                res = results.nth(i)
                title_elem = res.locator(".result__title a")
                snippet_elem = res.locator(".result__snippet")
                
                title = title_elem.inner_text().strip() if title_elem.count() > 0 else ""
                url = title_elem.get_attribute("href") if title_elem.count() > 0 else ""
                snippet = snippet_elem.inner_text().strip() if snippet_elem.count() > 0 else ""
                
                if url:
                    trends.append({
                        "hook_title": title,
                        "source_url": url,
                        "content_insight": snippet
                    })
        except Exception as e:
            sys.stderr.write(f"Trend search error: {e}\n")
        finally:
            browser.close()
            
    return trends

def generate_content_calendar(niche: str) -> Dict[str, Any]:
    """Generates ready-to-produce content calendar for Miami Cold Brew Cart & sister carts."""
    return {
        "niche": niche,
        "pillars": [
            "Behind the Scenes (18-hour cold brew steep & nitro draft pour)",
            "Event Case Studies (Brickell office activation & convention breaks)",
            "Multi-Concept Showcase (Pairing cold brew with ceremonial matcha & espresso)",
            "Event Planner Tips (How to serve 300+ guests without coffee lines)"
        ],
        "viral_hooks": [
            "Why tech conferences in Miami are replacing banquet urns with nitro cold brew carts.",
            "POV: You booked a private matcha & cold brew lounge for your Brickell office Friday.",
            "How we served 400 cold brews in 30 minutes with zero lines at Miami Beach Convention Center.",
            "The #1 mistake event planners make when calculating beverage catering."
        ]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Content Planner Agent public research")
    parser.add_argument("--niche", help="Target niche or topic to analyze")
    parser.add_argument("--plan", action="store_true", help="Generate sample content calendar")
    args = parser.parse_args()

    if args.plan and args.niche:
        data = generate_content_calendar(args.niche)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.niche:
        data = research_niche_trends(args.niche)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        parser.print_help()
