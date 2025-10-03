#!/usr/bin/env python3
"""
Create SQLite database schema and populate with music data
"""

import json
import sqlite3

# Create database
conn = sqlite3.connect('music_speed.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    bpm TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dances (
    dance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS song_dances (
    song_id INTEGER NOT NULL,
    dance_id INTEGER NOT NULL,
    PRIMARY KEY (song_id, dance_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    FOREIGN KEY (dance_id) REFERENCES dances(dance_id)
)
''')

print("Created database schema")

# Load normalized data
with open('music_data_normalized.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Insert songs and collect unique dances
unique_dances = set()
for record in data:
    for dance in record['dances']:
        unique_dances.add(dance)

# Insert dances first
print(f"\nInserting {len(unique_dances)} unique dances...")
for dance in sorted(unique_dances):
    cursor.execute('INSERT OR IGNORE INTO dances (name) VALUES (?)', (dance,))

# Get dance name to id mapping
cursor.execute('SELECT dance_id, name FROM dances')
dance_map = {name: dance_id for dance_id, name in cursor.fetchall()}

# Insert songs and relationships
print(f"Inserting {len(data)} songs...")
for record in data:
    # Insert song
    cursor.execute(
        'INSERT INTO songs (title, artist, bpm) VALUES (?, ?, ?)',
        (record['song_title'], record['artist'], record['bpm'])
    )
    song_id = cursor.lastrowid

    # Insert song-dance relationships
    for dance in record['dances']:
        dance_id = dance_map[dance]
        cursor.execute(
            'INSERT INTO song_dances (song_id, dance_id) VALUES (?, ?)',
            (song_id, dance_id)
        )

# Commit changes
conn.commit()

# Display statistics
cursor.execute('SELECT COUNT(*) FROM songs')
song_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM dances')
dance_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM song_dances')
relationship_count = cursor.fetchone()[0]

print(f"\nDatabase populated successfully!")
print(f"  Songs: {song_count}")
print(f"  Dances: {dance_count}")
print(f"  Song-Dance relationships: {relationship_count}")

# Show sample queries
print("\n=== Sample query: Songs for Swing ===")
cursor.execute('''
    SELECT s.title, s.artist, s.bpm
    FROM songs s
    JOIN song_dances sd ON s.song_id = sd.song_id
    JOIN dances d ON sd.dance_id = d.dance_id
    WHERE d.name = 'Swing'
    ORDER BY s.bpm
    LIMIT 5
''')
for row in cursor.fetchall():
    print(f"  {row[0]} by {row[1]} ({row[2]} BPM)")

print("\n=== Sample query: All dances for 'In the Mood' ===")
cursor.execute('''
    SELECT d.name
    FROM songs s
    JOIN song_dances sd ON s.song_id = sd.song_id
    JOIN dances d ON sd.dance_id = d.dance_id
    WHERE s.title = 'In the Mood'
''')
for row in cursor.fetchall():
    print(f"  {row[0]}")

print("\n=== All dances available ===")
cursor.execute('SELECT name FROM dances ORDER BY name')
for row in cursor.fetchall():
    print(f"  {row[0]}")

conn.close()
print("\nDatabase saved to music_speed.db")
