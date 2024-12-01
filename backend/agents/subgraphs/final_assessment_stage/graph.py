import os
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from agents.state_schema import OverallState
from langgraph.checkpoint.memory import MemorySaver
from agents.llm_models import chat_model

from agents.subgraphs.final_assessment_stage import prompts

class AssessmentResponse(BaseModel):
    rationale: str = Field(
        description="A step by step rationale for choosing your rating. Make sure you include evidence from the transcript and code to justify the rating."
    )
    rating: str = Field(
        description="Choose the best matching ration from Poor, Borderline, Solid and Outstanding based on your rationale."
    )


class OverallAssessmentPrivateState(BaseModel):
    code_comprehension_asessment: AssessmentResponse = Field(default=None)
    programming_assessment: AssessmentResponse = Field(default=None)
    data_structures_and_algorithms_assessment: AssessmentResponse = Field(default=None)
    testing_and_debugging_assessment: AssessmentResponse = Field(default=None)
    growth_mindset_assessment: AssessmentResponse = Field(default=None)


def assess_code_comprehension(state: OverallState) -> OverallAssessmentPrivateState:
    assessment_response = (
        ChatPromptTemplate.from_template(prompts.CODE_COMPREHENSION_ASSESSMENT_PROMPT)
        | chat_model.with_structured_output(AssessmentResponse)
    ).invoke(
        {
            "interview_transcript": state.stringify_messages(),
            "user_submitted_code": state.code_editor_state,
        }
    )
    return {
        'code_comprehension_asessment': assessment_response
    }

def assess_programming(state: OverallState) -> OverallAssessmentPrivateState:
    assessment_response = (
        ChatPromptTemplate.from_template(prompts.PROGRAMMING_ASSESSMENT_PROMPT)
        | chat_model.with_structured_output(AssessmentResponse)
    ).invoke(
        {
            "interview_transcript": state.stringify_messages(),
            "user_submitted_code": state.code_editor_state,
        }
    )
    return {"programming_assessment": assessment_response}

def assess_data_structures_and_algorithms(state: OverallState) -> OverallAssessmentPrivateState:
    assessment_response = (
        ChatPromptTemplate.from_template(prompts.DATA_STRUCTURES_AND_ALGORITHMS_ASSESSMENT_PROMPT)
        | chat_model.with_structured_output(AssessmentResponse)
    ).invoke(
        {
            "interview_transcript": state.stringify_messages(),
            "user_submitted_code": state.code_editor_state,
        }
    )
    return {"data_structures_and_algorithms_assessment": assessment_response}

def assess_debugging_and_testing(state: OverallState) -> OverallAssessmentPrivateState:
    assessment_response = (
        ChatPromptTemplate.from_template(prompts.TESTING_AND_DEBUGGING_SKILLS)
        | chat_model.with_structured_output(AssessmentResponse)
    ).invoke(
        {
            "interview_transcript": state.stringify_messages(),
            "user_submitted_code": state.code_editor_state,
        }
    )
    return {"testing_and_debugging_assessment": assessment_response}

def assess_growth_mindset(state: OverallState) -> OverallAssessmentPrivateState:
    assessment_response = (
        ChatPromptTemplate.from_template(prompts.GROWTH_MINDSET_ASSESSMENT_PROMPT)
        | chat_model.with_structured_output(AssessmentResponse)
    ).invoke(
        {
            "interview_transcript": state.stringify_messages(),
            "user_submitted_code": state.code_editor_state,
        }
    )
    return {"growth_mindset_assessment": assessment_response}

def compile_assessment(state: OverallAssessmentPrivateState) -> OverallState:
    assessment_response = (
        ChatPromptTemplate.from_template(prompts.ASSESSMENT_COMPILING_PROMPT)
        | chat_model
    ).invoke(
        {
            "code_comprehension": state.code_comprehension_asessment,
            "programming": state.programming_assessment,
            "data_structures_and_algorithms": state.data_structures_and_algorithms_assessment,
            "testing_and_debugging": state.testing_and_debugging_assessment,
            "growth_mindset": state.growth_mindset_assessment
        }
    )
    
    return {
            "display_decision": "Generated the final report using the 5 assessments.",
            "message_from_interviewer": assessment_response.content,
            "messages": [AIMessage(content=assessment_response.content)],
        }

g = StateGraph(OverallState)
g.add_edge(START, "start")
g.add_node("start", RunnablePassthrough())

g.add_node(n(assess_code_comprehension), assess_code_comprehension)
g.add_node(n(assess_programming), assess_programming)
g.add_node(n(assess_data_structures_and_algorithms), assess_data_structures_and_algorithms)
g.add_node(n(assess_debugging_and_testing), assess_debugging_and_testing)
g.add_node(n(assess_growth_mindset), assess_growth_mindset)
g.add_node(n(compile_assessment), compile_assessment)

g.add_edge("start", n(assess_code_comprehension))
g.add_edge("start", n(assess_programming))
g.add_edge("start", n(assess_data_structures_and_algorithms))
g.add_edge("start", n(assess_debugging_and_testing))
g.add_edge("start", n(assess_growth_mindset))

g.add_edge(n(assess_code_comprehension), "rendezvous")
g.add_edge(n(assess_programming), "rendezvous")
g.add_edge(n(assess_data_structures_and_algorithms), "rendezvous")
g.add_edge(n(assess_debugging_and_testing), "rendezvous")
g.add_edge(n(assess_growth_mindset), "rendezvous")

g.add_node("rendezvous", lambda state: {
    "display_decision": "Assessed your interview with 5 different aspects in parallel.",
})
g.add_edge("rendezvous", n(compile_assessment))

g.add_edge(n(compile_assessment), END)

final_assessment_stage_graph = g.compile(
    checkpointer=MemorySaver(),
    interrupt_after=["rendezvous", n(compile_assessment)],
)
