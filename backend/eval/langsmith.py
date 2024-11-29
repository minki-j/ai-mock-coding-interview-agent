from langsmith import evaluate, Client
from langsmith.schemas import Example, Run
from agents.main_graph import main_graph

client = Client()
dataset = client.clone_public_dataset(
    "https://smith.langchain.com/public/a63525f9-bdf2-4512-83e3-077dc9417f96/d"
)

def predict_assistant(example: dict):
    """Invoke assistant for single tool call evaluation"""
    msg = [("user", example["input"])]
    result = main_graph.invoke({"messages": msg})
    return {"response": result}


def check_specific_tool_call(root_run: Run, example: Example) -> dict:
    """
    Check if the first tool call in the response matches the expected tool call.
    """
    # Expected tool call
    expected_tool_call = "sql_db_list_tables"

    # Run
    response = root_run.outputs["response"]

    # Get tool call
    try:
        tool_call = getattr(response, "tool_calls", [])[0]["name"]
    except (IndexError, KeyError):
        tool_call = None

    score = 1 if tool_call == expected_tool_call else 0
    return {"score": score, "key": "thought_process"}


experiment_results = evaluate(
    predict_assistant,
    data=dataset,
    evaluators=[check_specific_tool_call],
    experiment_prefix="thought_process",
    num_repetitions=2,
    metadata={"version": "thought_process_v1"},
)
