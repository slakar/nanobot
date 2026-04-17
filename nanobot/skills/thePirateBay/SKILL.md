---
name: thePirateBay
description: Search for torrents on The Pirate Bay and return the best results based on seeders and specific criteria.
---

# thePirateBay Skill

This skill provides a structured way to search for torrents on The Pirate Bay and return the best results based on seeders and specific criteria.

## Capabilities
- Search The Pirate Bay for a specific query.
- Filter results by quality (e.g., 1080p) and codec (e.g., x264).
- Sort and return the top N results by seeder count.
- Only identify torrents from verified and top sources.

## Implementation Details
The skill uses the following URL template for searching:
`https://thepiratebay.org/search.php?q={query}&all=on&search=Pirate+Search&page=0&orderby=`

## Usage Pattern
1. Construct the search query by combining the movie/content name with quality and codec requirements.
2. Fetch the results page using `web_fetch`.
3. Parse the results to identify the name and seeder count of each torrent.
4. Sort the parsed results by seeders in descending order.
5. Return the top options to the user.
6. Deliver the result: Send the URL and Magnet URL in two separate messages to the user.
