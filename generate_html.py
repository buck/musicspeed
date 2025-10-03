#!/usr/bin/env python3
"""
Generate HTML page from music database
"""

import sqlite3

# Connect to database
conn = sqlite3.connect('music_speed.db')
cursor = conn.cursor()

# Query all songs with their dances
cursor.execute('''
    SELECT
        s.song_id,
        s.title,
        s.artist,
        s.bpm,
        GROUP_CONCAT(d.name, ', ') as dances
    FROM songs s
    LEFT JOIN song_dances sd ON s.song_id = sd.song_id
    LEFT JOIN dances d ON sd.dance_id = d.dance_id
    GROUP BY s.song_id
    ORDER BY CAST(SUBSTR(s.bpm, 1, INSTR(s.bpm || '-', '-') - 1) AS INTEGER)
''')

songs = cursor.fetchall()
conn.close()

# Generate HTML
html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music Speed Chart</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        table {
            width: 100%;
            max-width: 1200px;
            margin: 20px auto;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .bpm {
            text-align: center;
            font-weight: bold;
            color: #666;
        }
        .dances {
            color: #0066cc;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Music Speed Chart</h1>
    <table>
        <thead>
            <tr>
                <th>BPM</th>
                <th>Song Title</th>
                <th>Artist</th>
                <th>Suggested Dances</th>
            </tr>
        </thead>
        <tbody>
'''

# Add rows
for song_id, title, artist, bpm, dances in songs:
    html += f'''            <tr>
                <td class="bpm">{bpm}</td>
                <td>{title}</td>
                <td>{artist}</td>
                <td class="dances">{dances or ''}</td>
            </tr>
'''

html += '''        </tbody>
    </table>
    <div class="footer">
        <p>Music Speed Chart - Generated from Database</p>
        <p>Total Songs: ''' + str(len(songs)) + '''</p>
    </div>
</body>
</html>
'''

# Write to file
with open('music_chart.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated music_chart.html with {len(songs)} songs")
print("Open music_chart.html in your browser to view the chart")
