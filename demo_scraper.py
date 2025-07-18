#!/usr/bin/env python3
"""
Demo script showing how the Wonky Carrots scraper would work
Uses mock HTML data to demonstrate the price extraction functionality
"""

from bs4 import BeautifulSoup
import re
import json


def demo_price_extraction():
    """Demonstrate price extraction with mock HTML"""
    
    # Mock HTML that might be found on Ocado for Wonky Carrots
    mock_html = """
    <html>
    <body>
        <div class="product-list">
            <div class="product-item">
                <h3>Wonky Carrots 1kg</h3>
                <div class="product-price">£1.25</div>
                <p>Save money and reduce waste with our wonky carrots</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    print("Demo: Extracting Wonky Carrots price from mock HTML")
    print("=" * 55)
    
    # Parse the HTML
    soup = BeautifulSoup(mock_html, 'html.parser')
    
    # Find product price
    price_element = soup.select_one('.product-price')
    if price_element:
        price_text = price_element.get_text(strip=True)
        print(f"Found price element: {price_text}")
        
        # Extract price using regex
        price_match = re.search(r'£(\d+\.?\d*)', price_text)
        if price_match:
            price = float(price_match.group(1))
            print(f"✅ Extracted price: £{price:.2f}")
            
            # Create result
            result = {
                "product": "Wonky Carrots",
                "price": price,
                "currency": "GBP",
                "source": "ocado.com",
                "demo": True
            }
            
            # Save demo result
            with open('demo_wonky_carrots_price.json', 'w') as f:
                json.dump(result, f, indent=2)
            
            print("💾 Demo result saved to demo_wonky_carrots_price.json")
            print("\nDemo result:")
            print(json.dumps(result, indent=2))
            
        else:
            print("❌ Could not extract price from text")
    else:
        print("❌ Could not find price element")


if __name__ == "__main__":
    demo_price_extraction()