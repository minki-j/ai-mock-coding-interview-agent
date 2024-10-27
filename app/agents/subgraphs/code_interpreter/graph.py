import docker
import tempfile
import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from app.agents.state_schema import OverallState

def execute_code(state: OverallState):
    print("\n>>> NODE: execute_code")

    client = docker.from_env()

    # Create a temporary file with the user's code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(state.code_editor_state)
        temp_file_path = temp_file.name

    try:
        # Run the code in a Docker container
        container = client.containers.run(
            "python:3.9-slim",  # Use an official Python image
            f"python {os.path.basename(temp_file_path)}",
            volumes={os.path.dirname(temp_file_path): {'bind': '/code', 'mode': 'ro'}},
            working_dir='/code',
            remove=True,
            stdout=True,
            stderr=True,
            detach=False,
            mem_limit='100m',  # Limit memory usage
            cpu_period=100000,
            cpu_quota=50000,  # Limit CPU usage to 50%
            timeout=10  # Timeout of 10 seconds
        )

        result = container.decode('utf-8')
    except docker.errors.ContainerError as e:
        result = f"Error: {str(e)}"
    except docker.errors.APIError as e:
        result = f"Docker API Error: {str(e)}"
    except Exception as e:
        result = f"Unexpected error: {str(e)}"
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

    return {
        "code_execution_result": f"Execution result of:\n{state.code_editor_state}\n\nOutput:\n{result}"
    }

g = StateGraph(OverallState)
g.add_edge(START, n(execute_code))

g.add_node(execute_code)
g.add_edge(n(execute_code), END)

code_interpreter_graph = g.compile()