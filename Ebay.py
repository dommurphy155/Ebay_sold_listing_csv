import re
import time
import random
import csv
from datetime import datetime
from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# CONFIG
MAX_SCROLLS = 6
WAIT_ITEM_TIMEOUT = 15
TOP_DISPLAY = 20

# UTILITY
def log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

def clean_title(text: str) -> str:
    """Cleans up raw eBay title and removes junk metadata."""
    if not text: return "N/A"
    
    junk_phrases = [
        r"Opens in a new window or tab",
        r"New listing",
        r"Pre-owned",
        r"Brand new",
        r"Buy It Now",
        r"View similar active items",
        r"Sell one like this",
        r"Last one",
        r"or Best Offer",
        r"Sponsored",
        r"product ratings",
        r"out of 5 stars"
    ]
    
    for phrase in junk_phrases:
        text = re.sub(rf"(?i){phrase}", "", text)

    text = re.sub(r"(?i)Sold\s+\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    if " - " in text:
        parts = text.split(" - ")
        if len(parts) >= 2 and parts[0].strip().lower() in parts[1].strip().lower():
            text = parts[1].strip()
        elif len(parts) >= 2:
            text = parts[0].strip()

    return text

def clean_price(text: str) -> str:
    """Extracts only the price amount with symbol."""
    match = re.search(r"£[\d,.]+", text)
    return match.group(0) if match else ""

def parse_price_to_float(price_str: str) -> float:
    """Converts a price string like '£455.50' to a float."""
    try:
        clean_num = re.sub(r"[^\d.]", "", price_str)
        return float(clean_num)
    except (ValueError, TypeError):
        return 0.0

def clean_date(text: str) -> str:
    """Extracts date DD MMM YYYY."""
    match = re.search(r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})", text, re.IGNORECASE)
    return match.group(1) if match else "N/A"

def handle_cookie(driver):
    try:
        cookie = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all') or contains(., 'Consent')]"))
        )
        driver.execute_script("arguments[0].click();", cookie)
        log("🍪 Cookie banner dismissed")
        time.sleep(1)
    except TimeoutException:
        pass

def scroll_page(driver, max_scrolls=MAX_SCROLLS):
    log(f"⏫ Scrolling page {max_scrolls} times to load items")
    for i in range(1, max_scrolls + 1):
        driver.execute_script(f"window.scrollTo(0, {i*800});")
        time.sleep(random.uniform(1, 2))

def extract_item(item):
    try:
        try:
            title_elem = item.find_element(By.CSS_SELECTOR, "div.s-card__title span.su-styled-text.primary.default")
            title = clean_title(title_elem.text)
        except NoSuchElementException:
            return None

        try:
            price_elem = item.find_element(By.CSS_SELECTOR, "span.s-card__price")
            price = clean_price(price_elem.text)
        except NoSuchElementException:
            price = ""

        if not title or title == "N/A" or not price or "shop on ebay" in title.lower():
            return None

        try:
            date_elem = item.find_element(By.CSS_SELECTOR, "span.su-styled-text.positive.default")
            date = clean_date(date_elem.text)
        except NoSuchElementException:
            date = "N/A"

        try:
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            link = link.split("?")[0] if link else "N/A"
        except NoSuchElementException:
            link = "N/A"

        return {
            "title": title,
            "price": price,
            "link": link,
            "date": date
        }

    except StaleElementReferenceException:
        return None

def main():
    search_query = input("🤖 Please tell me what item you're looking for. ").strip()
    if not search_query:
        print("Search query cannot be empty.")
        return

    log(f"✅ Scrape started for: {search_query}")
    display = Display(visible=0, size=(1920,1080))
    display.start()
    driver = None

    try:
        log("🌐 Launching browser")
        options = uc.ChromeOptions()
        options.add_argument('--no-first-run')
        options.add_argument('--window-size=1920,1080')
        driver = uc.Chrome(options=options)
        driver.implicitly_wait(10)

        # Build URL
        encoded_query = search_query.replace(" ", "+")
        url = f'https://www.ebay.co.uk/sch/i.html?_nkw={encoded_query}&LH_Sold=1&LH_Complete=1&_dmd=1'
        
        log(f"🔎 Navigating to eBay")
        driver.get(url)
        time.sleep(5)

        handle_cookie(driver)
        scroll_page(driver, MAX_SCROLLS)

        log("⏳ Extracting items")
        containers = driver.find_elements(By.CSS_SELECTOR, "li.s-card")
        
        seen_links = set()
        valid_items = []
        prices_for_avg = []
        
        for item in containers:
            data = extract_item(item)
            if data and data["link"] not in seen_links and data["link"] != "N/A":
                valid_items.append(data)
                seen_links.add(data["link"])
                
                p_val = parse_price_to_float(data["price"])
                if p_val > 0:
                    prices_for_avg.append(p_val)

        log(f"✅ Found {len(valid_items)} valid listings")

        print("\n🎯 SOLD LISTINGS")
        print("-" * 50)
        
        final_list = valid_items[:TOP_DISPLAY]
        for idx, item in enumerate(final_list, 1):
            print(f"{idx}. 🏷️ {item['title']}")
            print(f"   💰 {item['price']} | 📅 Sold: {item['date']}")
            print(f"   🔗 {item['link']}\n")

        # 2. Calculate average and range
        if prices_for_avg:
            avg_price = sum(prices_for_avg) / len(prices_for_avg)
            lower_bound = avg_price * 0.95
            upper_bound = avg_price * 1.05
            print(f"🧾 Avg resale for {search_query}: £{lower_bound:,.2f} - £{upper_bound:,.2f}")

        log("💾 Saving to 'ebay_sold_listings.csv'")
        with open("ebay_sold_listings.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "price", "date", "link"])
            writer.writeheader()
            writer.writerows(valid_items)

        log("✅ Scrape completed successfully!")

    except Exception as e:
        log(f"❌ ERROR: {e}")

    finally:
        if driver: driver.quit()
        display.stop()
        log("🧹 Clean exit.")

if __name__ == "__main__":
    main()
