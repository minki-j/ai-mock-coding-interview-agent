import os
from varname import nameof as n
from pydantic import BaseModel, Field
from langgraph.graph import START, END, StateGraph

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from agents.state_schema import OverallState
from agents.llm_models import chat_model

from agents.subgraphs.feedback_agent import prompts

def generate_default_feedback(state: OverallState):
    print("\n>>> NODE: generate_default_feedback")

    messages = [SystemMessage(
            content=prompts.TURN_N_ASSESSMENT_SYSTEM_PROMPT
        )]
    
    last_user_message = None
    for message in state.messages:
        if message.type != "system":
            messages.append(message)
            if message.type == "human":
                last_user_message = message
            
    # Add user code to last user message
    if last_user_message:
        last_user_message.content = f"{last_user_message.content}\n\n{state.code_editor_state}"

    chain = ChatPromptTemplate.from_messages(messages) | chat_model
    assessment_response = chain.invoke({
            'question': state.interview_question,
            'solution': state.interview_solution,
        })
    
    chain =  ChatPromptTemplate.from_template(prompts.SOLUTION_ELIMINATION_PROMPT) | chat_model

    feedback_response = chain.invoke({
            'question': state.interview_question,
            'solution': state.interview_solution,
            'feedback': assessment_response.content
        })

    return {
        "message_from_interviewer": feedback_response.content,
        "messages": [feedback_response],
    }

def generate_code_feedback(state: OverallState):
    print("\n>>> NODE: generate_code_feedback")

    chain =  ChatPromptTemplate.from_template(prompts.ASSESSMENT_PROMPT) | chat_model

    assessment_response = chain.invoke({
            'question': state.interview_question,
            'correct_solution': state.interview_solution,
            'user_solution': state.code_editor_state
        })

    chain =  ChatPromptTemplate.from_template(prompts.FEEDBACK_PROMPT) | chat_model

    feedback_response = chain.invoke(
        {
            "question": state.interview_question,
            "user_solution": state.code_editor_state,
            "assessment": assessment_response.content,
        }
    )

    class SolutionEliminationResponse(BaseModel):
        is_solution_revealed: bool = Field(description="Whether the solution is revealed in the feedback.")
        amended_feedback: str = Field(description="The feedback with the solution removed. If the solution is not revealed, return an empty string.")

    chain = ChatPromptTemplate.from_template(
        prompts.SOLUTION_ELIMINATION_PROMPT
    ) | chat_model.with_structured_output(SolutionEliminationResponse)

    validation_result = chain.invoke({
            'question': state.interview_question,
            'solution': state.interview_solution,
            'feedback': feedback_response.content
        })

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

g = StateGraph(OverallState)

g.add_node(n(should_generate_code_feedback), RunnablePassthrough())
g.add_edge(START, n(should_generate_code_feedback))

g.add_node(n(generate_code_feedback), generate_code_feedback)
g.add_node(n(generate_default_feedback), generate_default_feedback)
g.add_conditional_edges(n(should_generate_code_feedback), should_generate_code_feedback, [n(generate_code_feedback), n(generate_default_feedback)]) # add the list of nodes to display diagram correctly

g.add_edge(n(generate_code_feedback), END)
g.add_edge(n(generate_default_feedback), END)

feedback_agent_graph = g.compile()
