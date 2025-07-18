#!/usr/bin/env python3
"""
Wonky Carrots Price Scraper for Ocado
Extracts the price of Wonky Carrots from www.ocado.com
"""

import requests
import re
from bs4 import BeautifulSoup
import json
import sys
from urllib.parse import urljoin, quote_plus


class OcadoScraper:
    def __init__(self):
        self.base_url = "https://www.ocado.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_product(self, product_name):
        """Search for a product on Ocado and return search results"""
        search_url = f"{self.base_url}/search"
        params = {
            'entry': product_name
        }
        
        try:
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error searching for product: {e}")
            return None
    
    def extract_price_from_product_page(self, product_url):
        """Extract price from a specific product page"""
        try:
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Common selectors for price on e-commerce sites
            price_selectors = [
                '.price',
                '.product-price',
                '[data-test-id="price"]',
                '.current-price',
                '.price-current',
                '[class*="price"]'
            ]
            
            for selector in price_selectors:
                price_element = soup.select_one(selector)
                if price_element:
                    price_text = price_element.get_text(strip=True)
                    # Extract price using regex
                    price_match = re.search(r'£(\d+\.?\d*)', price_text)
                    if price_match:
                        return float(price_match.group(1))
            
            return None
        except requests.RequestException as e:
            print(f"Error extracting price from product page: {e}")
            return None
    
    def find_wonky_carrots_price(self):
        """Main method to find and extract Wonky Carrots price"""
        print("Searching for Wonky Carrots on Ocado...")
        
        search_response = self.search_product("Wonky Carrots")
        if not search_response:
            return None
        
        soup = BeautifulSoup(search_response.content, 'html.parser')
        
        # Look for product links in search results
        product_links = []
        
        # Common patterns for product links
        link_selectors = [
            'a[href*="/product/"]',
            'a[href*="/products/"]',
            '.product-link',
            '[data-test-id="product-link"]'
        ]
        
        for selector in link_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    # Check if this looks like a Wonky Carrots product
                    link_text = link.get_text(strip=True).lower()
                    if 'wonky' in link_text and 'carrot' in link_text:
                        full_url = urljoin(self.base_url, href)
                        product_links.append(full_url)
        
        if not product_links:
            # Fallback: look for any price directly in search results
            print("No direct product links found, looking for prices in search results...")
            price_elements = soup.select('.price, [class*="price"]')
            for price_element in price_elements:
                # Check if this price is associated with Wonky Carrots
                parent = price_element.find_parent()
                if parent:
                    parent_text = parent.get_text(strip=True).lower()
                    if 'wonky' in parent_text and 'carrot' in parent_text:
                        price_text = price_element.get_text(strip=True)
                        price_match = re.search(r'£(\d+\.?\d*)', price_text)
                        if price_match:
                            return float(price_match.group(1))
            
            return None
        
        # Extract price from the first matching product
        print(f"Found {len(product_links)} potential Wonky Carrots products")
        for product_url in product_links:
            print(f"Checking product: {product_url}")
            price = self.extract_price_from_product_page(product_url)
            if price:
                return price
        
        return None


def main():
    """Main function to run the scraper"""
    scraper = OcadoScraper()
    
    try:
        price = scraper.find_wonky_carrots_price()
        
        if price:
            print(f"✅ Found Wonky Carrots price: £{price:.2f}")
            
            # Also output as JSON for programmatic use
            result = {
                "product": "Wonky Carrots",
                "price": price,
                "currency": "GBP",
                "source": "ocado.com"
            }
            
            with open('wonky_carrots_price.json', 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"💾 Price saved to wonky_carrots_price.json")
            
        else:
            print("❌ Could not find Wonky Carrots price on Ocado")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()