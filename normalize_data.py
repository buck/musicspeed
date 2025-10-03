#!/usr/bin/env python3
"""
Normalize music data: fix capitalization, expand abbreviations, parse multi-valued dances
"""

import json
import re

# Read raw data
with open('music_data_raw.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Dance abbreviation mappings
DANCE_ABBREV = {
    '2STEP': 'Texas Two Step',
    'TWOSTEP': 'Texas Two Step',
    'JITT': 'Jitterbug',
    'JITTBUG': 'Jitterbug',
    'WLTZ': 'Waltz',
    'SWING': 'Swing',
    'SWNG': 'Swing',
    'FXTRT': 'Foxtrot',
    'FOXTROT': 'Foxtrot',
    'SLOW DANCE': 'Slow Dance',
    'SLOW D': 'Slow Dance',
    'WALTZ': 'Waltz',
    'WHIP': 'Whip',
    'POLKA': 'Polka',
    'SLOW POLKA': 'Slow Polka',
    'FAST POLKA': 'Fast Polka',
    'FASTEST POLKA': 'Fastest Polka',
    'MAMBO': 'Mambo',
    'RUMBA': 'Rumba',
    'CHA CHA': 'Cha Cha',
    'CHACHA': 'Cha Cha',
    'SAMBA': 'Samba',
    'TANGO': 'Tango',
    'MERENGUE': 'Merengue',
    'LINDY': 'Lindy Hop',
    'JITTERBUG': 'Jitterbug',
    'VIENNESE WLTZ': 'Viennese Waltz',
    'WEST WALTZ': 'Western Waltz',
    'SLO TWOSTEP': 'Slow Two Step',
    'FAST SWING': 'Fast Swing',
}

def normalize_title(text):
    """Normalize song title to title case"""
    # Remove extra whitespace including newlines
    text = ' '.join(text.split())
    # Title case
    words = text.split()
    normalized = []
    for i, word in enumerate(words):
        # Keep certain words lowercase if not first word
        if i > 0 and word.lower() in ['a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'from', 'by', 'and', 'or', 'but']:
            normalized.append(word.lower())
        else:
            # Title case
            normalized.append(word.capitalize())
    return ' '.join(normalized)

def normalize_artist(text):
    """Normalize artist name"""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Title case but handle special cases
    return text.title()

def parse_dances(text):
    """Parse dance field and return list of normalized dance names"""
    # Split on comma or slash
    parts = re.split(r'[,/]', text)
    dances = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Look up abbreviation
        normalized = DANCE_ABBREV.get(part.upper(), part)
        if normalized not in dances:  # Avoid duplicates
            dances.append(normalized)
    return dances

# Normalize all records
normalized_data = []
for record in raw_data:
    normalized = {
        'song_title': normalize_title(record['song']),
        'artist': normalize_artist(record['artist']),
        'bpm': record['bpm'],
        'dances': parse_dances(record['dances'])
    }
    normalized_data.append(normalized)

# Save normalized data
with open('music_data_normalized.json', 'w', encoding='utf-8') as f:
    json.dump(normalized_data, f, indent=2, ensure_ascii=False)

print(f"Normalized {len(normalized_data)} records")
print("\n=== Sample normalized records ===")
for i in [0, 5, 10, 20, -1]:
    rec = normalized_data[i]
    print(f"\n{rec['song_title']}")
    print(f"  Artist: {rec['artist']}")
    print(f"  BPM: {rec['bpm']}")
    print(f"  Dances: {', '.join(rec['dances'])}")
