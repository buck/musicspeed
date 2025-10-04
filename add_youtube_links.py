#!/usr/bin/env python3
"""
Add YouTube links to songs in database
"""

import sqlite3
import subprocess
import json
import sys

def get_youtube_url(title, artist):
    """Get most viewed YouTube video URL for a song"""
    query = f"{title} {artist}"

    try:
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--playlist-end', '3', f'ytsearch3:{query}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=30
        )

        if result.returncode != 0 or not result.stdout:
            return None

        # Parse top 3 results and find most viewed
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    v = json.loads(line)
                    videos.append({
                        'url': v.get('webpage_url'),
                        'views': v.get('view_count', 0) or 0
                    })
                except:
                    pass

        if videos:
            best = max(videos, key=lambda x: x['views'])
            return best['url']

        return None
    except:
        return None

# Connect to database
conn = sqlite3.connect('music_speed.db')
cursor = conn.cursor()

# Get songs without YouTube URLs
cursor.execute('SELECT song_id, title, artist FROM songs WHERE youtube_url IS NULL LIMIT 50')
songs = cursor.fetchall()

if not songs:
    print("All songs have YouTube links!")
    sys.exit(0)

print(f"Processing {len(songs)} songs...")

count = 0
for song_id, title, artist in songs:
    print(f"  {title} by {artist}...", end=' ', flush=True)

    url = get_youtube_url(title, artist)

    if url:
        cursor.execute('UPDATE songs SET youtube_url = ? WHERE song_id = ?', (url, song_id))
        conn.commit()
        print(f"✓ {url}")
        count += 1
    else:
        print("✗")

conn.close()
print(f"\nAdded {count} YouTube links")
