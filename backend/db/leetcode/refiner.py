import os
import json
import time
import random
import requests
from typing import Dict
from dotenv import load_dotenv
from problem_names import PROBLEM_NAMES
from markdownify import markdownify
from tqdm import tqdm
import logging


from problem_names import PROBLEM_NAMES

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-3-5-sonnet-latest")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Get the directory of the current file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_dir)

# Optionally, print the current working directory to confirm
print("Current working directory:", os.getcwd())

logging.basicConfig(level=logging.INFO)

def populate_codes_in_solution(solution: str, problem_name: str):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://leetcode.com/",
            "Origin": "https://leetcode.com",
            "Connection": "keep-alive",
        }
    )

    urls = []
    implementation_codes = []
    start_idx = solution.find("https://leetcode.com/playground")
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

        start_idx = solution.find("https://leetcode.com/playground", end_idx)

    for url in urls:
        try:
            playground_id = url.split("/playground/")[1].split("/")[0]
            content, lang_slug = fetch_code_via_graphql(session, playground_id)

            if content:    
                implementation_codes.append({
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
    return solution, implementation_codes

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


def extract_approach_from_solution(solution: str) -> str:
    chat_model = ChatOpenAI(
        model=DEFAULT_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=LLM_TEMPERATURE,
    )

    response = (
        ChatPromptTemplate.from_template("""You are given a detailed solution document to a coding problem. The document contains one or many approaches  to solve the problem. Each approach will potentially have a title, description, algorithm, python code, time complexity analysis and some followup questions. Your task is to convert this blob of document into structured JSON output.
    
<document>
{solution}
</document
    
Output a JSON array where each object represents an approach. Each approach object should have ONLY the following keys
title: Name of the approach. Do not include text like "Approach 1" in the title.
approach: Methodology to solve the problem.
analysis: Time and space complexity of the approach including their explanations.
""") | chat_model
    ).invoke(
        {
            "solution": solution,
        }
    )

    return json.loads(response.content.strip("`JjSsOoNn\n "), strict=False)

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
            data["approaches"] = extract_approach_from_solution(original_solution)

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
