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

def generate_test_cases(solution: str, test_cases: str, previous_test_cases: str = "", previous_error: str = ""):

    if previous_test_cases:
        previous_test_cases = "\n\nPrevious test cases: \n" + previous_test_cases

    if previous_error:
        previous_error = "\n\nPrevious error: \n" + previous_error

    response = client.beta.chat.completions.parse(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "Please generate the following leetcode algorithm additional test cases, based on provided solutions and existing test cases. Please include as much as test cases as possible, and be sure to cover all edge cases. All the code should be in python. the unit test should use a class as seen in examples, and be sure to include if __name__ == \"__main__\": so it can start the unit test if i run the python file. If there are any errors in the previous test cases, please fix them instead of generating new ones."
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Current solution: \n" + solution + "\n\nExisting test cases: \n" + test_cases + "\n\n" + previous_test_cases + previous_error
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


def main(tries: int = 3):

    # let's start with two-sum only
    with open("interview_data/two-sum.json", "r") as f:
        data = json.load(f)

    test_cases = data["test_code"]
    solution = data["approaches"][0]["implementation_code"]

    if test_cases and solution:
        tries_count = 0
        previous_test_cases, previous_error = "", ""
        for _ in tqdm(range(tries)):
            print(f"Generating test cases - Tries: {tries_count + 1}")
            new_test_cases = generate_test_cases(solution, test_cases, previous_test_cases, previous_error).model_dump()

            # Test new test cases
            print("Testing new test cases")
            test_code = solution + "\n\n" + new_test_cases["unit_test"]

            test_code_execution = CodeExecution(code=test_code)
            formatted_code = format_code(test_code_execution)["formatted_code"]

            test_code_execution = CodeExecution(code=formatted_code)
            execution_result = execute_code(test_code_execution)

            print(execution_result)

            if execution_result.error:
                tries_count += 1
                previous_test_cases = new_test_cases["unit_test"]
                previous_error = execution_result.error
                print(f"Error {previous_error}, trying again")
            else:
                print("No errors, breaking")
                break

        with open("interview_data/two-sum-test-cases.json", "w") as f:
            json.dump({"test_code": new_test_cases}, f)


if __name__ == "__main__":
    main(tries=3)
