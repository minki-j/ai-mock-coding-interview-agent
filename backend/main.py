import datetime
import os
import subprocess
import tempfile
import uuid
from typing import List, Optional

from agents.main_graph import main_graph
from db.schema import Interview, Message, User
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mongo import insert_document
from pydantic import BaseModel

app = FastAPI(title="Python Code Execution Service")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def add_user(user: User):
    print("/add_user", user)
    user_id = await insert_document("users", user)
    return {"id": str(user_id), **user.model_dump()}

@app.post("/init_interview")
async def init_interview(interview_info: Interview):
    output = main_graph.invoke(
        input={
            "interview_question": interview_info.interview_question,
            "interview_solution": interview_info.interview_solution,
        },
        config={
            "configurable": {"thread_id": interview_info.id},
            "recursion_limit": 100,
        },
    )

    # Insert interview document
    interview_id = await insert_document("interviews", interview_info)

    # Create and insert message document
    message = Message(
        message=output.message_from_interviewer,
        sent_time=datetime.datetime.now(),
        sender="AI",
        interview_id=str(interview_id)  # Convert ObjectId to string
    )
    message_id = await insert_document("messages", message)

    # Update the message with its MongoDB id before returning
    return {
        "id": str(message_id),
        **message.model_dump(exclude={'id'})
    }


@app.post("/chat", response_model=Message)
async def chat(user_msg: Message):
    config = {
        "configurable": {"thread_id": user_msg.interview_id},
        "recursion_limit": 100
    }
    
    main_graph.update_state(
        config,
        {"messages": [{"role": "user", "content": user_msg.message}]},
    )
    output = main_graph.invoke(None, config)

    # Insert user message
    await insert_document("messages", user_msg)
    
    # Create and insert AI reply
    reply = Message(
        interview_id=user_msg.interview_id,
        message=output.message_from_interviewer,
        sent_time=datetime.datetime.now(),
        sender="AI",
    )
    reply_id = await insert_document("messages", reply)
    
    return {
        "id": str(reply_id),
        **reply.model_dump(exclude={'id'})
    }


class InterviewUIState(BaseModel):
    messages: List[Message]
    code_editor_state: str
    test_result: str


@app.get("/interview/{id}")
async def get_interview(id: str):
    return InterviewUIState()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
