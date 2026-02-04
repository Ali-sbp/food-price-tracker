"""
Scrape food prices from Yandex Market for Russian cities.
"""
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from datetime import datetime
from urllib.parse import quote

# Products to scrape
PRODUCTS = {
    "Bread": "хлеб белый",
    "Milk": "молоко 3.2%",
    "Eggs": "яйца куриные",
    "Tomatoes": "помидоры",
    "Cucumbers": "огурцы",
    "Bananas": "бананы",
    "Chicken Breast": "куриная грудка",
}

# Cities/regions
REGIONS = {
    "Moscow": 213,
    "St Petersburg": 2,
    "Novosibirsk": 65,
    "Yekaterinburg": 54,
    "Kazan": 43,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}


def scrape_product_price(product_query, region_id):
    """Scrape price for a product in a specific region."""
    try:
        url = f"https://market.yandex.ru/search?text={quote(product_query)}&lr={region_id}"
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Try multiple selectors to find price
        price_selectors = [
            '[data-auto="snippet-price-current"]',
            '[data-auto="mainPrice"]',
            'span[data-auto="snippet-price"]',
            'div[data-zone-name="price"] span',
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Extract numeric price
                price_str = ''.join(c for c in price_text if c.isdigit() or c == '.')
                if price_str:
                    price = float(price_str)
                    print(f"  ✓ Found price: {price} RUB")
                    return price
        
        print(f"  ⚠ Could not find price in HTML")
        return None
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def main():
    """Main scraping function."""
    print("🔍 Starting Yandex Market scraper...\n")
    
    results = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for product_name, query in PRODUCTS.items():
        print(f"\n📦 Scraping: {product_name} ({query})")
        
        for region_name, region_id in REGIONS.items():
            print(f"  🌍 {region_name}...", end=" ")
            
            price = scrape_product_price(query, region_id)
            
            if price:
                # Determine unit
                if product_name in ["Bread", "Chicken Breast", "Tomatoes", "Cucumbers", "Bananas"]:
                    unit = "RUB/kg"
                elif product_name == "Milk":
                    unit = "RUB/l"
                elif product_name == "Eggs":
                    unit = "RUB/10pcs"
                else:
                    unit = "RUB"
                
                results.append({
                    "date": current_date,
                    "region": region_name,
                    "commodity": product_name,
                    "price": price,
                    "unit": unit,
                })
            
            # Be nice to the server
            time.sleep(random.uniform(1, 3))
    
    # Save to CSV
    if results:
        csv_path = "app/data/sample_prices.csv"
        print(f"\n💾 Saving {len(results)} records to {csv_path}")
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "region", "commodity", "price", "unit"])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"✅ Done! Scraped {len(results)} prices from Yandex Market")
    else:
        print("\n❌ No prices were scraped. Market may have changed structure or blocked request.")


if __name__ == "__main__":
    main()
