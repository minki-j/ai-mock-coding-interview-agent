import os
import subprocess
import tempfile
import uuid
from typing import Dict, List, Optional
from pathlib import Path

from agents.llm_models import chat_model
from agents.main_graph import main_graph
from bson import ObjectId
from db.mongo import delete_many, find_many, find_one, insert_document
from db.schema import LeetcodeQuestion
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

app = FastAPI(title="Python Code Execution Service")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DebugCodeResult(BaseModel):
    solution: str = Field(description="Fixed code")
    explanation: str = Field(description="Explanation for the fixed code")


class CodeExecution(BaseModel):
    code: str
    timeout: Optional[int] = 5000  # Default timeout in milliseconds


class ExecutionResult(BaseModel):
    output: str
    error: Optional[str] = None
    execution_time: float


@app.post("/format")
async def format_code(code_execution: CodeExecution):
    """Preview how the code will be formatted without executing it"""
    normalized_code = normalize_indentation(code_execution.code)
    return {"original_code": code_execution.code, "formatted_code": normalized_code}


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


@app.post("/execute", response_model=ExecutionResult)
async def execute_code(code_execution: CodeExecution):
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
            raise HTTPException(status_code=408, detail="Code execution timed out")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing code: {str(e)}")

    finally:
        # Cleanup temporary files
        try:
            os.remove(file_path)
            os.rmdir(temp_dir)
        except:
            pass


@app.post("/add_user")
async def add_user(user: dict):
    # Check if oauth_id is provided
    if "oauth_id" not in user:
        raise HTTPException(status_code=400, detail="oauth_id is required")

    # Check if user exists using oauth_id
    existing_user = await find_one("users", {"oauth_id": user["oauth_id"]})
    if existing_user:
        print("the user already exists")
        return existing_user

    # If user doesn't exist, insert new user
    print("inserting new user")
    user_id = await insert_document("users", user)
    return {"id": str(user_id), **user}


@app.post("/init_interview")
async def init_interview(interview_info: dict):
    print(f"==>> init_interview with user_id: {interview_info['user_id']}")
    user_id = ObjectId(interview_info["user_id"])
    interview_id = await insert_document(
        "interviews",
        {
            "user_id": user_id,
        },
    )

    main_graph.invoke(
        input={
            "start_date": interview_info["start_date"],
            "interviewee_name": interview_info["interviewee_name"],
            "difficulty_level": interview_info["difficulty"].lower(),
            "interview_title": interview_info["title"],
            "interview_question": interview_info["content"],
            "interview_question_md": interview_info["content_md"],
            "interview_approaches": interview_info["approaches"],
            "test_code": interview_info["test_code"],
            "test_input_output": interview_info["test_input_output"],
            "code_snippet": interview_info["codeSnippets"],
        },
        config={
            "configurable": {"thread_id": interview_id, "get_code_feedback": True},
            "recursion_limit": 100,
        },
    )

    return {"interview_id": str(interview_id)}


@app.post("/chat")
async def chat(data: dict):
    config = {
        "configurable": {"thread_id": data["interview_id"], "get_code_feedback": True},
        "recursion_limit": 100,
    }
    main_graph.update_state(
        config,
        {
            "messages": [HumanMessage(content=data["message"])],
            "code_editor_state": data["code_editor_state"],
            "test_result": data["test_result"],
        },
    )
    output = main_graph.invoke(None, config)

    return {
        "message_from_interviewer": output["message_from_interviewer"],
        "stage": output["stage"],
        "main_stage_step": output["main_stage_step"],
    }


@app.post("/update_code_editor_state")
async def update_code_editor_state(data: dict):
    main_graph.update_state(
        {"configurable": {"thread_id": data["interview_id"]}},
        {
            "code_editor_state": data["code_editor_state"],
            "test_result": data["test_result"],
        },
    )


@app.get("/get_interview/{id}")
async def get_interview(id: str):
    state = main_graph.get_state(config={"configurable": {"thread_id": id}}).values

    messages = [
        {
            "message": msg.content,
            "sentTime": "",
            "sender": "AI" if isinstance(msg, AIMessage) else "User",
        }
        for msg in state["messages"][1:]
    ]

    return {
        "interview_question": state["interview_question"],
        "messages": messages,
        "code_editor_state": state["code_editor_state"],
        "test_result": state["test_result"],
        "code_snippet": state["code_snippet"],
        "test_code": state["test_code"],
        "test_input_output": state["test_input_output"],
        "stage": state["stage"],
        "main_stage_step": state["main_stage_step"],
    }


@app.get("/get_interview_questions")
async def get_interview_questions():
    import json

    data_path = Path("db/leetcode/interview_data")
    questions = []

    for file_path in data_path.glob("*.json"):
        with open(file_path, "r") as f:
            data = json.load(f)
            questions.append(data)

    # with open("db/leetcode.json", "r", encoding="utf-8") as f:
    #     questions = json.load(f)

    # questions = [LeetcodeQuestion(**question) for question in questions if question["id"] in questions_set]

    return questions


