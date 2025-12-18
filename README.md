🚀 eBay Sold Listings Scraper 🕵️‍♂️💰

🔥 The Ultimate Tool to Uncover REAL SOLD Prices on eBay.co.uk! 🔥

Stop guessing what items are worth — this powerful Python script reveals exactly what people actually paid by scraping completed and sold listings directly from eBay UK. Perfect for resellers, flippers, bargain hunters, collectors, and anyone who wants true market value data! 🤑💪

✨ What It Does

• Targets only SOLD & COMPLETED items — no more fake "asking prices"
• Asks you what item to search for (e.g. "Shure SM7B", "PS5 Slim", "iPhone 14 Pro")
• Automatically bypasses eBay's anti-bot protection using stealth browser tech
• Scrolls and loads all visible listings on the page
• Cleans up messy titles — removes junk like "New listing", "or Best Offer", star ratings, etc.
• Extracts clean prices (£ only), sold dates, and direct links
• Shows you the top 20 most recent sold listings in a beautiful, easy-to-read format
• Calculates and displays a realistic average resale price range (±5%)
• Saves every single result to a CSV file (ebay_sold_listings.csv) for Excel/spreadsheet use
• Runs headlessly — perfect for servers, laptops, or cloud setups

🎯 Why This Is Awesome

• See real market trends and demand
• Spot fake/counterfeit listings with suspiciously low prices 🚩
• Make smarter buying and selling decisions
• Research pricing for flipping, collecting, or avoiding scams
• Get data that most people can’t access easily

⚡ How to Set It Up & Use It

1. Make sure you have Python 3 installed on your computer (Linux, macOS, or Windows with WSL works best)

2. Save the script as ebay_scraper.py

3. Create a file called requirements.txt in the same folder with this content:
selenium>=4.15.0
undetected-chromedriver>=3.5.5
pyvirtualdisplay>=3.0

4. Open a terminal/command prompt in that folder and run:
pip install -r requirements.txt

5. Run the script:
python ebay_scraper.py

6. When prompted, type the item you're searching for (e.g. Shure SM7B) and press Enter

7. Sit back and watch it work! You'll see live logs, then a clean list of sold items + average price range

8. Open ebay_sold_listings.csv to see all the data in spreadsheet form

🛠️ Tech Highlights

• Uses undetected-chromedriver to stay hidden from eBay's bot detection
• Runs in a virtual headless browser (no window popping up)
• Smart scrolling to load lazy items
• Robust error handling for reliability
• Updated for eBay's 2025 layout

⚠️ Important

• For personal, occasional use only
• eBay doesn't allow large-scale automated access — use responsibly and don't spam requests
• Keep the undetected-chromedriver package updated for best results
• Works best on Linux/macOS; Windows users may need WSL or adjustments

🏆 Built for deal hunters, by a deal hunter

Now go find those hidden gems and real market prices! 🚀🤑
