from varname import nameof as n
from pydantic import BaseModel, Field

from langgraph.graph import START, END, StateGraph

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import  AIMessage

from agents.state_schema import OverallState
from agents.subgraphs.thought_process_stage.prompts import default_system_message


from agents.llm_models import chat_model


def greeting(state: OverallState):
    print("\n>>> NODE: greeting")
    first_msg = f"Hello {state.interviewee_name.split(' ')[0]}! How are you doing today?"
    greeting_messages = [
        "The interview will have four stages:\n\n1. **Thought Process**: Walk me through your approach to solving the problem.\n2. **Coding**: Write code to implement your solution based on that approach.\n3. **Debugging**: Address edge cases and refine your code for accuracy.\n4. **Algorithmic Analysis**: Analyze the time and space complexity of your solution.\n\nDoes that sound clear to you?",
        "Great! Let's begin the thought process stage.\nPlease read the interview question above carefully, and explain how you would approach the problem. Feel free to ask clarifying questions at any point 😁",
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
        if state.messages[-1].content.strip().lower() == "skip":
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
You just started interviewing a candidate for a software engineering role. 
There are four stages in this interview: thought process, coding, debugging, and algorithmic analysis: 
- In thought process stage, you will ask the candidate to explain how they would approach solving the problem, and the candidate will answer through chat. 
- In coding stage, the candidate will write code in the code editor that is shown in the right panel. 
- In debugging stage, you will ask the candidate to address edge cases and refine their code for accuracy. 
- In algorithmic analysis stage, you will analyze the time and space complexity of the candidate's solution. 
- We only have python as the supported language in this interview. If the candidate asks about other languages, you should remind them that we only support python in this interview.
The interview question is displayed above this chat panel.

---

Predefined reply:
{predefined_reply}

---

Conversation history:
{conversation}

---

You need to decide whether to use the predefined reply or create a free-style response:

1. If the content of the predefined reply fits the conversation flow:
   - Set should_use_predefined_reply to True
   - Modify the predefined reply in amended_predefined_reply to acknowledge and respond to the candidate's latest message. For example, if the candiate said "I'm good! How are you?", then you could add the following message infront of the predefined reply: "Great to hear that! I'm doing good too!\n\n"
   - Leave free_reply empty

2. If the predefined reply doesn't fit:
   - Set should_use_predefined_reply to False 
   - Create an appropriate free-style response in free_reply that maintains the interview flow
   - Leave amended_predefined_reply empty
   - This free-style response must not contain the information from the predefined reply.

Please use markdown to format your responses.
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
