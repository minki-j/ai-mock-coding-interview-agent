import json
import subprocess
import tempfile
import os
import uuid
from dotenv import load_dotenv
from typing import Optional
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
        except:
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

Think about all the possible cases given the constraints, which are not covered in the existing examples. Generate tricky test cases covering all corner cases inputs being empty, very large, very small etc. Output in the format shown above. Include a description of why each test case is tricky in the JSON. Remember to think outside the box to generate very hard test cases.
"""
            }
          ]
        }
        ],
      temperature=1,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response.choices[0].message.content.strip("`jsonJSON \n")

def convert_examples_to_test_code(test_examples, test_code):
    response = client.beta.chat.completions.parse(
      model="gpt-4o",
      messages=[
          {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You are an expert programmer. Your task is to generate test code for the test cases. All the code should be in python. the unit test should use a class as seen in examples, and be sure to include if __name__ == \"__main__\": so it can start the unit test if i run the python file."
            }
          ]
        },
          {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": f"""Here is the expected output format:
<test_code>
{test_code}
</test_code>

Generate working code in the above format for the test cases below:

<test_examples>
{test_examples}
</test_examples>
"""
            }
          ]
        }
        ],
      temperature=1,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response.choices[0].message.content.strip('`python \n')

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
              "text": "You are an expert software engineer in testing. You have been given a coding problem, a test code which has a bunch of test cases for that coding problem and some error messages from running the test cases. Modify the test cases to resolve those errors and output the resolved test code."
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


def main(tries: int = 3):

    # let's start with two-sum only
    with open("interview_data/two-sum.json", "r") as f:
        data = json.load(f)

    content_md = data["content_md"]
    test_cases_code = data["test_code"]
    question = content_md[:content_md.rfind("\n\n**Example")].strip()
    constraints = content_md[content_md.rfind("Constraints:**"):].strip()
    solution = data["approaches"][0]["implementation_code"]
    existing_examples = data["test_input_output"]
    generate_tries, fix_tries = 2, 3
    new_examples = []
    new_test_examples_codes = []
    if test_cases_code and solution:
        for _ in tqdm(range(generate_tries)):
            new_examples = generate_test_examples(question=question, constraints=constraints, existing_test_examples=existing_examples)
            new_test_examples_code = convert_examples_to_test_code(new_examples, test_cases_code)
            
            tries_count = 0
            previous_test_cases, previous_error = "", ""
            for _ in tqdm(range(fix_tries)):
                # Test new test cases
                print("Testing new test cases")
                test_code = solution + "\n\n" + new_test_examples_code

                test_code_execution = CodeExecution(code=test_code)
                formatted_code = format_code(test_code_execution)["formatted_code"]

                test_code_execution = CodeExecution(code=formatted_code)
                execution_result = execute_code(test_code_execution)

                print(execution_result)

                if execution_result.error:
                    tries_count += 1
                    previous_test_cases = new_test_examples_code
                    previous_error = execution_result.error
                    print(f"Error {previous_error}, trying again")
                else:
                    print("No errors, breaking")
                    break


                print(f"Fixing test cases - Tries: {tries_count + 1}")
                new_test_examples_code = fix_test_cases(solution, new_test_examples_code, previous_test_cases, previous_error)
            new_examples = eval(new_examples)
            new_test_examples_codes.append(new_test_examples_code)

        with open("interview_data/two-sum-test-cases.json", "w") as f:
            json.dump({"test_code": new_test_examples_codes}, f)


if __name__ == "__main__":
    main(tries=3)
