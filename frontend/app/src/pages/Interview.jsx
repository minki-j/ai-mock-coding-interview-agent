import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import PythonEditor from "../components/PythonEditor";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

const initialMessages = [
  {
    message: "Hello! I'll be your interviewer today. Let's work through a coding problem together.",
    sentTime: "just now",
    sender: "Interviewer",
  },
  {
    message: "Here's your coding question: Write a function that finds the longest substring without repeating characters in a given string.",
    sentTime: "just now",
    sender: "Interviewer",
  },
  {
    message: "Take your time to understand the problem. Let me know if you have any questions!",
    sentTime: "just now",
    sender: "Interviewer",
  },
];

import messageSound from '../assets/sounds/message-pop-alert.mp3';

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
  const [code, setCode] = useState(`def function(name):\n  print(name)\n\nfunction("hello world")`); // Initial code for the editor
  const messageListRef = useRef(null);

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
    const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];

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

  const handleSubmit = async (e) => {
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
          <MainContainer className="flex-1 px-4 py-2 bg-gray-700 shadow-md text-white rounded">
            <ChatContainer className="flex-1">
              <MessageList 
                ref={messageListRef} 
                style={{ maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }} // Adjust height as needed
              >
                {messages.map((msg, index) => (
                  <Message
                    key={index}
                    model={{
                      ...msg,
                      direction: msg.sender === "User" ? "outgoing" : "incoming",
                      position: "single",
                    }}
                  />
                ))}
              </MessageList>
              <MessageInput
                placeholder="Type message here"
                onSend={handleSendMessage}
                attachButton={false}
              />
            </ChatContainer>
          </MainContainer>
        </div>

        {/* Code Editor Section */}
        <div className="col-span-1 flex flex-col gap-2.5 h-full">
          <div className="rounded bg-white shadow-md p-5 flex-1">
            <PythonEditor code={code} setCode={setCode} />
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