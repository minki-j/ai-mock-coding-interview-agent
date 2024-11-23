import os
import json
import time
import random
import requests
from typing import Dict
from dotenv import load_dotenv
from problem_names import PROBLEM_NAMES
from markdownify import markdownify
import logging
import re
from enum import Enum
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


logging.basicConfig(level=logging.INFO)


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

    def get_schema_info(self):
        introspection_query = """
        query {
          __type(name: "QuestionNode") {
            name
            fields {
              name
              type {
                name
                kind
              }
              description
            }
          }
        }
        """

        try:
            response = self.session.post(
                self.base_url,
                json={"query": introspection_query},
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching schema: {str(e)}")
            return {}

    def populate_codes_in_approach(self, approach: str, approach_title: str):
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

        approaches = []
        implementation_code = ""
        start_idx = approach.find("https://leetcode.com/playground")
        while start_idx != -1:
            end_idx = approach.find('"', start_idx)
            if end_idx == -1:
                end_idx = approach.find(" ", start_idx)
            if end_idx == -1:
                end_idx = approach.find(">", start_idx)
            if end_idx == -1:
                break

            full_url = approach[start_idx:end_idx]
            approaches.append({"title": approach_title, "url": full_url})

            start_idx = approach.find("https://leetcode.com/playground", end_idx)

        for approach_data in approaches:
            try:
                playground_id = (
                    approach_data["url"].split("/playground/")[1].split("/")[0]
                )
                content, lang_slug = self.fetch_code_via_graphql(session, playground_id)

                if content:
                    implementation_code = content

                    iframe_pattern = f'<iframe[^>]*src="{re.escape(approach_data["url"])}"[^>]*></iframe>'
                    approach = re.sub(
                        iframe_pattern, f"\n```{lang_slug}\n{content}\n```\n", approach
                    )
                # time.sleep(random.uniform(2, 4))
            except Exception as e:
                logging.error(
                    f"Failed to fetch code from {approach_data['url']}: {str(e)}"
                )
        return approach, implementation_code

    def fetch_code_via_graphql(self, session, playground_id):
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
                json={"query": query, "variables": {"uuid": playground_id}},
            )
            data = response.json()
            codes = (
                data.get("data", {}).get("playground", {}).get("playgroundcodeSet", [])
            )
            # Get first available solution, preferring Python
            python_solution = next(
                (code for code in codes if code.get("langSlug") == "python3"),
                next(iter(codes), None),  # Fallback to first solution of any language
            )
            if python_solution:
                return python_solution.get("code"), python_solution.get("langSlug")
            return None, None
        except Exception as e:
            logging.error(f"GraphQL error: {str(e)}")
            return None, None

    def scrape_problem(self, problem_name: str) -> Dict:
        print(f">> Scraping problem: {problem_name}")
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
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                exampleTestcaseList
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
            if "data" in data and "question" in data["data"]:
                question = data["data"]["question"]
                if question["solution"].get("content") is None:
                    return None
                question["codeSnippets"] = [
                    snippet
                    for snippet in question["codeSnippets"]
                    if snippet["lang"] == "Python3"
                ]
                return question
            return None
        except requests.RequestException as e:
            print(f"Error fetching problem {problem_name}: {str(e)}")
            return {}


def generate_test_code(test_input_output_dict_list, function_name):
    test_code = """import unittest

class Test(unittest.TestCase):"""

    # Generate test methods for each test case
    for i, test_case in enumerate(test_input_output_dict_list, 1):
        inputs = test_case["input"]
        expected = test_case["output"]

        # Format the test method
        test_method = f"""
    def test_{i}(self):
        solution = Solution()
        self.___(solution.{function_name}({inputs}), {expected})"""  # Need to use LLM to guess the assert method. For ordering  and a sinlge ouput questions, we can use assertEqual, for multiple output questions that don't have ordering, we need to use assertCountEqual

        test_code += test_method

    # Add main block
    test_code += """

if __name__ == "__main__":
    unittest.main()
"""
    return test_code


def main():
    scraper = LeetCodeScraper()

    # schema = scraper.get_schema_info()
    # for field in schema["data"]["__type"]["fields"]:
    #     print(f"{field['name']}: {field['type']['name'] or field['type']['kind']}")

    for problem_name in PROBLEM_NAMES:

        # if os.path.exists(f"./data/{problem_name}.json"):
        #     print(f"-- Skipping {problem_name} - already exists")
        #     continue

        result = scraper.scrape_problem(problem_name)
        if not result:
            continue

        # Contents
        result["content_md"] = (
            markdownify(result["content"]).replace("\n\n\u00a0\n\n", "").strip()
        )

        # Extract test examples from contents
        test_examples = result["content_md"].split("**Example ")[1:]
        test_examples[-1] = test_examples[-1].split("**Constraints:")[0]
        test_input_output_dict_list = []
        for test_example in test_examples:
            test_input_output_dict = {}
            try:
                code_blocks = test_example.split("```")
                if len(code_blocks) >= 2:
                    code_block = code_blocks[1].strip()
                    lines = code_block.split("\n")
                    input_line = next(
                        (line for line in lines if line.startswith("Input:")), ""
                    )
                    output_line = next(
                        (line for line in lines if line.startswith("Output:")), ""
                    )
                    test_input_output_dict["input"] = input_line.replace(
                        "Input:", ""
                    ).strip()
                    test_input_output_dict["output"] = output_line.replace(
                        "Output:", ""
                    ).strip()
                    test_input_output_dict_list.append(test_input_output_dict)
            except Exception as e:
                print(f"Error parsing test example: {e}")
                continue
        result["test_input_output"] = test_input_output_dict_list

        # Test code
        function_name = (
            result["codeSnippets"][0]["code"].split("def ")[1].split("(")[0].strip()
        )
        test_code = generate_test_code(result["test_input_output"], function_name)

        load_dotenv('.env', override=True)
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        chat_model = ChatOpenAI(
            model="gpt-4o-2024-08-06",
            api_key=OPENAI_API_KEY,
            temperature=0.7,
        )

        class FunctionName(Enum):
            assertEqual = "assertEqual"
            assertCountEqual = "assertCountEqual"
        class Response(BaseModel):
            function_name: FunctionName = Field(
                description="The function name to use for the assert method."
            )
        response = (
            ChatPromptTemplate.from_template(
                """
            You are given an coding interview question and a test code for a function. You need to determine which assert method to use for the test in the place of ___.
            ---
            Interview question: {content_md}
            ---
            Test code:
            {test_code}
            ---
            """
            )
            | chat_model.with_structured_output(Response)
        ).invoke(
            {
                "test_code": test_code,
                "content_md": result["content_md"],
            }
        )
        result["test_code"] = test_code.replace("___", response.function_name.value)

        # Solutions
        solution_sections = result["solution"]["content"].split("### Approach ")

        solution_intro = solution_sections[0]
        result["solution_intro"] = solution_intro

        approaches = solution_sections[1:]
        result["approaches"] = []
        for i, approach in enumerate(approaches):
            approach_title = approach.split("\n")[0].replace(f"{i+1}: ", "").strip()
            populated_approach, implementation_code = (
                scraper.populate_codes_in_approach(approach, approach_title)
            )
            result["approaches"].append(
                {
                    "title": approach_title,
                    "approach": "\n".join(populated_approach.split("\n")[1:])
                    .replace("---", "")
                    .strip(),
                    "implementation_code": implementation_code,
                }
            )

        with open(
            f"./data/{problem_name}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
