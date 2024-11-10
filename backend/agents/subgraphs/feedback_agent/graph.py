import os
from varname import nameof as n
from pydantic import BaseModel, Field
from langgraph.graph import START, END, StateGraph

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from agents.state_schema import OverallState
from agents.llm_models import chat_model

from agents.subgraphs.feedback_agent import prompts


def generate_default_feedback(state: OverallState):
    print("\n>>> NODE: generate_default_feedback")

    messages = [SystemMessage(content=prompts.TURN_N_ASSESSMENT_SYSTEM_PROMPT)]

    last_user_message = None
    for message in state.messages:
        if message.type != "system":
            messages.append(message)
            if message.type == "human":
                last_user_message = message

    # Add user code to last user message
    if last_user_message:
        last_user_message.content = (
            f"{last_user_message.content}\n\n{state.code_editor_state}"
        )

    chain = ChatPromptTemplate.from_messages(messages) | chat_model
    assessment_response = chain.invoke(
        {
            "question": state.interview_question,
            "solution": state.interview_solution,
        }
    )

    chain = (
        ChatPromptTemplate.from_template(prompts.SOLUTION_ELIMINATION_PROMPT)
        | chat_model
    )

    feedback_response = chain.invoke(
        {
            "question": state.interview_question,
            "solution": state.interview_solution,
            "feedback": assessment_response.content,
        }
    )

    return {
        "message_from_interviewer": feedback_response.content,
        "messages": [feedback_response],
    }


def generate_code_feedback(state: OverallState):
    print("\n>>> NODE: generate_code_feedback")

    chain = ChatPromptTemplate.from_template(prompts.ASSESSMENT_PROMPT) | chat_model

    assessment_response = chain.invoke(
        {
            "question": state.interview_question,
            "correct_solution": state.interview_solution,
            "user_solution": state.code_editor_state,
        }
    )

    chain = ChatPromptTemplate.from_template(prompts.FEEDBACK_PROMPT) | chat_model

    feedback_response = chain.invoke(
        {
            "question": state.interview_question,
            "user_solution": state.code_editor_state,
            "assessment": assessment_response.content,
        }
    )

    class SolutionEliminationResponse(BaseModel):
        is_solution_revealed: bool = Field(
            description="Whether the solution is revealed in the feedback."
        )
        amended_feedback: str = Field(
            description="The feedback with the solution removed. If the solution is not revealed, return an empty string."
        )

    chain = ChatPromptTemplate.from_template(
        prompts.SOLUTION_ELIMINATION_PROMPT
    ) | chat_model.with_structured_output(SolutionEliminationResponse)

    validation_result = chain.invoke(
        {
            "question": state.interview_question,
            "solution": state.interview_solution,
            "feedback": feedback_response.content,
        }
    )

    if validation_result.is_solution_revealed:
        feedback_response.content = validation_result.amended_feedback

    return {
        "message_from_interviewer": feedback_response.content,
        "messages": [feedback_response],
    }


def should_generate_code_feedback(state: OverallState, config):
    if config["configurable"]["get_code_feedback"]:
        return n(generate_code_feedback)
    return n(generate_default_feedback)


def just_started_feedback_agent(state: OverallState):
    if state.stage != "coding":
        return n(generate_first_reply)
    return n(generate_default_feedback)


def generate_first_reply(state: OverallState):
    chain = (
        ChatPromptTemplate.from_template(
            """
You are interviewing a candidate for a software engineering role. There are two stages of the interview. A) Thought process stage: The candidate is thinking out loud about the problem. B) Actual coding stage: The candidate is writing code to solve the problem.
You've been in the thought process stage and now it's time to move on to the actual coding stage. 

--- 

## current conversation
{messages}

--- 

## predefined reply
Great job on the thought process! Now, let’s dive into coding:
1. Use the code editor on the right to start implementing your ideas.
2. Feel free to adjust your plan, but let me know here if you do.
3. You can ask for feedback at any stage—I’ll provide tips without giving away the full solution.
4. If you need any clarification, just ask.
Alright, let’s start coding!

---

Modify the predefined reply to fit in the conversation. Only return the modified reply without any other text such as "Here is the modified reply:" or anything like that.
"""
        )
        | chat_model
        | StrOutputParser()
    )

    reply = chain.invoke(
        {
            "messages": "\n".join(
                [
                    f">>{message.type.upper()}: {message.content}"
                    for message in state.messages[1:]
                ]
            )
        }
    )

    return {
        "stage": "coding",
        "message_from_interviewer": reply,
        "messages": [AIMessage(content=reply)],
    }


g = StateGraph(OverallState)

g.add_edge(START, n(just_started_feedback_agent))

g.add_node(n(just_started_feedback_agent), RunnablePassthrough())
g.add_conditional_edges(
    n(just_started_feedback_agent),
    just_started_feedback_agent,
    [n(generate_first_reply), n(should_generate_code_feedback)],
)

g.add_node(generate_first_reply)
g.add_edge(n(generate_first_reply), END)


g.add_node(n(should_generate_code_feedback), RunnablePassthrough())
g.add_conditional_edges(
    n(should_generate_code_feedback),
    should_generate_code_feedback,
    [n(generate_code_feedback), n(generate_default_feedback)],
)

g.add_node(n(generate_code_feedback), generate_code_feedback)
g.add_edge(n(generate_code_feedback), END)

g.add_node(n(generate_default_feedback), generate_default_feedback)
g.add_edge(n(generate_default_feedback), END)

feedback_agent_graph = g.compile()
