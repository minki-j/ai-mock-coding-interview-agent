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
    console.log("fetching interview with id", id);
    const fetchInterview = async () => {
      try {
        const res = await fetch(`/get_interview/${id}`);
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json();
        setMessages(data.messages || initialMessages);
        setCode(data.code_editor_state || code);
        setTestResults(data.test_result || '');
      } catch (error) {
        console.error("Error fetching interview:", error);
        // Fallback to initial states if fetch fails
        setMessages(initialMessages);
      }
    };
    fetchInterview();
  }, []);

  const handleSendMessage = async (message) => {
    console.log("Sending message:", message);
    // Add user message to chat
    const userMessage = {
      message: message,
      sentTime: new Date().toISOString(),
      sender: "User",
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(userMessage),
      });
      
      const responseData = await response.json(); // Parse the JSON response
      
      const interviewerMessage = {
        message: responseData.message,
        sentTime: responseData.sentTime,
        sender: responseData.sender,
      };

      // Use a timeout to ensure the sound plays after the message is added
      setTimeout(() => {
        setMessages((prevMessages) => [...prevMessages, interviewerMessage]);
        const audio = new Audio(messageSound);
        audio.play(); // Play sound when interviewer responds
      }, 100);
    } catch (error) {
      console.error("Error handling chat response:", error);
      // Optionally handle the error in the UI
    }
  };

  const handleFinalSolutionSubmit = async (e) => {
    e.preventDefault();
    console.log("Code submitted:", code);
    // Here you can handle the code submission logic
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
        <div className="col-span-1 flex flex-col gap-2.5 h-full">
          {/* Code Editor Section */}
          <div className="rounded bg-white shadow-md p-5 flex-1">
            <PythonEditor
              code={code}
              setCode={setCode}
              testResult={testResults}
              executeCode={executeCode}
            />
          </div>
          {/* Submit Button Section */}
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
