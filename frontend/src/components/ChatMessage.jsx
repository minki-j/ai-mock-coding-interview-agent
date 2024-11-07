import PropTypes from 'prop-types';

const ChatMessage = ({ role, content }) => {
  const alignment = role === 'AI' ? 'justify-start' : 'justify-end';

  return (
    <div className={`flex ${alignment}`}>
      <div className="mb-4 p-4 border border-gray-200 rounded-3xl max-w-[70%] relative shadow-md">
        <div className="text-sm tracking-wider">
          <strong>{role}</strong>
        </div>
        <div className="mt-2">
          <p>{content}</p>
        </div>
      </div>
    </div>
  );
};

ChatMessage.propTypes = {
  role: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired
};

export default ChatMessage;
