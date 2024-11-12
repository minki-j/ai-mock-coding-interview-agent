import os
import json
import time
import random
import requests
from typing import Dict
from dotenv import load_dotenv
from problem_names import PROBLEM_NAMES
from markdownify import markdownify

def populate_codes_in_solution(solution: str):
    keyword = ["https://leetcode.com/playground"]
    urls = []
    for k in keyword:
        start_idx = solution.find(k)
        while start_idx != -1:
            end_idx = solution.find('"', start_idx)
            if end_idx == -1:
                end_idx = solution.find(' ', start_idx)
            if end_idx == -1:
                end_idx = solution.find('>', start_idx)
            if end_idx == -1:
                break
                
            full_url = solution[start_idx:end_idx]
            urls.append(full_url)

            start_idx = solution.find(k, end_idx)

    # Add code fetching logic
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                code_data = response.json()
                if code_data.get('code'):
                    # Replace the URL with the actual code in a markdown code block
                    solution = solution.replace(
                        url, 
                        f"\n```\n{code_data['code']}\n```\n"
                    )
            # Add delay to avoid rate limiting
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Failed to fetch code from {url}: {str(e)}")
    
    return solution

def main():
    for problem_name in PROBLEM_NAMES:
        with open(
            f"./scraped_data/{problem_name}.json",
            "r",
        ) as f:
            data = json.load(f)

        original_solution = data["solution"]["content"]
        if original_solution:
            data["solution"]["content"] = populate_codes_in_solution(original_solution)

        data["content_md"] = markdownify(data["content"])
        if data.get("solution") and data["solution"].get("content"):
            data["solution_md"] = markdownify(data["solution"]["content"])
        else:
            data["solution_md"] = None

        with open(
            f"./refined_data/{problem_name}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
