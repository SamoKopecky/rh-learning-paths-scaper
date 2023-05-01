# Scraper for the RH learning paths
This script will scrape the time, resources, description and title information from a learning path page and export it into a json for every url given in the input file.

## Usage

To parse a list of urls, pass as a parameter the path to the file.

```commandline
python3 main.py lps.txt
```

The resulting data will be saved to a `data.json` file in the current directory.