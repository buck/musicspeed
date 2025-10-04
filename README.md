# Music Speed Chart

A database and interactive web chart of dance music organized by tempo (BPM), with YouTube links for each song.

🎵 **Live site:** https://buck.github.io/musicspeed/

## Overview

This project scraped a music speed chart from ssqq.com and converted it into a searchable, sortable database with YouTube links for each song. The data includes 70 songs ranging from 60 to 240 BPM, with suggested dances for each tempo.

## Features

- **SQLite Database**: Normalized schema with songs, dances, and many-to-many relationships
- **YouTube Integration**: Each song has a link to the most-viewed YouTube video
- **Clean HTML Table**: Sortable by BPM with clickable YouTube links
- **22 Dance Types**: From Slow Dance to Fast Polka, Swing to Tango

## Data Source

Original data scraped from: https://ssqq.com/stories/speedcha.htm

The original HTML was hand-coded and not well-structured, requiring custom parsing to extract the data from separate table columns.

## Database Schema

### Tables

**songs**
- `song_id`: Primary key
- `title`: Song title (normalized capitalization)
- `artist`: Artist name (normalized capitalization)
- `bpm`: Beats per minute (may be a range like "075-150")
- `youtube_url`: Link to most-viewed YouTube video

**dances**
- `dance_id`: Primary key
- `name`: Dance name (e.g., "Texas Two Step", "Swing", "Waltz")

**song_dances**
- `song_id`: Foreign key to songs
- `dance_id`: Foreign key to dances
- Supports multi-valued dance suggestions per song

## Files

### Core Files
- `music_speed.db` - SQLite database with all song data
- `index.html` - GitHub Pages entry point
- `music_chart.html` - Generated HTML table

### Scripts
- `scrape_music.py` - Initial page fetcher
- `parse_music.py` - HTML parser to extract data from table columns
- `normalize_data.py` - Capitalizes titles/artists, expands dance abbreviations
- `create_database.py` - Creates SQLite schema and populates tables
- `generate_html.py` - Generates HTML table from database
- `add_youtube_links.py` - Fetches YouTube URLs for songs

### Data Files
- `music_data_normalized.json` - Cleaned and normalized song data

## Usage

### Regenerate HTML from Database

```bash
python3 generate_html.py
```

This queries the database and creates `music_chart.html` with all current data.

### Add/Update YouTube Links

```bash
python3 add_youtube_links.py
```

This finds songs without YouTube URLs and searches for the most-viewed version of each.

### Query the Database

```bash
sqlite3 music_speed.db

# Find all swing songs
SELECT s.title, s.artist, s.bpm
FROM songs s
JOIN song_dances sd ON s.song_id = sd.song_id
JOIN dances d ON sd.dance_id = d.dance_id
WHERE d.name = 'Swing'
ORDER BY CAST(SUBSTR(s.bpm, 1, INSTR(s.bpm || '-', '-') - 1) AS INTEGER);

# List all available dances
SELECT name FROM dances ORDER BY name;
```

## Development Notes

### Dance Abbreviations

The original chart used abbreviations that were expanded:
- `2STEP`, `TWOSTEP` → Texas Two Step
- `JITT`, `JITTBUG` → Jitterbug
- `WLTZ` → Waltz
- `SWNG` → Swing
- `FXTRT` → Foxtrot

### Data Corrections

- Artist "Bb King" → "B.B. King"
- Song "Hoodoo Voodoo Doll" BPM "120-240" → "240" (fast song, 120 was incorrect timing)

### YouTube Selection

For each song, the script searches for the top 3 YouTube results matching "{title} {artist}" and selects the video with the most views.

## Project Timeline

1. Scraped HTML from ssqq.com
2. Parsed non-standard table structure
3. Normalized song/artist names and dance abbreviations
4. Built SQLite database with proper schema
5. Generated initial HTML table
6. Added YouTube integration with yt-dlp
7. Published to GitHub Pages

## License

Data originally from ssqq.com. This project is for educational/reference purposes.
