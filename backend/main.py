import os
import subprocess
import tempfile
import uuid
from typing import Optional, List, Dict, Annotated
import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import create_engine, SQLModel, Session

from agents.main_graph import main_graph
from db.schema import User, Interview, Message, CodeEditorState


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(title="Python Code Execution Service", lifespan=lifespan)


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
async def add_user(user: User, session: SessionDep):
    print("/add_user", user)
    session.add(user)
    session.commit()
    return user

@app.post("/init_interview")
async def init_interview(interview_info: Interview, session: SessionDep):
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

    session.add(
        Interview(
            id=interview_info.id,
            interview_question=interview_info.interview_question,
            interview_solution=interview_info.interview_solution,
            user_id=interview_info.user_id,
        )
    )
    session.commit()

    message = Message(
        message=output.message_from_interviewer,
        sentTime=datetime.datetime.now().isoformat(),
        sender="AI",
        interview_id=interview_info.id,
    )
    session.add(message)
    session.commit()

    return message


@app.post("/chat", response_model=Message)
async def chat(user_msg: Message, session: SessionDep):
    config = (
        {"configurable": {"thread_id": user_msg.interview_id}, "recursion_limit": 100},
    )
    main_graph.update_state(
        config,
        {"messages": [{"role": "user", "content": user_msg.message}]},
    )
    output = main_graph.invoke(None, config)
    session.add(user_msg)
    reply = Message(
        interview_id=user_msg.interview_id,
        message=output.message_from_interviewer,
        sentTime=datetime.datetime.now().isoformat(),
        sender="AI",
    )
    session.add(reply)
    session.commit()
    return reply


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
