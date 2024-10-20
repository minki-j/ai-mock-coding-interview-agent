import os
import uuid
from app.agents.main_graph import main_graph

thread_id = str(uuid.uuid4())
print(f"==>> thread_id: {thread_id}")
config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 100}

result = main_graph.invoke({"difficulty_level": "easy"}, config)

print("-" * 50)
print("Interview Question:", result["interview_question"])
print("-" * 50)
print("\n\n")

while True:
    user_message = input("Type your message to the interviewer:\n")
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
