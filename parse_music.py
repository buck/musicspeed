#!/usr/bin/env python3
"""
Parse music speed chart from ssqq.com HTML
"""

import re
from bs4 import BeautifulSoup

# Read the raw HTML
with open('raw_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all tables
tables = soup.find_all('table')

# Find the table with the music data (it has bgcolor="#0000FF")
music_table = None
for table in tables:
    if table.get('bgcolor') == '#0000FF':
        music_table = table
        break

if not music_table:
    print("Could not find music table!")
    exit(1)

# Get all td elements from this table
tds = music_table.find_all('td')

print(f"Found {len(tds)} td elements in music table")

# The table has 4 columns: BPM, Song Title, Artist, Suggested Dance
# Find the column that has "BEATS PERMIN" header
bpm_col = None
song_col = None
artist_col = None
dance_col = None

for i, td in enumerate(tds):
    text = td.get_text().strip()
    if 'BEATS PERMIN' in text or 'BEATS' in text and 'MIN' in text:
        bpm_col = td
        print(f"Found BPM column at td index {i}")
    elif 'SONG' in text and 'TITLE' in text:
        song_col = td
        print(f"Found Song column at td index {i}")
    elif 'ARTIST' in text:
        artist_col = td
        print(f"Found Artist column at td index {i}")
    elif 'SUGGESTED' in text and 'DANCE' in text:
        dance_col = td
        print(f"Found Dance column at td index {i}")

# Extract data from each column
def extract_column_data(td):
    """Extract all <p> tag contents from a column"""
    data = []
    for p in td.find_all('p'):
        # Get text but preserve structure
        text = p.get_text(separator=' ', strip=True)
        # Skip empty and header rows
        if not text:
            continue
        # Skip headers - be more specific
        if text == 'BEATS PERMIN':
            continue
        if 'SONG' in text and 'TITLE' in text:
            continue
        if "ARTIST's" in text or (text == 'NAME'):
            continue
        if 'SUGGESTED' in text and 'DANCE' in text:
            continue
        data.append(text)
    return data

bpms = extract_column_data(bpm_col)
songs = extract_column_data(song_col)
artists = extract_column_data(artist_col)
dances = extract_column_data(dance_col)

print(f"\nExtracted:")
print(f"  BPMs: {len(bpms)}")
print(f"  Songs: {len(songs)}")
print(f"  Artists: {len(artists)}")
print(f"  Dances: {len(dances)}")

# Combine into records
records = []
max_len = max(len(bpms), len(songs), len(artists), len(dances))

for i in range(max_len):
    record = {
        'bpm': bpms[i] if i < len(bpms) else '',
        'song': songs[i] if i < len(songs) else '',
        'artist': artists[i] if i < len(artists) else '',
        'dances': dances[i] if i < len(dances) else ''
    }
    records.append(record)

# Print first 10 records
print("\n=== First 10 records ===")
for i, rec in enumerate(records[:10]):
    print(f"{i+1}. BPM:{rec['bpm']:8} | {rec['song']:30} | {rec['artist']:20} | {rec['dances']}")

# Print last 5 records
print("\n=== Last 5 records ===")
for i, rec in enumerate(records[-5:], len(records)-4):
    print(f"{i}. BPM:{rec['bpm']:8} | {rec['song']:30} | {rec['artist']:20} | {rec['dances']}")

# Save to file
import json
with open('music_data_raw.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(records)} records to music_data_raw.json")
