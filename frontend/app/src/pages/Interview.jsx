import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import PythonEditor from "../components/PythonEditor";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import ChatContainer from "../components/ChatContainer";

const initialMessages = [
  {
    message:
      "Hello! I'll be your interviewer today. Let's work through a coding problem together.",
    sentTime: "just now",
    sender: "Interviewer",
  },
  {
    message:
      "Here's your coding question: Write a function that finds the longest substring without repeating characters in a given string.",
    sentTime: "just now",
    sender: "Interviewer",
  },
  {
    message:
      "Take your time to understand the problem. Let me know if you have any questions!",
    sentTime: "just now",
    sender: "Interviewer",
  },
];

import messageSound from "../assets/sounds/message-pop-alert.mp3";

// Define mock messages outside the Interview component
const mockResponses = [
  "That's an interesting approach!",
  "Can you explain your thought process?",
  "What would you do differently?",
  "Let's break this down step by step.",
  "Have you considered edge cases?",
];

const Interview = () => {
  const { id } = useParams();
  const [messages, setMessages] = useState(initialMessages);
  const [code, setCode] = useState(
    `def function(name):\n  print(name)\n\nfunction("hello world")`
  );
  const [testResults, setTestResults] = useState("");

  const executeCode = async () => {
    setTestResults("Running code...");
    try {
      const response = await fetch("/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
          code: code,
          timeout: 5000
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setTestResults(data.output || data.error || "No output");
      } else {
        const errorData = await response.json();
        setTestResults(`Error: ${errorData.detail || "Failed to execute code"}`);
      }
    } catch (error) {
      setTestResults(`Error: ${error.message}`);
    }
  };

  useEffect(() => {
    // TODO: Fetch initial state from backend
  }, [id]);

  const handleSendMessage = async (message) => {
    // Add user message to chat
    const userMessage = {
      message: message,
      sentTime: "just now",
      sender: "User",
      direction: "outgoing",
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Simulate interviewer response with a random message
    const randomResponse =
      mockResponses[Math.floor(Math.random() * mockResponses.length)];

    // Add interviewer response to chat
    const interviewerMessage = {
      message: randomResponse,
      sentTime: "just now",
      sender: "Interviewer",
      direction: "incoming",
    };

    // Use a timeout to ensure the sound plays after the message is added
    setTimeout(() => {
      setMessages((prevMessages) => [...prevMessages, interviewerMessage]);
      const audio = new Audio(messageSound);
      audio.play(); // Play sound when interviewer responds
    }, 100); // Delay to allow for the message to be rendered before playing sound
  };

  const handleFinalSolutionSubmit = async (e) => {
    e.preventDefault();
    // Here you can handle the code submission logic
    console.log("Code submitted:", code);
    // You can also send the code to a backend or evaluate it
  };

  return (
    <div className="container h-[calc(100vh-120px)] max-w-full">
      <div className="grid grid-cols-2 gap-2.5 h-full">
        {/* Chat UI Kit Section */}
        <div className="col-span-1 flex flex-col">
          <ChatContainer
            messages={messages}
            onSendMessage={handleSendMessage}
          />
        </div>
        {/* Code Editor Section */}
        <div className="col-span-1 flex flex-col gap-2.5 h-full">
          <div className="rounded bg-white shadow-md p-5 flex-1">
            <PythonEditor
              code={code}
              setCode={setCode}
              testResult={testResults}
              executeCode={executeCode}
            />
          </div>
          <div className="flex gap-2.5 w-full">
            <button
              className="flex-1 px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-800"
              onClick={handleFinalSolutionSubmit}
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Interview;
