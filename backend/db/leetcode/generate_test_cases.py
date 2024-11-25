import json
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from problem_names import PROBLEM_NAMES

load_dotenv()

class TestCase(BaseModel):
    solution: str = Field(description="The solution to the leetcode problem.")
    unit_test: str = Field(description="The unit test case associated with the solution.")

client = OpenAI()

def generate_test_cases(problem_name: str):

    response = client.beta.chat.completions.parse(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "Please generate the following leetcode algorithm with solution and test cases, please include as much as test cases as possible. all the code should be in python. The case should use the standard class Solution, and the unit test should use a class as well, and be sure to include if __name__ == \"__main__\": so it can start the unit test if i run the python file"
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": problem_name
            }
          ]
        }
      ],
      response_format=TestCase,
      temperature=1,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response.choices[0].message.parsed


LEETCODE_TEST_CASES = {}

for problem_name in tqdm(PROBLEM_NAMES, desc="Generating test cases"):
    json_data = generate_test_cases(problem_name)
    LEETCODE_TEST_CASES[problem_name] = json_data.model_dump()

with open("leetcode_test_cases.json", "w", encoding="utf-8") as f:
    json.dump(LEETCODE_TEST_CASES, f)
