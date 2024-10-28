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
    <div
      className="container"
      style={{
        height: "calc(100vh - 120px)",
        maxWidth: "100%",
      }}
    >
      <div
        className="interview-grid"
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "10px",
          height: "100%",
        }}
      >
        {/* Chat Section */}
        <div
          className="chat-container"
          style={{
            borderRadius: "3px",
            padding: "20px",
            boxShadow: "0 0 10px rgba(0,0,0,0.1)",
            backgroundColor: "var(--pico-card-background-color)",
            height: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <h3 style={{ flex: "0 0 auto", marginBottom: "10px" }}>Chat</h3>
          <div
            id="chat-messages"
            style={{
              flex: 1,
              overflowY: "auto",
              marginBottom: "10px",
            }}
          >
            {messages.map((msg, index) => (
              <ChatMessage key={index} role={msg[0]} content={msg[1]} />
            ))}
          </div>
          <form
            onSubmit={handleSendMessage}
            style={{
              flex: "0 0 auto",
              display: "flex",
              gap: "10px",
            }}
          >
            <input
              type="text"
              name="message"
              style={{ marginBottom: 0, flex: 1 }}
            />
            <button type="submit">Send</button>
          </form>
        </div>

        {/* Code Editor Section */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "10px",
            height: "100%",
          }}
        >
          <div
            style={{
              borderRadius: "3px",
              padding: "20px",
              boxShadow: "0 0 10px rgba(0,0,0,0.1)",
              backgroundColor: "var(--pico-card-background-color)",
              height: "100%",
            }}
          >
            <h3>Code Editor</h3>
            <PythonEditor />
          </div>
          <div style={{ display: "flex", gap: "10px", width: "100%" }}>
            <button
              className="contrast"
              style={{ flex: 1, width: "calc(50% - 5px)" }}
              onClick={handleSubmit}
            >
              Submit
            </button>
          </div>
        </div>
      </div>
      <style>
        {`
          @media (max-width: 1024px) {
            .interview-grid {
              grid-template-columns: 1fr !important;
              height: auto !important;
            }
            .chat-container {
              height: 50vh !important;
            }
          }
        `}
      </style>
    </div>
  );
};

export default Interview;
