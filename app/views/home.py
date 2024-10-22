from fasthtml.common import *

from app.views.components.header import header_component

from interview_questions import INTERVIEW_QUESTION_AND_SOLUTION

def home_view(request):
    return (
        Title("AI Coding Interview Agent"),
        Main(cls="container")(
            header_component(),
            Div(
                cls="question-cards",
                style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 20px;",
            )(
                *[
                    Form(
                        hx_post="/init",
                        hx_target="body",
                        hx_swap="outerHTML",
                        hx_replace_url="true",
                        cls="card",
                        style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; transition: box-shadow 0.3s ease-in-out;",
                    )(
                        H3(
                            question["difficulty_level"].capitalize(),
                            style="margin-top: 0; color: #333;",
                        ),
                        P(question["question"], style="color: #666;"),
                        Input(
                            type="hidden",
                            name="difficulty",
                            value=question["difficulty_level"],
                        ),
                        Input(
                            type="hidden", name="question", value=question["question"]
                        ),
                        Input(
                            type="hidden", name="solution", value=question["solution"]
                        ),
                        Div(style="display: flex; justify-content: flex-end; margin-top: 15px;")(
                            Button(
                                "Start Interview",
                                cls="btn btn-primary",
                                style="background-color: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; transition: background-color 0.3s ease-in-out;",
                            ),
                        ),
                    )
                    for question in INTERVIEW_QUESTION_AND_SOLUTION
                ]
            ),
        ),
        Style(
            """
            .card:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .btn-primary:hover {
                background-color: #0056b3;
            }
        """
        ),
    )
