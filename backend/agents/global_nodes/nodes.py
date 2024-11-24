from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, RemoveMessage
from pydantic import BaseModel, Field

from agents.state_schema import OverallState
from agents.llm_models import chat_model
from agents.global_nodes import prompts


def check_if_solution_is_leaked(state: OverallState):
    print("\n>>> NODE: check_if_solution_is_leaked")

    class SolutionEliminationResponse(BaseModel):
        rationale: str = Field(
            description="Think out loud and step by step about whether the solution is revealed in the feedback."
        )
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
            "question": state.interview_question_md,
            "solution": state.user_approach,
            "feedback": state.message_from_interviewer,
        }
    )

    if validation_result.is_solution_revealed:
        return {
            "message_from_interviewer": validation_result.amended_feedback,
            "messages": [
                RemoveMessage(id=state.messages[-1].id),
                AIMessage(content=validation_result.amended_feedback),
            ],
        }
    else:
        return {
            "message_from_interviewer": state.message_from_interviewer,
        }
