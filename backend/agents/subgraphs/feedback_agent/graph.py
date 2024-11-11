import os
from varname import nameof as n
from pydantic import BaseModel, Field
from enum import Enum
from langgraph.graph import START, END, StateGraph

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from agents.state_schema import OverallState
from agents.llm_models import chat_model

from agents.subgraphs.feedback_agent import prompts


def answer_general_question(state: OverallState):
    print("\n>>> NODE: answer_general_question")

    chain = (
        ChatPromptTemplate.from_template(prompts.DEFAULT_FEEDBACK_PROMPT) | chat_model
    )
    feedback_response = chain.invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type}: {message.content}"
                    for message in state.messages[-4:]  # last 4 messages
                ]
            ),
            "code_editor_state": state.code_editor_state,
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


def user_intent_classifier(state: OverallState):

    class Intent(Enum):
        GENERAL_QUESTION = "asking_general_question"
        CODE_FEEDBACK = "asking_for_code_feedback"

    class UserIntentResponse(BaseModel):
        rationale: str = Field(description="The rationale for the user's intent.")
        user_intent: Intent = Field(
            description="If the user's intent is 'asking_general_question', the user is asking a question about details of a library, API, or general programming knowledge that is not the complete solution to the problem.\n\nIf the user's intent is 'asking_for_code_feedback', the user wants to get feedback on their code solution."
        )

    chain = ChatPromptTemplate.from_template(
        prompts.USER_INTENT_CLASSIFIER_PROMPT
    ) | chat_model.with_structured_output(UserIntentResponse)

    response = chain.invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type.upper()}: {message.content}"
                    for message in state.messages[-4:]  # last 4 messages
                ]
            ),
        }
    )

    if response.user_intent == Intent.CODE_FEEDBACK:
        return n(generate_code_feedback)
    elif response.user_intent == Intent.GENERAL_QUESTION:
        return n(answer_general_question)
    else:
        raise ValueError(f"Invalid user intent: {response.user_intent}")


def just_started_feedback_agent(state: OverallState):
    if state.stage != "coding":
        return [n(generate_first_reply), n(summarize_thought_process)]
    return n(user_intent_classifier)


async def generate_first_reply(state: OverallState):
    """Also summarize the thought process"""
    chain = (
        ChatPromptTemplate.from_template(prompts.FIRST_REPLY_PROMPT)
        | chat_model
        | StrOutputParser()
    )
    first_reply = await chain.invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type.upper()}: {message.content}"
                    for message in state.messages[1:]
                ]
            )
        }
    )

    return {
        "stage": "coding",
        "message_from_interviewer": first_reply,
        "messages": [AIMessage(content=first_reply)],
    }


def summarize_thought_process(state: OverallState):
    chain = (
        ChatPromptTemplate.from_template(prompts.THOUGHT_PROCESS_SUMMARY_PROMPT)
        | chat_model
        | StrOutputParser()
    )
    thought_process_summary = chain.invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type.upper()}: {message.content}"
                    for message in state.messages
                ]
            )
        }
    )
    return {
        "thought_process_summary": thought_process_summary,
    }


g = StateGraph(OverallState)

g.add_edge(START, n(just_started_feedback_agent))

g.add_node(n(just_started_feedback_agent), RunnablePassthrough())
g.add_conditional_edges(
    n(just_started_feedback_agent),
    just_started_feedback_agent,
    [n(generate_first_reply), n(user_intent_classifier), n(summarize_thought_process)],
)

g.add_node(generate_first_reply)
g.add_edge(n(generate_first_reply), END)

g.add_node(summarize_thought_process)
g.add_edge(n(summarize_thought_process), END)

g.add_node(n(user_intent_classifier), RunnablePassthrough())
g.add_conditional_edges(
    n(user_intent_classifier),
    user_intent_classifier,
    [n(generate_code_feedback), n(answer_general_question)],
)

g.add_node(n(generate_code_feedback), generate_code_feedback)
g.add_edge(n(generate_code_feedback), END)

g.add_node(n(answer_general_question), answer_general_question)
g.add_edge(n(answer_general_question), END)

feedback_agent_graph = g.compile()
