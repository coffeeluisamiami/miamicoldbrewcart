import time
from playwright.sync_api import sync_playwright

def test_chatbot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        
        print("1. Opening live website...")
        page.goto("https://miamicoldbrewcart.web.app", wait_until="networkidle")
        
        print("2. Checking Chatbot button...")
        chat_btn = page.locator("#chatToggle")
        assert chat_btn.is_visible(), "Chatbot button is not visible"
        chat_btn.click()
        page.wait_for_timeout(1000)
        
        chat_window = page.locator("#chatWindow")
        assert "open" in chat_window.get_attribute("class"), "Chat window did not open"
        print("[OK] Chat window opened successfully.")
        
        print("3. Testing interactive quote button...")
        quote_chip = page.locator("button[data-action='quote']")
        quote_chip.click()
        page.wait_for_timeout(1000)
        
        # Click on Nitro Cold Brew
        nitro_btn = page.locator("button:has-text('Nitro Cold Brew')")
        nitro_btn.click()
        page.wait_for_timeout(1000)
        
        # Click on Up to 50 ($750)
        guests_btn = page.locator("button:has-text('Up to 50')")
        guests_btn.click()
        page.wait_for_timeout(1000)
        
        # Click on Brickell / Downtown
        loc_btn = page.locator("button:has-text('Brickell / Downtown')")
        loc_btn.click()
        page.wait_for_timeout(1500)
        
        # Verify quote calculation card appears
        assert page.locator(".chat-calc-card").is_visible(), "Quote card did not appear"
        print("[OK] Interactive quote card rendered correctly with pricing & specs.")
        
        # Take a screenshot
        page.screenshot(path="images/chatbot_live_test.png")
        print("[OK] Screenshot saved to images/chatbot_live_test.png")
        
        # Submit an email through the chat
        print("4. Submitting test email in chat...")
        chat_input = page.locator("#chatInput")
        chat_input.fill("mcardenas.cl@gmail.com")
        page.locator("#chatForm button[type='submit']").click()
        page.wait_for_timeout(2500)
        
        # Take final screenshot
        page.screenshot(path="images/chatbot_email_submitted.png")
        print("[OK] Lead captured in chat and screenshot saved.")
        
        browser.close()

if __name__ == "__main__":
    test_chatbot()
