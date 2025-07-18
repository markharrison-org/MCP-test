# Wonky Carrots Price Scraper

A Python script to extract the price of Wonky Carrots from www.ocado.com.

## Features

- Searches for "Wonky Carrots" on Ocado
- Extracts the current price
- Outputs the price both to console and as JSON file
- Robust error handling and multiple fallback strategies

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:

```bash
python scrape_wonky_carrots.py
```

The script will:
1. Search for Wonky Carrots on Ocado
2. Extract the price from the product page
3. Display the price in the console
4. Save the result to `wonky_carrots_price.json`

## Output

### Console Output
```
Searching for Wonky Carrots on Ocado...
Found 1 potential Wonky Carrots products
Checking product: https://www.ocado.com/products/...
✅ Found Wonky Carrots price: £1.25
💾 Price saved to wonky_carrots_price.json
```

### JSON Output
The script creates a `wonky_carrots_price.json` file with the following structure:
```json
{
  "product": "Wonky Carrots",
  "price": 1.25,
  "currency": "GBP",
  "source": "ocado.com"
}
```

## Error Handling

The script handles various scenarios:
- Network connectivity issues
- Product not found
- Price extraction failures
- Website structure changes

## Technical Details

- Uses `requests` for HTTP requests
- Uses `BeautifulSoup` for HTML parsing
- Implements multiple CSS selectors for robust price extraction
- Includes User-Agent headers to avoid blocking
- Follows best practices for web scraping