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

from agents.subgraphs.coding_stage import prompts

from agents.subgraphs.code_feedback_agent.graph import code_feedback_agent_graph


def answer_general_question(state: OverallState):
    print("\n>>> NODE: answer_general_question")

    reply = (
        ChatPromptTemplate.from_template(prompts.DEFAULT_FEEDBACK_PROMPT) | chat_model
    ).invoke(
        {
            "messages": "\n\n".join(
                [
                    f">>{message.type}: {message.content}"
                    for message in state.messages[-4:]  # last 4 messages
                ]
            ),
            "code_editor_state": state.code_editor_state,
            "interview_question": state.interview_question,
        }
    )

    return {
        "message_from_interviewer": reply.content,
    }


def check_if_solution_is_leaked(state: OverallState):
    print("\n>>> NODE: check_if_solution_is_leaked")

    class SolutionEliminationResponse(BaseModel):
        is_solution_revealed: bool = Field(
            description="Whether the solution is revealed in the feedback."
        )
        amended_feedback: str = Field(
            description="If solution is revealed, amend the feedback so that the solution is not revealed. If the solution is not revealed, return an empty string."
        )

    validation_result = (
        ChatPromptTemplate.from_template(prompts.SOLUTION_ELIMINATION_PROMPT)
        | chat_model.with_structured_output(SolutionEliminationResponse)
    ).invoke(
        {
            "question": state.interview_question,
            "solution": state.interview_solution,
            "feedback": state.message_from_interviewer,
        }
    )

    if validation_result.is_solution_revealed:
        return {
            "message_from_interviewer": validation_result.amended_feedback,
            "messages": [AIMessage(content=validation_result.amended_feedback)],
        }
    else:
        return {
            "messages": [AIMessage(content=state.message_from_interviewer)],
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

    response = (
        ChatPromptTemplate.from_template(prompts.USER_INTENT_CLASSIFIER_PROMPT)
        | chat_model.with_structured_output(UserIntentResponse)
    ).invoke(
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
        return n(code_feedback_agent_graph)
    elif response.user_intent == Intent.GENERAL_QUESTION:
        return n(answer_general_question)
    else:
        raise ValueError(f"Invalid user intent: {response.user_intent}")


def just_started_feedback_agent(state: OverallState):
    if state.stage != "coding":
        return "parallel_execution"
    return n(user_intent_classifier)


def generate_first_reply(state: OverallState):
    first_reply = (
        ChatPromptTemplate.from_template(prompts.FIRST_REPLY_PROMPT)
        | chat_model
        | StrOutputParser()
    ).invoke(
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
    thought_process_summary = (
        ChatPromptTemplate.from_template(prompts.THOUGHT_PROCESS_SUMMARY_PROMPT)
        | chat_model
        | StrOutputParser()
    ).invoke(
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
    [n(user_intent_classifier), "parallel_execution"],
)

g.add_node("parallel_execution", RunnablePassthrough())
g.add_edge("parallel_execution", n(generate_first_reply))
g.add_edge("parallel_execution", n(summarize_thought_process))

g.add_node(generate_first_reply)
g.add_edge(n(generate_first_reply), "rendezvous")

g.add_node(summarize_thought_process)
g.add_edge(n(summarize_thought_process), "rendezvous")

g.add_node("rendezvous", RunnablePassthrough())
g.add_edge("rendezvous", END)

g.add_node(n(user_intent_classifier), RunnablePassthrough())
g.add_conditional_edges(
    n(user_intent_classifier),
    user_intent_classifier,
    [n(code_feedback_agent_graph), n(answer_general_question)],
)

g.add_node(n(code_feedback_agent_graph), code_feedback_agent_graph)
g.add_edge(n(code_feedback_agent_graph), n(check_if_solution_is_leaked))

g.add_node(n(answer_general_question), answer_general_question)
g.add_edge(n(answer_general_question), n(check_if_solution_is_leaked))

g.add_node(check_if_solution_is_leaked)
g.add_edge(n(check_if_solution_is_leaked), END)

coding_stage_graph = g.compile()