@app.get("/get_interview_question/{id}")
async def get_interview_question(id: str):
    print(f"==>> get_interview_question with id: {id}")
    questions = await get_interview_questions()
    question = next((question for question in questions if question.id == id), None)

    if not question:
        raise HTTPException(status_code=404, detail=f"Question with id {id} not found")

    question_dict = question.model_dump()

    # print(f"==>> question: {question_dict}")

    try:
        with open(f"db/prep/{id}.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"==>> prep file for {id} not found")
        lines = []
    question_dict["prep_code"] = lines

    return question_dict


async def debug_code_with_llm(leetcode_number, solution, prep_code, error_message):
    leetcode_question = await get_interview_question(leetcode_number)

    chain = (
        ChatPromptTemplate.from_template(
            """
You are a Python debugging assistant specializing in LeetCode problems. Your task is to analyze a given LeetCode question, the current solution attempt, a failing test case, and the associated error. Then, you will provide a corrected solution along with a detailed explanation of the changes made.

Here's the LeetCode question:
{leetcode_question}


The current solution attempt is:
{current_solution}

The failing test case is:
{prep_code}

The error message received is:
{error_message}
Please follow these steps to debug and improve the solution:

1. Carefully read the question, current solution, test case, and error message.
2. Identify the root cause of the error by analyzing the code and the test case.
3. Consider edge cases and potential logical errors in the current solution.
4. Develop a corrected solution that addresses the identified issues.
5. Test your solution mentally with the given test case and other potential edge cases.
6. Prepare a clear explanation of the changes made and why they resolve the issue.

Provide your response in the following format:

<debug_analysis>
[Your analysis of the error and its root cause]
</debug_analysis>

<corrected_solution>
[The complete corrected Python code]
</corrected_solution>

<explanation>
[A detailed explanation of the changes made, why they were necessary, and how they resolve the issue]
</explanation>

Ensure that your corrected solution is complete, properly indented, and free of syntax errors. Your explanation should be clear and informative, helping the user understand the problem and its solution.
"""
        )
        | chat_model.with_structured_output(DebugCodeResult)
    )

    return chain.invoke(
        {
            "leetcode_question": leetcode_question,
            "current_solution": solution,
            "prep_code": prep_code,
            "error_message": error_message,
        }
    )


@app.post("/debug_code")
async def debug_code(data: dict):
    leetcode_number = data["leetcode_number"]
    solution = data["user_solution"]

    try:
        with open(f"db/prep/{leetcode_number}_test.py", "r", encoding="utf-8") as f:
            prep_code = f.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Test file for {leetcode_number} not found"
        )

    tries, max_tries = 0, 3
    working_code = False

    while not working_code and tries < max_tries:
        tries += 1

        # add user solution and prep code together
        full_code = solution + "\n\n" + prep_code

        output = await execute_code(CodeExecution(code=full_code, timeout=5000))

        if output.error:
            working_code = False
        else:
            working_code = True

        # ask LLM to debug the code and return the fixed code
        if not working_code:
            debug_result = await debug_code_with_llm(
                leetcode_number, solution, prep_code, output.error
            )

            solution = debug_result.solution

    if not working_code:
        raise HTTPException(
            status_code=400,
            detail="Code is not working",
            debug_result=debug_result,
            debug_explanation=debug_result.explanation,
            debug_solution=debug_result.solution,
        )

    return {
        "status": "success",
        "solution": solution,
        "explanation": debug_result.explanation,
    }


@app.get("/get_history/{user_id}")
async def get_history(user_id: str):
    interview_ids = await find_many("interviews", {"user_id": ObjectId(user_id)})
    interview_ids = [str(interview_id["_id"]) for interview_id in interview_ids]
    interviews = []
    for interview_id in interview_ids:
        state = main_graph.get_state(
            config={"configurable": {"thread_id": interview_id}}
        ).values

        interview = {}
        interview["id"] = interview_id
        interview["title"] = state.get("interview_title", "No Title")
        interview["start_date"] = state.get("start_date", "No Start Date")

        interviews.append(interview)
    return interviews


@app.delete("/delete_all_history/{user_id}")
async def delete_all_history(user_id: str):
    await delete_many("interviews", {"user_id": ObjectId(user_id)})
    return {"status": "success"}


@app.post("/change_step")
async def change_step(data: dict):
    step = data["step"]
    if step in ["coding", "debugging", "algorithmic_analysis"]:
        stage = "main"
        main_graph.update_state(
            {"configurable": {"thread_id": data["interview_id"]}},
            {"stage": "main", "main_stage_step": step},
        )
    else:
        stage = step
        main_graph.update_state(
            {"configurable": {"thread_id": data["interview_id"]}},
            {"stage": stage, "main_stage_step": "coding"},  # only change stage and set main_stage_step default 
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
