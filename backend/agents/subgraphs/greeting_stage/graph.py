import os
from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from agents.state_schema import OverallState
from agents.subgraphs.thought_process_stage.prompts import default_system_message


from agents.llm_models import chat_model


def greeting(state: OverallState):
    print("\n>>> NODE: greeting")
    first_msg = f"Hello {state.interviewee_name}! How are you doing today?"
    skip_msg = "\n\n💡If you already know how the interview works, you can answer 'skip'"
    greeting_messages = [
        """The interview consists of four stages:

1. Thought Process: Explain your approach to solving the problem.
2. Coding: Implement your solution based on that approach.
3. Debugging: Refine your code by addressing edge cases.
4. Algorithmic Analysis: Evaluate the time and space complexity of your solution.

Does this sound clear?""",
        """Great! Let's begin the thought process stage.

Please read the interview question above carefully, and explain how you would approach the problem. Feel free to ask clarifying questions at any point 😁""",
    ]

    if len(state.messages) == 0:
        greeting_msg = first_msg
        return {
            "message_from_interviewer": greeting_msg,
            "messages": [
                default_system_message(state.interview_question_md),
                AIMessage(content=greeting_msg),
            ],
        }
    else:
        if (
            len(state.messages) > 1
            and state.messages[-1].content.strip().lower() == "skip"
        ):
            greeting_msg_index = -1
            return {
                "message_from_interviewer": greeting_messages[greeting_msg_index],
                "messages": [AIMessage(content=greeting_messages[greeting_msg_index])],
                "greeting_msg_index": greeting_msg_index,
                "stage": (
                    "greeting"
                    if greeting_msg_index < len(greeting_messages)
                    and greeting_msg_index >= 0
                    else "thought_process"
                ),
            }

        class ContextualizedGreetingMessage(BaseModel):
            rationale: str = Field(description="The rationale for the decision.")
            should_use_predefined_reply: bool = Field(
                description="Return True if the predefined reply fits in the conversation. Otherwise, return False."
            )
            amended_predefined_reply: str = Field(
                description="Return the amended predefined reply if should_use_predefined_reply is True. Otherwise, return an empty string."
            )
            free_reply: str = Field(
                description="Return the free reply if should_use_predefined_reply is False. Otherwise, return an empty string."
            )

        chain = (
            ChatPromptTemplate.from_template(
                """
You just started interviewing a candidate for a software engineering role. There are four stages in this interview: thought process, coding, debugging, and algorithmic analysis. You are going to greet the candidate and introduce how the interview will work. In thought process stage, you will ask the candidate to explain how they would approach solving the problem, and the candidate will answer through chat. In coding stage, the candidate will write code in the code editor that is shown in the right panel. The interview question is displayed above this chat panel. No code is shown in this chat panel.

---

Now you have to decide which option to use to reply to the candidate. Options are:
{predefined_reply}

---

## conversation
{conversation}

---

Reply to the candidate either using the predefined reply or just free-style.
"""
            )
            | chat_model.with_structured_output(ContextualizedGreetingMessage)
        )

        stringified_messages = "\n\n".join(
            [f">>{message.type}: {message.content}" for message in state.messages[1:]]
        )

        response = chain.invoke(
            {
                "predefined_reply": greeting_messages[state.greeting_msg_index],
                "conversation": stringified_messages,
            }
        )

        if response.should_use_predefined_reply:
            greeting_msg = response.amended_predefined_reply
            greeting_msg_index = state.greeting_msg_index + 1
        else:
            greeting_msg = response.free_reply
            greeting_msg_index = state.greeting_msg_index

        return {
            "message_from_interviewer": greeting_msg,
            "messages": [AIMessage(content=greeting_msg)],
            "greeting_msg_index": greeting_msg_index,
            "stage": (
                "greeting"
                if greeting_msg_index < len(greeting_messages)
                else "thought_process"
            ),
        }


g = StateGraph(OverallState)
g.add_edge(START, n(greeting))

g.add_node(greeting)
g.add_edge(n(greeting), END)

greeting_stage_graph = g.compile()
