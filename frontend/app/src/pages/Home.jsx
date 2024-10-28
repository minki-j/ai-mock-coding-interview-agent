import INTERVIEW_QUESTIONS from '../assets/interview_questions';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handleStartInterview = async (question) => {
    navigate(`/interview?`);
  };

  console.log(INTERVIEW_QUESTIONS);
    
  return (
    <div className="question-cards" style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '20px',
      padding: '20px'
    }}>
      {INTERVIEW_QUESTIONS.map((question, index) => (
        <div key={index} className="card" style={{
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '20px',
          transition: 'box-shadow 0.3s ease-in-out'
        }}>
          <h3 style={{ marginTop: 0, color: '#333' }}>
            {question.difficulty_level.charAt(0).toUpperCase() + question.difficulty_level.slice(1)}
          </h3>
          <p style={{ height: '500px', overflowY: 'auto' }}>
            {question.question}
          </p>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '15px' }}>
            <button
              onClick={() => handleStartInterview(question)}
              className="btn btn-primary"
              style={{
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                padding: '10px 15px',
                borderRadius: '5px',
                cursor: 'pointer',
                transition: 'background-color 0.3s ease-in-out'
              }}
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
