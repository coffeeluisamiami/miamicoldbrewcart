"""
Playwright-powered public research tool for Lead Gen Agent.
Scrapes and inspects public web profiles and niche pages (Instagram, LinkedIn public posts, YouTube, etc.)
WITHOUT ever logging into any account.
"""

import sys
import json
import argparse
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright

def inspect_public_url(url: str, timeout_ms: int = 20000) -> Dict[str, Any]:
    """
    Visits a public URL, extracts title, meta description, visible headings,
    and key text snippets without authenticating.
    """
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "headings": [],
        "text_snippets": [],
        "public_posts_or_highlights": [],
        "status": "success",
        "notes": ""
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            page.wait_for_timeout(2000)  # brief wait for client rendering
            
            # Check for aggressive login walls (e.g., LinkedIn / Instagram force redirects)
            current_url = page.url.lower()
            if "login" in current_url or "signin" in current_url or "auth" in current_url:
                result["status"] = "login_wall_detected"
                result["notes"] = "Page redirected to login. Skipped per safe scraping protocol."
                browser.close()
                return result

            result["title"] = page.title()
            
            # Meta description
            meta_desc = page.locator("meta[name='description']").get_attribute("content")
            if meta_desc:
                result["meta_description"] = meta_desc
                
            # Extract top headings
            headings = page.locator("h1, h2, h3").all_inner_texts()
            result["headings"] = [h.strip() for h in headings if h.strip()][:10]
            
            # Extract paragraphs / posts
            paragraphs = page.locator("p, article, span").all_inner_texts()
            clean_paras = [p.strip() for p in paragraphs if len(p.strip()) > 30]
            result["text_snippets"] = clean_paras[:8]
            
        except Exception as e:
            result["status"] = "error"
            result["notes"] = str(e)
        finally:
            browser.close()
            
    return result

def search_public_intel(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Uses DuckDuckGo HTML search to locate public LinkedIn, YouTube, Instagram profiles or niche leads.
    """
    search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    found = []
    
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
                    found.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })
        except Exception as e:
            sys.stderr.write(f"Search error: {e}\n")
        finally:
            browser.close()
            
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Public research tool using Playwright")
    parser.add_argument("--url", help="Direct public URL to inspect")
    parser.add_argument("--search", help="Search query for public prospects (e.g. 'site:linkedin.com/in \"coffee roaster\"')")
    
    args = parser.parse_args()
    
    if args.url:
        data = inspect_public_url(args.url)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.search:
        data = search_public_intel(args.search)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        parser.print_help()
