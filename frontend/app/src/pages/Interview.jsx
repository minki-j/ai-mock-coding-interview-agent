import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import PythonEditor from "../components/PythonEditor";
import ChatMessage from "../components/ChatMessage";

const Interview = () => {
  const { id } = useParams();
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");

  useEffect(() => {
    // TODO: Fetch initial state from backend
    // This would replace the main_graph.get_state functionality
  }, [id]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const message = formData.get("message");

    // TODO: Implement chat functionality with backend
    // This would replace the hx_post="/chat" functionality

    e.target.reset();
  };

  const handleSubmit = async () => {
    // TODO: Implement submission functionality
  };

  return (
    <div className="container h-[calc(100vh-120px)] max-w-full">
      <div className="grid grid-cols-2 gap-2.5 h-full">
        {/* Chat Section */}
        <div className="rounded bg-white shadow-md p-5 h-full flex flex-col">
          <h3 className="flex-none mb-2.5">Chat</h3>
          <div className="flex-1 overflow-y-auto mb-2.5">
            {messages.map((msg, index) => (
              <ChatMessage key={index} role={msg[0]} content={msg[1]} />
            ))}
          </div>
          <form onSubmit={handleSendMessage} className="flex-none flex gap-2.5">
            <input
              type="text"
              name="message"
              className="flex-1 mb-0"
            />
            <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">Send</button>
          </form>
        </div>

        {/* Code Editor Section */}
        <div className="flex flex-col gap-2.5 h-full">
          <div className="rounded bg-white shadow-md p-5 h-full">
            <PythonEditor />
          </div>
          <div className="flex gap-2.5 w-full">
            <button
              className="flex-1 px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-800"
              onClick={handleSubmit}
            >
              Submit
            </button>
          </div>
        </div>
      </div>
      
      {/* Responsive styles */}
      <style>
        {`
          @media (max-width: 1024px) {
            .grid { grid-template-columns: 1fr !important; }
            .h-full { height: auto !important; }
            .chat-container { height: 50vh !important; }
          }
        `}
      </style>
    </div>
  );
};

export default Interview;
