import PropTypes from "prop-types";
import ReactMarkdown from 'react-markdown';

const ChatMessage = ({ role, content}) => {

  return (
    <div
      className={`flex flex-col w-full`}
    >
      <div
        className={`mt-2 mb-2 p-2 border border-gray-200 rounded-xl max-w-[70%] w-fit relative shadow-sm ${
          role === "User" ? "ml-auto bg-blue-200 items-end" : "mr-auto items-start"
        }`}
      >
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
};

ChatMessage.propTypes = {
  role: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
};

export default ChatMessage;
