import os
import json
import subprocess
import tempfile
import uuid
from varname import nameof as n
from operator import add
from pydantic import BaseModel, Field
from typing import Annotated

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv("../../.env", override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
chat_model = ChatOpenAI(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
    temperature=0.7,
)

def list_reducer(original: list, new_edge_cases: list):
    print(f"original: {original}")
    print(f"new_edge_cases: {new_edge_cases}")
    return original + new_edge_cases


class Output(BaseModel):
    new_edge_cases: Annotated[list[dict], list_reducer] = Field(default=[])
    completed: bool = Field(default=False)


class OverallState(Output):
    interview_question: str
    test_code_template: str
    constraints: str
    solution: str
    existing_examples: list[dict]
    max_num_of_edge_cases: int = Field(default=3)
    max_debug_count: int = Field(default=3)
    debug_count: int = Field(default=0)

    temp_edge_case: dict = Field(default={})
    output_generated: bool = Field(default=False)
    error_message: str = Field(default="")


def generate_new_edge_case(state: OverallState):
    class NewEdgeCase(BaseModel):
        think_out_loud: str = Field(
            description="Think step by step about the algorithm and the constraints. Then, analyze the test cases generated so far one by one, examining what kind of edge cases they cover. Then, reason what kind of new edge cases there might be left to generate. think_out_loud value is the most important part of this task, so be specific and detailed in this reasoning process. "
        )
        does_new_edge_case_exist: bool = Field(
            description="Return False if you think there is no more edge cases to generate. Otherwise, return True."
        )
        input: str = Field(
            description="The input to the function. Make sure the type matches the input type in the solution code. Follow the same format as the existing test cases. If does_new_edge_case_exist is False, leave this blank."
        )
        label: str = Field(
            description="The short label of the new edge case. If does_new_edge_case_exist is False, leave this blank."
        )

    new_edge_case = (
        ChatPromptTemplate.from_template(
            """
You are an expert test case generator. Your task is to analyze a LeetCode interview question and generate edge cases that thoroughly test the solution.

You will:
1. Carefully read and understand the interview question, constraints, and solution
2. Review the existing test cases and any newly generated edge cases
3. Think critically about what edge cases are not yet covered
4. Generate a new edge case that tests an uncovered scenario, or determine if all important edge cases are covered
5. For any new edge case, explain why it is important to test that specific scenario

When generating edge cases, consider:
- Boundary conditions and limits
- Special input formats or patterns
- Empty/null/invalid inputs
- Minimum and maximum values
- Complex interactions between inputs
- Common pitfalls and gotchas

---

## Interview Question
{interview_question}

## Constraints
{constraints}

## Solution
{solution}  

## Generated edge case so far
{test_cases}

---

## Keep in mind that:
- the edge case should follow the constraints.
- the edge case should not be the same as the existing test cases.
- the edge case should not be trivial to the solution. For instance, when the input has 2 elements, and the ouput is selecting two elements out of the input, the possible answer is only one, which is trivial. 
- the input should be in the same format as the existing test cases.
"""
        )
        | chat_model.with_structured_output(NewEdgeCase)
    ).invoke(
        {
            "interview_question": state.interview_question,
            "constraints": state.constraints,
            "solution": state.solution,
            "test_cases": json.dumps(state.existing_examples + state.new_edge_cases),
        }
    )

    if new_edge_case.does_new_edge_case_exist:
        return {
            "temp_edge_case": {
                "input": new_edge_case.input,
                "label": new_edge_case.label,
            },
            "debug_count": 0,
        }
    else:
        return {
            "completed": True,
        }


def check_constraints(state: OverallState):

    class UpdatedEdgeCase(BaseModel):
        think_out_loud: str = Field(
            description="Think step by step whether the edge case meets the constraints or not. This is the most important part of this task, so be specific and detailed in this reasoning process and take as much time as you need. "
        )
        does_meet_constraints: bool = Field(
            description="Return True if the edge case meets the constraints. Otherwise, return False."
        )
        modified_input: str = Field(
            description="The input to the function. If does_meet_constraints is True, leave this blank."
        )

    response = (
        ChatPromptTemplate.from_template(
            """
Check if the following edge case follows the constraints.

---

## Interview Question
{interview_question}

## Constraints
{constraints}

## Solution
{solution}

## Generated edge case so far
{test_cases}

---

## edge case to examine
{edge_case}

---

## Keep in mind that:
- If the edge case does not follow the constraints, modify the edge case so that it follows the constraints. When modifying the edge case, make sure the edge case is still covering a new edge case, meaning it should not be the same as the existing edge cases.
- When the constraints says there is only one valid answer, make sure you check if there is only one possible output. This is important since the solution code will only return one output in this case.
"""
        )
        | chat_model.with_structured_output(UpdatedEdgeCase)
    ).invoke(
        {
            "interview_question": state.interview_question,
            "constraints": state.constraints,
            "solution": state.solution,
            "test_cases": json.dumps(state.existing_examples + state.new_edge_cases),
            "edge_case": json.dumps(state.temp_edge_case),
        }
    )

    updated_edge_case = state.temp_edge_case
    if not response.does_meet_constraints:
        updated_edge_case["input"] = response.modified_input

    return {
        "temp_edge_case": updated_edge_case,
    }


def get_edge_case_output(state: OverallState):
    input_variables = state.temp_edge_case["input"]
    func_name = state.test_code_template.split("solution.")[1].split("(")[0].strip()
    code = (
        state.solution
        + "\n\n"
        + "if __name__ == '__main__':\n    "
        + f"solution = Solution()\n    result = solution.{func_name}({input_variables})"
        + "\n    print(result)"
    )
    try:
        output = subprocess.check_output(["python", "-c", code], text=True)
    except Exception as e:
        print(f"==>> error: {e}")
        return {
            "output_generated": False,
            "error_message": str(e),
        }
    return {
        "temp_edge_case": {
            "input": input_variables,
            "output": output.strip(),
            "label": state.temp_edge_case["label"],
        },
        "output_generated": True,
    }


def did_output_generated(state: OverallState):
    if state.debug_count >= state.max_debug_count:
        return "end_of_loop"

    if state.output_generated:
        return "add_new_edge_case"
    else:
        return n(debug_generated_edge_case)


def debug_generated_edge_case(state: OverallState):

    class NewEdgeCase(BaseModel):
        think_out_loud: str = Field(
            description="Think step by step about the error message and the edge case. Then, debug the edge case so that it will pass with the solution code."
        )
        input: str = Field(description="The input to the function.")

    debugged_edge_case = (
        ChatPromptTemplate.from_template(
            """
## Context
You are an expert test case generator. Your task is to analyze a LeetCode interview question and generate edge cases that thoroughly test the solution.
You've already generated a new edge case input. However, the solution code returned an error when used the input. Please debug the edge case input so that it will pass with the solution 

---

## Interview Question
{interview_question}

## Constraints
{constraints}

## Solution
{solution}  

## Generated edge case so far
{test_cases}

---

## The edge case that failed
{edge_case}

## Error message
{error_message}

---

## Keep in mind that:
- the edge case should follow the constraints.
- the edge case should not be the same as the existing test cases. In other words, the edge case should be covering a new edge case.
- the edge case should not be trivial to the solution. For instance, when the input has 2 elements, and the ouput is selecting two elements out of the input, the possible answer is only one, which is trivial. 
"""
        )
        | chat_model.with_structured_output(NewEdgeCase)
    ).invoke(
        {
            "interview_question": state.interview_question,
            "constraints": state.constraints,
            "solution": state.solution,
            "test_cases": json.dumps(state.existing_examples + state.new_edge_cases),
            "edge_case": json.dumps(state.temp_edge_case),
            "error_message": state.error_message,
        }
    )

    return {
        "temp_edge_case": {
            "input": debugged_edge_case.input,
            "label": state.temp_edge_case["label"],
        },
        "debug_count": state.debug_count + 1,
    }


def end_of_loop(state: OverallState):
    print(f"state.max_num_of_edge_cases: {state.max_num_of_edge_cases}")
    print(f"len(state.new_edge_cases): {len(state.new_edge_cases)}")
    if state.max_num_of_edge_cases <= len(state.new_edge_cases):
        return "break_loop"
    else:
        return n(generate_new_edge_case)


g = StateGraph(OverallState, output=Output)
g.add_edge(START, n(generate_new_edge_case))

g.add_node(generate_new_edge_case)
g.add_edge(n(generate_new_edge_case), "no_more_edge_cases")

g.add_node("no_more_edge_cases", RunnablePassthrough())
g.add_conditional_edges(
    "no_more_edge_cases",
    lambda state: "break_loop" if state.completed else n(check_constraints),
    ["break_loop", n(check_constraints)],
)

g.add_node(check_constraints)
g.add_edge(n(check_constraints), n(get_edge_case_output))

g.add_node(get_edge_case_output)
g.add_edge(n(get_edge_case_output), n(did_output_generated))

g.add_node("did_output_generated", RunnablePassthrough())
g.add_conditional_edges(
    "did_output_generated",
    did_output_generated,
    [
        n(debug_generated_edge_case),
        "add_new_edge_case",
        "end_of_loop",
    ],
)

g.add_node(debug_generated_edge_case)
g.add_edge(n(debug_generated_edge_case), n(get_edge_case_output))


def add_new_edge_case(state: OverallState):
    print(f"Add temp_edge_case: {state.temp_edge_case}")
    return {"new_edge_cases": [state.temp_edge_case]}


g.add_node(
    "add_new_edge_case", add_new_edge_case
)
g.add_edge("add_new_edge_case", "end_of_loop")

g.add_node("end_of_loop", RunnablePassthrough())
g.add_conditional_edges(
    "end_of_loop",
    end_of_loop,
    [n(generate_new_edge_case), "break_loop"],
)

g.add_node("break_loop", lambda _: {"completed": True})
g.add_edge("break_loop", END)


test_generator_graph = g.compile(
    checkpointer=MemorySaver(), interrupt_after=["end_of_loop"]
)

with open("./test_generator_graph.png", "wb") as f:
    f.write(test_generator_graph.get_graph(xray=0).draw_mermaid_png())


def load_interview_data(question_file):
    with open(f"./interview_data/{question_file}", "r") as f:
        data = json.load(f)
    content_md = data["content_md"]
    test_cases_code = data["test_code"].split("def test_2")[0].strip()
    question = content_md.split("**Example")[0].strip().replace("\n\n\n+", "\n")
    constraints = content_md.split("**Constraints:**")[1].split("**Follow")[0].strip()
    solution = data["approaches"][0]["implementation_code"]
    existing_examples = data["test_input_output"]
    return question, test_cases_code, constraints, solution, existing_examples


if __name__ == "__main__":
    question_files = os.listdir("interview_data")

    for question_file in question_files:
        print(f"Generating edge cases for {question_file}")
        question, test_cases_code, constraints, solution, existing_examples = (
            load_interview_data(question_file)
        )

        state = OverallState(
            interview_question=question,
            test_code_template=test_cases_code,
            constraints=constraints,
            solution=solution,
            existing_examples=existing_examples,
        )
        new_edge_cases = None
        config = {
            "configurable": {"thread_id": question_file + str(uuid.uuid4())},
        }
        while True:
            output = test_generator_graph.invoke(state, config)

            if len(output["new_edge_cases"]) > 0:
                print(output["new_edge_cases"])
                # print("New edge cases: ", output["new_edge_cases"][-1])


            if len(output["new_edge_cases"]) >= 3:
                new_edge_cases = output["new_edge_cases"]
                break

            answer = input("Continue?")
            if answer.lower() != "y":
                break

        with open(f"./edge_cases/{question_file}", "w") as f:
            json.dump(new_edge_cases, f)

        print("-" * 50)
