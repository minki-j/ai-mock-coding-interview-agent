import INTERVIEW_QUESTIONS from '../assets/interview_questions';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handleStartInterview = async (question) => {
    navigate(`/interview/${question.id}`);
  };
    
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 p-5">
      {INTERVIEW_QUESTIONS.map((question, index) => (
        <div key={index} className="border border-gray-200 rounded-lg p-5 transition-shadow hover:shadow-lg">
          <h3 className="mt-0 text-gray-700 capitalize">
            {question.difficulty_level}
          </h3>
          <p className="h-[500px] overflow-y-auto">
            {question.question}
          </p>
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

Home.propTypes = {
  handleStartInterview: PropTypes.func.isRequired
};

export default Home;
