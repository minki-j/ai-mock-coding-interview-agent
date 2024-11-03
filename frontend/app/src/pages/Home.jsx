import INTERVIEW_QUESTIONS from "../assets/interview_questions";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleStartInterview = async (question) => {
    const response = await fetch("/init_interview", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        interview_question: question.question,
        interview_solution: question.solution,
      }),
    });
    if (response.ok) {
      const data = await response.json();
      navigate(`/interview/${data.interview_id}`);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 p-5">
      {INTERVIEW_QUESTIONS.map((question, index) => (
        <div
          key={index}
          className="border border-gray-200 rounded-lg p-5 transition-shadow hover:shadow-lg"
        >
          <h3 className="mt-0 text-gray-700 capitalize">
            {question.difficulty_level}
          </h3>
          <p className="h-[500px] overflow-y-auto">{question.question}</p>
          <div className="flex justify-end mt-4">
            <button
              onClick={() => handleStartInterview(question)}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
            >
              Start Interview
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};


export default Home;
