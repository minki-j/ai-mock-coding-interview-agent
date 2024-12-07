import json
import subprocess
import tempfile
import os
import uuid
from dotenv import load_dotenv
from typing import Optional, List
from openai import OpenAI
from pydantic import BaseModel, Field
from tqdm import tqdm

load_dotenv()

class TestCase(BaseModel):
    unit_test: str = Field(description="The unit test case associated with the solution.")

class CodeExecution(BaseModel):
    code: str
    timeout: Optional[int] = 5000  # Default timeout in milliseconds

class ExecutionResult(BaseModel):
    output: str
    error: Optional[str] = None
    execution_time: float

class TestExample(BaseModel):
    name: str
    input: str
    output: str
    description: str = Field(description="A description of why this test case is chosen and why it is important to have it in the test suite.")

class TestExamples(BaseModel):
    test_examples: List[TestExample]

def normalize_indentation(code: str) -> str:
    """
    Normalize the indentation of code by:
    1. Converting tabs to spaces
    2. Detecting the minimum indentation level
    3. Removing any common leading indentation
    4. Ensuring consistent newlines
    5. Removing leading/trailing blank lines
    """
    # Convert tabs to spaces
    code = code.replace("\t", "    ")

    # Split into lines
    lines = code.replace("\r\n", "\n").split("\n")

    # Remove leading and trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return ""

    # Find minimum indentation level (excluding empty lines)
    non_empty_lines = [line for line in lines if line.strip()]
    if not non_empty_lines:
        return ""

    min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)

    # Remove common leading indentation and join lines
    normalized_lines = []
    for line in lines:
        if line.strip():  # Non-empty line
            normalized_lines.append(line[min_indent:])
        else:  # Empty line
            normalized_lines.append("")

    return "\n".join(normalized_lines)


def format_code(code_execution: CodeExecution):
    """Preview how the code will be formatted without executing it"""
    normalized_code = normalize_indentation(code_execution.code)
    return {"original_code": code_execution.code, "formatted_code": normalized_code}

