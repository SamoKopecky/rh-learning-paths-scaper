import json
import sys
from typing import List

import requests
from bs4 import BeautifulSoup as Bs


class LearningPath:
    def __init__(self, url):
        self.paths: int = 0
        self.hours: int = 0
        self.description: str = ""
        self.label: str = ""
        self.url: str = url


def read_csv(file_path: str) -> List[str]:
    urls_list = []
    with open(file_path) as urls:
        for row in urls:
            urls_list.append(row.strip())
    return urls_list


def main(file_path):
    urls = read_csv(file_path)
    print(f"Found {len(urls)} urls")
    lps_json = []
    for url in urls:
        lps_json.append(scrape_learning_path(url).__dict__)
    with open("data.json", "w") as file:
        file.write(json.dumps(lps_json))


def scrape_learning_path(url: str) -> LearningPath:
    lp = LearningPath(url)
    req = requests.get(lp.url)
    soup = Bs(req.content, "html.parser")
    get_time_and_resources(lp, soup)
    lp_body: Bs = soup.find_all("div", class_="lp-hero__body")[0]
    lp.description = lp_body.text.strip()
    lp_title: Bs = soup.find_all("h2", class_="lp-hero__title-text")[0]
    lp.label = lp_title.text.strip()
    return lp


def get_time_and_resources(lp, soup):
    print(f"Scraping {lp.url}")
    lp_metadata: Bs = soup.find_all("div", class_="lp-hero__meta-data")[0]
    for span in lp_metadata.select("span"):
        span_split = span.text.split(" ")
        span_first = span_split[0]
        if span_first.isnumeric():
            last_split = span_split[-1].lower()
            numeric = int(span_first)
            if last_split in ["resource", "resources"]:
                lp.paths = numeric
            elif last_split in ["hour", "hours", "hrs", "hr"]:
                lp.hours = numeric
            elif last_split in ["mins", "min", "minutes"]:
                minutes = int(span_split[-2])
                if len(span_split) <= 2:
                    lp.hours = 1
                elif minutes >= 30:
                    lp.hours = numeric + 1
                else:
                    lp.hours = numeric


if __name__ == "__main__":
    main(sys.argv[1])
