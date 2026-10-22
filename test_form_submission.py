from playwright.sync_api import sync_playwright

def submit_live_event_inquiry():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Opening https://miamicoldbrewcart.web.app/#book-event...")
        page.goto("https://miamicoldbrewcart.web.app/#book-event", wait_until="networkidle")

        print("Filling out event catering fields...")
        page.fill("#name", "Marcelo Cardenas")
        page.fill("#businessName", "Maxtron Luxury Events")
        page.fill("#email", "mcardenas.cl@gmail.com")
        page.fill("#eventLocation", "Brickell City Centre Penthouse, Miami")
        page.fill("#eventDate", "2026-11-20")
        page.select_option("#duration", "3 Hours (Recommended Event Standard)")
        page.select_option("#guestCount", "100-200 guests")
        page.select_option("#helpWith", "Signature Nitro Cold Brew Bar (Nitro & Iced Specialty Lattes)")
        page.select_option("#budget", "$1,000-$2,500")
        page.fill("#bottleneck", "Fast guest flow with zero lines, custom branded cups with Maxtron logo, oat milk focus")

        print("Submitting live event inquiry...")
        page.click("#submitBtn")
        page.wait_for_selector("#successAlert", state="visible", timeout=15000)
        print("SUCCESS: Event inquiry successfully submitted and written to Firestore!")
        browser.close()

if __name__ == "__main__":
    submit_live_event_inquiry()
