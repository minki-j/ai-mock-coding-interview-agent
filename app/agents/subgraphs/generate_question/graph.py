import datetime
import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState


def pick_a_question(state: OverallState):
    print("\n>>> NODE: pick_a_question")

    return {
        "interview_question": "Write a Python function called is_even that takes an integer as input and returns True if the number is even, and False if the number is odd.",
        "interview_solution": "```python\ndef is_even(number):\n\treturn number % 2 == 0\n```",
        "start_time": datetime.datetime.now(),
        "is_question_generated": True,
    }

g = StateGraph(OverallState)
g.add_edge(START, n(pick_a_question))

g.add_node(pick_a_question)
g.add_edge(n(pick_a_question), END)

generate_question_graph = g.compile()
