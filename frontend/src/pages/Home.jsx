import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const [interviews, setInterviews] = useState([]);
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [allTopics, setAllTopics] = useState([]);

  const [isNavigating, setIsNavigating] = useState(false);

  useEffect(() => {
    const fetchInterviews = async () => {
      try {
        const response = await fetch("/get_interview_questions");
        if (response.ok) {
          const data = await response.json();
          setInterviews(data);
        }
      } catch (error) {
        console.error("Error fetching interviews:", error);
      }
    };

    fetchInterviews();
  }, []);

  useEffect(() => {
    const topics = [...new Set(interviews.flatMap(q => q.topicTags.map(tag => tag.name)))];
    setAllTopics(topics);
  }, [interviews]);

  const filteredInterviews = interviews.filter(question => {
    const difficultyMatch = !selectedDifficulty || question.difficulty === selectedDifficulty;
    const topicMatch = !selectedTopic || question.topicTags.some(tag => tag.name === selectedTopic);
    return difficultyMatch && topicMatch;
  });

  const handleStartInterview = async (question) => {
    setIsNavigating(true);
    try {
      const response = await fetch("/init_interview", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: sessionStorage.getItem("userId"),
          interviewee_name: sessionStorage.getItem("userName"),
          interview_question: question.content,
          interview_question_md: question.content_md,
          interview_solution: question.solution.content,
          interview_solution_md: question.solution_md,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        navigate(`/interview/${data.interview_id}`);
      }
    } catch (error) {
      console.error("Error initializing interview:", error);
      setIsNavigating(false);
    }
  };
  return (
    <div className="p-5">
      <div className="mb-6 flex gap-4">
        <select
          value={selectedDifficulty}
          onChange={(e) => setSelectedDifficulty(e.target.value)}
          className="border rounded-lg px-3 py-2"
        >
          <option value="">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>

        <select
          value={selectedTopic}
          onChange={(e) => setSelectedTopic(e.target.value)}
          className="border rounded-lg px-3 py-2"
        >
          <option value="">All Topics</option>
          {allTopics.map((topic, index) => (
            <option key={index} value={topic}>
              {topic}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredInterviews.map((question, index) => (
          <div
            key={index}
            className="border border-gray-200 rounded-lg p-5 transition-shadow hover:shadow-lg"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                {question.title}
              </h2>
              <span
                className={`px-3 py-1 rounded-full text-sm font-medium
                ${
                  question.difficulty === "Easy"
                    ? "bg-green-100 text-green-800"
                    : question.difficulty === "Medium"
                    ? "bg-yellow-100 text-yellow-800"
                    : "bg-red-100 text-red-800"
                }`}
              >
                {question.difficulty}
              </span>
            </div>

            <div
              className="h-[400px] overflow-y-auto prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: question.content }}
            ></div>

            <div className="mt-4 flex justify-between items-center">
              <div className="flex flex-wrap gap-2">
                {question.topicTags.map((tag, i) => (
                  <span
                    key={i}
                    className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm"
                  >
                    {tag.name}
                  </span>
                ))}
              </div>
              <button
                onClick={() => handleStartInterview(question)}
                disabled={isNavigating}
                className={`p-2 rounded-full border-2 transition-colors ${
                  isNavigating
                    ? 'border-gray-300 text-gray-300 cursor-not-allowed'
                    : 'border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white'
                }`}
                title="Start Interview"
              >
                {isNavigating ? (
                  <svg 
                    className="w-6 h-6 animate-spin" 
                    xmlns="http://www.w3.org/2000/svg" 
                    fill="none" 
                    viewBox="0 0 24 24"
                  >
                    <circle 
                      className="opacity-25" 
                      cx="12" 
                      cy="12" 
                      r="10" 
                      stroke="currentColor" 
                      strokeWidth="4"
                    ></circle>
                    <path 
                      className="opacity-75" 
                      fill="currentColor" 
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                ) : (
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    viewBox="0 0 24 24" 
                    fill="currentColor" 
                    className="w-6 h-6"
                  >
                    <path d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347c-.75.412-1.667-.13-1.667-.986V5.653Z" />
                  </svg>
                )}
              </button>
            </div>
          <div className="hidden">
            <div data-content-md={question.content_md}></div>
            <div data-solution-md={question.solution_md}></div>
          </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
