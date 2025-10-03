#!/usr/bin/env python3
"""
Scrape music speed chart from ssqq.com
"""

import re
import requests
from bs4 import BeautifulSoup

url = "https://ssqq.com/stories/speedcha.htm"

# Fetch the page
response = requests.get(url)
response.raise_for_status()
html = response.text

# Save raw HTML for inspection
with open('raw_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Raw HTML saved to raw_page.html")
print(f"HTML length: {len(html)} characters")

# Try to find the data section
soup = BeautifulSoup(html, 'html.parser')

# Look for tables
tables = soup.find_all('table')
print(f"\nFound {len(tables)} table elements")

# Look for pre-formatted text
pres = soup.find_all('pre')
print(f"Found {len(pres)} pre elements")

# Print first 5000 chars of body to see structure
body = soup.find('body')
if body:
    print("\n=== First 5000 chars of body ===")
    print(str(body)[:5000])
