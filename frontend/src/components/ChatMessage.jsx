import PropTypes from "prop-types";
import ReactMarkdown from 'react-markdown';

const ChatMessage = ({ role, content}) => {
  return (
    <div
      className={`flex flex-col w-full`}
    >
      <div
        className={`${
          role === "display_decision" 
            ? "mt-0.5 mb-0.5 flex items-center gap-2 w-full"
            : `mt-2 mb-2 p-2 border border-gray-200 rounded-xl max-w-[70%] w-fit relative shadow-sm ${
                role === "User" ? "ml-auto bg-blue-200 items-end" : "mr-auto items-start"
              }`
        }`}
      >
        {role === "display_decision" && (
          <>
            <div className="flex items-center gap-2 text-gray-500">
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                width="16" 
                height="16" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              >
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
              <div className="text-sm">{content}</div>
            </div>
          </>
        )}
        {role !== "display_decision" && (
          <ReactMarkdown
            components={{
              p: ({children, ...props}) => (
                <p className="mb-2 last:mb-0" {...props}>{children}</p>
              ),
              ol: ({children, ...props}) => (
                <ol className="mb-2 last:mb-0 list-decimal pl-4" {...props}>{children}</ol>
              ),
              ul: ({children, ...props}) => (
                <ul className="mb-2 last:mb-0 list-disc pl-4" {...props}>{children}</ul>
              ),
              h1: ({children, ...props}) => (
                <h1 className="text-2xl font-bold mb-2 last:mb-0" {...props}>{children}</h1>
              ),
              h2: ({children, ...props}) => (
                <h2 className="text-xl font-bold mb-3 last:mb-0" {...props}>{children}</h2>
              ),
              h3: ({children, ...props}) => (
                <h3 className="text-lg font-bold mb-2 last:mb-0" {...props}>{children}</h3>
              ),
              blockquote: ({children, ...props}) => (
                <blockquote className="border-l-4 border-gray-300 pl-4 mb-2 last:mb-0" {...props}>{children}</blockquote>
              ),
              code: ({children, ...props}) => (
                <code className="bg-gray-100 rounded px-1 py-0.5" {...props}>{children}</code>
              ),
              pre: ({children, ...props}) => (
                <pre className="bg-gray-100 rounded p-3 mb-2 last:mb-0 overflow-x-auto" {...props}>{children}</pre>
              )
            }}
          >
            {content}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
};

ChatMessage.propTypes = {
  role: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
};

export default ChatMessage;
