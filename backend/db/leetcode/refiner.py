import os
import json
import time
import random
import requests
from problem_names import PROBLEM_NAMES
from markdownify import markdownify
from tqdm import tqdm
import logging

# Get the directory of the current file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_dir)

# Optionally, print the current working directory to confirm
print("Current working directory:", os.getcwd())

logging.basicConfig(level=logging.INFO)

def populate_codes_in_solution(solution: str, problem_name: str):
    keyword = ["https://leetcode.com/playground"]
    urls = []
    code_snippets = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://leetcode.com/",
        "Origin": "https://leetcode.com",
        "Connection": "keep-alive"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
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

    for url in urls:
        try:
            playground_id = url.split("/playground/")[1].split("/")[0]
            content, lang_slug = fetch_code_via_graphql(session, playground_id)
            
            if content:    
                code_snippets.append({
                    "url": url,
                    "code": content,
                    "langSlug": lang_slug
                })
                
                solution = solution.replace(
                    url, 
                    f"\n```{lang_slug}\n{content}\n```\n"
                )
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            logging.error(f"Failed to fetch code from {url}: {str(e)}")
    
    return solution, code_snippets

def fetch_code_via_graphql(session, playground_id):
    query = """
    query getPlaygroundCode($uuid: String!) {
        playground(uuid: $uuid) {
            playgroundcodeSet {
                code
                langSlug
            }
        }
    }
    """
    try:
        response = session.post(
            "https://leetcode.com/graphql",
            json={
                "query": query,
                "variables": {"uuid": playground_id}
            }
        )
        data = response.json()
        codes = data.get("data", {}).get("playground", {}).get("playgroundcodeSet", [])
        # Get first available solution, preferring Python
        python_solution = next(
            (code for code in codes if code.get("langSlug") == "python3"),
            next(iter(codes), None)  # Fallback to first solution of any language
        )
        if python_solution:
            return python_solution.get("code"), python_solution.get("langSlug")
        return None, None
    except Exception as e:
        logging.error(f"GraphQL error: {str(e)}")
        return None, None

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    successful_fetch_count = 0
    for problem_name in tqdm(PROBLEM_NAMES, desc="Processing problems"):
        with open(f"./scraped_data/{problem_name}.json", "r") as f:
            data = json.load(f)

        original_solution = data["solution"]["content"]
        if original_solution:
            modified_solution, code_snippets = populate_codes_in_solution(original_solution, problem_name)
            data["solution"]["content"] = modified_solution
            data["code_snippets"] = code_snippets
            
            if code_snippets:
                successful_fetch_count += 1
                logging.info(f"Successfully fetched {len(code_snippets)} code snippets for {problem_name}")
            else:
                logging.info(f"No code snippets found for {problem_name}")

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

    logging.info(f"Successfully fetched code snippets for {successful_fetch_count} problems.")

if __name__ == "__main__":
    main()
