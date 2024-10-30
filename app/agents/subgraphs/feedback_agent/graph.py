import os
from varname import nameof as n

from langgraph.graph import START, END, StateGraph

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState
from app.agents.llm_models import chat_model

from app.agents.subgraphs.feedback_agent import prompts

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

    chain =  ChatPromptTemplate.from_template(prompts.SOLUTION_ELIMINATION_PROMPT) | chat_model

    validated_response = chain.invoke({
            'question': state.interview_question,
            'solution': state.interview_solution,
            'feedback': feedback_response.content
        })

    return {
        "message_from_interviewer": validated_response.content,
        "messages": [validated_response],
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
g.add_conditional_edges(n(should_generate_code_feedback), should_generate_code_feedback)

g.add_edge(n(generate_code_feedback), END)
g.add_edge(n(generate_default_feedback), END)

feedback_agent_graph = g.compile()
