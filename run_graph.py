import datetime
import os
import uuid
from interview_questions import INTERVIEW_QUESTION_AND_SOLUTION
from app.agents.main_graph import main_graph

thread_id = str(uuid.uuid4())
print(f"==>> thread_id: {thread_id}")
config = {"configurable": {"thread_id": thread_id, "get_code_feedback": False}, "recursion_limit": 100}

# result = main_graph.invoke({"difficulty_level": "hard"}, config)
main_graph.update_state(config, {
    "start_time": datetime.datetime.now(),
    "difficulty_level": "hard",
    "interview_question": INTERVIEW_QUESTION_AND_SOLUTION[2]["question"],
    "interview_solution": INTERVIEW_QUESTION_AND_SOLUTION[2]["solution"],
})
main_graph.invoke(None, config)

print("-" * 50)
state = main_graph.get_state(config)
print("Interview Question:", state.values["interview_question"])
print("-" * 50)
print("\n\n")

while True:
    user_message = input("Type your message to the interviewer:\n")

    if "```python" in user_message:
        # TODO: Placeholder code to separate text and coding inputs till we have UI integration
        user_code = user_message[user_message.find("```python") + len("```python"):user_message.rfind("```")]
        user_message = user_message.replace(user_code, "").strip()
        config["configurable"]["get_code_feedback"] = True
        main_graph.update_state(
            config,
            {
                "messages": [{"role": "user", "content": user_message}],
                "code_editor_state": user_code
            },
        )
    else:
        config["configurable"]["get_code_feedback"] = False
        main_graph.update_state(
            config,
            {"messages": [{"role": "user", "content": user_message}]},
        )
    result = main_graph.invoke(None, config)

    print("-" * 50)
    print("Interviewer replied:\n", result["message_from_interviewer"])
    print("-" * 50)
    input("Press Enter to continue...")
    print("\n\n")