def execute_code(code_execution: CodeExecution):
    # Normalize the code indentation
    normalized_code = normalize_indentation(code_execution.code)

    # Create a unique temporary file
    file_id = str(uuid.uuid4())
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, f"{file_id}.py")

    try:
        # Write code to temporary file
        with open(file_path, "w") as f:
            f.write(normalized_code)

        # Execute the code with timeout
        process = subprocess.Popen(
            ["python", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            stdout, stderr = process.communicate(timeout=code_execution.timeout)
            return ExecutionResult(
                output=stdout,
                error=stderr if stderr else None,
                execution_time=code_execution.timeout,
            )
        except subprocess.TimeoutExpired:
            process.kill()
            raise Exception("Code execution timed out")

    except Exception as e:
        raise Exception(f"Error executing code: {str(e)}")

    finally:
        # Cleanup temporary files
        try:
            os.remove(file_path)
            os.rmdir(temp_dir)
        except Exception as _:
            pass

client = OpenAI()

def generate_test_examples(question, constraints, existing_test_examples):
    response = client.beta.chat.completions.parse(
      model="gpt-4o",
      messages=[
          {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You are an expert software tester. Your task is to generate diverse test cases for a given question with some contraints. Be creative and think outside the box to generate tricky test cases."
            }
          ]
        },
          {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": f"""<question>
{question}
</question>

<constraints>
{constraints}
</constraints>

<example_tests>
{existing_test_examples}
</example_tests>

Think about all the possible cases given the constraints, which are not covered in the existing examples. Generate tricky test cases covering all corner cases inputs being empty, very large, very small etc. Output in the format shown above. Include a 'description' of why each test case is tricky and a camel cased 'name' for the test in the JSON. Remember to think outside the box to generate very hard test cases.
"""
            }
          ]
        }
        ],
      temperature=1,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      response_format=TestExamples
    )

    return response.choices[0].message.parsed

def convert_examples_to_test_code(test_examples, test_code):
    """Receive a list of test examples, generate test code for each one"""

    # implementation_code is used as the solution

    output_code_list = []

    for index, test_example in enumerate(test_examples):
        input = test_example["input"]
        output = test_example["output"]
        name = test_example["name"]

        test_code_template = f"""
import unittest\n\nclass Test(unittest.TestCase):\n    def test_{name}_{index}(self):\n        solution = Solution()\n        self.assertCountEqual(solution.twoSum({input}), {output})\n\nif __name__ == \"__main__\":\n    unittest.main()\n
    """
        test_code += "\n\n" + test_code_template

        output_code_list.append((test_code, test_example))

    return output_code_list

def fix_test_cases(solution: str, test_cases: str, previous_test_cases: str = "", previous_error: str = ""):

    if previous_test_cases:
        previous_test_cases = "\nTest cases: \n" + previous_test_cases

    if previous_error:
        previous_error = "\nErrors: \n" + previous_error


    response = client.beta.chat.completions.parse(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You are an expert software engineer in testing. You have been given a coding problem, a test code which has a test case for that coding problem and some error message from running the test case. Modify the test case to resolve those errors and output the resolved test code."
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Current solution: \n" + solution + "\n\n" + previous_test_cases + previous_error
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

    return response.choices[0].message.parsed.unit_test

def main(generate_tries: int = 2, fix_tries: int = 1):

    # let's start with two-sum only
    with open("interview_data/two-sum.json", "r") as f:
        data = json.load(f)

    content_md = data["content_md"]
    test_cases_code = data["test_code"]
    question = content_md[:content_md.rfind("\n\n**Example")].strip()
    constraints = content_md[content_md.rfind("Constraints:**"):].strip()
    solution = data["approaches"][0]["implementation_code"]
    existing_examples = data["test_input_output"]
    new_examples = []

    if test_cases_code and solution:
        for _ in tqdm(range(generate_tries)):
            new_examples = generate_test_examples(question=question, constraints=constraints, existing_test_examples=existing_examples)

            print("*** New test cases ***")

            new_examples_json = json.loads(new_examples.model_dump_json())["test_examples"]
            print(new_examples_json)

            new_tests_list = convert_examples_to_test_code(new_examples_json, solution)

            failing_tests = []
            passing_tests = []
            for test_code, test_example in new_tests_list:
                test_code_execution = CodeExecution(code=test_code)
                formatted_code = format_code(test_code_execution)["formatted_code"]

                test_code_execution = CodeExecution(code=formatted_code)
                execution_result = execute_code(test_code_execution)

                if execution_result.error:
                    failing_tests.append({"name": test_example["name"], "code": test_code, "error": execution_result.error})
                else:
                    passing_tests.append({"name": test_example["name"], "code": test_code})


            for test in failing_tests:
                tries_count = 0
                previous_test_cases, previous_error = test["code"], test["error"]
                for _ in tqdm(range(fix_tries)):
                    print(f"Fixing test cases - Tries: {tries_count + 1}")
                    print(f"bug_test_code: {previous_test_cases}")
                    print(f"bug_message: {previous_error}")
                    new_code_for_test = fix_test_cases(solution, '', previous_test_cases, previous_error)
                    print(f"new_test_code: {new_code_for_test}")

                    test_code = solution + "\n\n" + new_code_for_test

                    test_code_execution = CodeExecution(code=test_code)
                    formatted_code = format_code(test_code_execution)["formatted_code"]

                    test_code_execution = CodeExecution(code=formatted_code)
                    execution_result = execute_code(test_code_execution)

                    print(execution_result)

                    if execution_result.error:
                        tries_count += 1
                        previous_test_cases = new_code_for_test
                        previous_error = execution_result.error
                        print(f"Error {previous_error}, trying again")
                    else:
                        passing_tests.append({"name": test["name"], "code": new_code_for_test})
                        print("No errors, breaking")
                        break

            passed_examples = []
            for test in new_examples:
                if test in passing_tests:
                    passed_examples.append(test)

            data["test_examples_debugging"] = passed_examples
            data["test_code_debugging"] = passing_tests

        with open("interview_data/two-sum.json", "w") as f:
            json.dump(data, f)


if __name__ == "__main__":
    main()
