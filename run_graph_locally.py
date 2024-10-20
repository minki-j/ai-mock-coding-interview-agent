import os
import uuid
from app.agents.main_graph import main_graph


config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 100}

result = main_graph.invoke(
    {
        "difficulty_level": "easy",
    },
    config,
)

print("-" * 50)
print("Interview Question:", result["interview_question"])
print("-" * 50)
print("\n\n")

while True:
    main_graph.update_state(
        config,
        {"messages": [{"role": "user", "content": "Hi, I'm here for an interview."}]},
    )
    result = main_graph.invoke(None, config)

    print("-" * 50)
    print("Graph OUTPUT:", result["message_from_interviewer"])
    print("-" * 50)
    input("Press Enter to continue...")
    print("\n\n")
