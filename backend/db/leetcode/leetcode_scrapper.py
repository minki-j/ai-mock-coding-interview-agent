import os
import json
import time
import random
import requests
from typing import Dict
from dotenv import load_dotenv
from problem_names import PROBLEM_NAMES


class LeetCodeScraper:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://leetcode.com/graphql"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_problem(self, problem_name: str) -> Dict:
        query = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                content
                difficulty
                title
                topicTags {
                    name
                }
                solution {
                    content
                }
            }
        }
        """

        try:
            response = self.session.post(
                self.base_url,
                json={"query": query, "variables": {"titleSlug": problem_name}},
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"GraphQL errors: {data['errors']}")
                return {}

            return data["data"]["question"]

        except requests.RequestException as e:
            print(f"Error fetching problem {problem_name}: {str(e)}")
            return {}


def main():
    scraper = LeetCodeScraper()

    for problem_name in PROBLEM_NAMES:
        if os.path.exists(f"./data/{problem_name}.json"):
            print(f"-- Skipping {problem_name} - already exists")
            continue

        print(f">> Scraping problem: {problem_name}")
        result = scraper.scrape_problem(problem_name)

        with open(
            f"./data/{problem_name}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
