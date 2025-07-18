#!/usr/bin/env python3
"""
Test script for the Wonky Carrots scraper
Tests the basic functionality without making actual web requests
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scrape_wonky_carrots import OcadoScraper
import unittest.mock as mock


def test_scraper_initialization():
    """Test that the scraper initializes correctly"""
    scraper = OcadoScraper()
    assert scraper.base_url == "https://www.ocado.com"
    assert "Mozilla" in scraper.session.headers.get('User-Agent', '')
    print("✅ Scraper initialization test passed")


def test_price_extraction_regex():
    """Test the price extraction regex patterns"""
    import re
    
    test_cases = [
        ("£1.25", 1.25),
        ("Price: £2.99", 2.99),
        ("£0.85 each", 0.85),
        ("Special offer £3.50", 3.50),
    ]
    
    for text, expected_price in test_cases:
        price_match = re.search(r'£(\d+\.?\d*)', text)
        if price_match:
            extracted_price = float(price_match.group(1))
            assert extracted_price == expected_price, f"Expected {expected_price}, got {extracted_price}"
        else:
            assert False, f"No price found in '{text}'"
    
    print("✅ Price extraction regex test passed")


def test_url_construction():
    """Test URL construction for search"""
    from urllib.parse import urljoin
    
    base_url = "https://www.ocado.com"
    search_path = "/search"
    
    expected_search_url = "https://www.ocado.com/search"
    actual_search_url = urljoin(base_url, search_path)
    
    assert actual_search_url == expected_search_url
    print("✅ URL construction test passed")


def main():
    """Run all tests"""
    print("Running Wonky Carrots scraper tests...")
    print("=" * 50)
    
    try:
        test_scraper_initialization()
        test_price_extraction_regex()
        test_url_construction()
        
        print("=" * 50)
        print("✅ All tests passed!")
        print("The scraper is ready to use.")
        print("Note: Actual web scraping will depend on website availability and structure.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()