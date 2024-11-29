import { useRef, useContext } from "react";
import { useParams } from "react-router-dom";
import PropTypes from "prop-types";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer as ChatUI,
  MessageList,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

import ChatMessage from "./ChatMessage";

import { StageContext } from "../context/StageContext";

const stageIntroductionMessages = {
  coding:
    "Welcome to the coding stage! Let's get started. Start coding your solution using the code editor on the right.",
  debugging:
    "Welcome to the debugging stage! Let's get started. Read your solution carefully and identify if there are any edge cases that you might have missed.",
  algorithmic_analysis:
    "Welcome to the algorithmic analysis stage! Let's get started. Please explain time and space complexity of your solution.",
};

const ChatContainer = ({ messages, setMessages, onSendMessage }) => {
  const { id } = useParams();
  const messageListRef = useRef(null);
  const {
    setDidUserConfirm,
    setCurrentStep,
    currentStep,
    nextStep,
    showUserConfirmation,
    setShowUserConfirmation,
  } = useContext(StageContext);

  // Add helper function to strip HTML tags
  const stripHtmlTags = (html) => {
    const tmp = document.createElement("div");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
  };

  // Wrap onSendMessage to clean the input
  const handleSendMessage = (message) => {
    const cleanMessage = stripHtmlTags(message);
    onSendMessage(cleanMessage);
  };

  const handleResponse = async (accepted) => {
    if (accepted) {
      setCurrentStep(nextStep);
      setDidUserConfirm(true);
      setShowUserConfirmation(false);

      const stageIntroductionMessage = stageIntroductionMessages[nextStep];

      console.log(
        "======= stageIntroductionMessage =======\n",
        stageIntroductionMessage
      );
      console.log("======= nextStep =======\n", nextStep);

      try {
        fetch("/chat_stage_introduction", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            interview_id: id,
            stage_introduction_message: stageIntroductionMessage,
          }),
        }).then((res) => {
          if (res.ok) {
            console.log("added stage introduction message to messages");
            setMessages((prevMessages) => [
              ...prevMessages,
              {
                message: stageIntroductionMessage,
                sentTime: new Date().toISOString(),
                sender: "AI",
              },
            ]);
          } else {
            console.error("Failed to revert stage");
          }
        });
      } catch (error) {
        console.error("Error reverting stage:", error);
      }
    } else {
      try {
        fetch("/revert_stage", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            interview_id: id,
          }),
        }).then((res) => {
          if (res.ok) {
            console.log("Stage reverted");
            setDidUserConfirm(true);
            setShowUserConfirmation(false);
          } else {
            console.error("Failed to revert stage");
          }
        });
      } catch (error) {
        console.error("Error reverting stage:", error);
      }
    }
  };

  return (
    <MainContainer className="flex flex-col h-full">
      <ChatUI className="flex flex-col flex-1 min-h-0">
        <MessageList
          ref={messageListRef}
          className="flex-1 overflow-y-auto"
          style={{}}
        >
          {messages.map((msg, index) => (
            <ChatMessage key={index} role={msg.sender} content={msg.message} />
          ))}
          {showUserConfirmation && (
            <div className="mt-0 mb-3 p-2 border border-gray-200 rounded-xl w-fit relative shadow-md">
              <p>
                I think you&apos;re ready to move to the next stage. Shall we
                proceed?
              </p>
              <div className={`flex gap-2 mt-2 justify-start`}>
                <button
                  onClick={() => handleResponse(true)}
                  className="px-2 py-1 bg-blue-400 text-white rounded hover:bg-blue-500 text-sm"
                >
                  Yes, continue
                </button>
                <button
                  onClick={() => handleResponse(false)}
                  className="px-2 py-1 border border-gray-200 text-gray-500 rounded hover:bg-gray-100 text-sm"
                >
                  No, not yet
                </button>
              </div>
            </div>
          )}
        </MessageList>
        <MessageInput
          placeholder="Type message here"
          onSend={handleSendMessage}
          attachButton={false}
        />
      </ChatUI>
    </MainContainer>
  );
};

ChatContainer.propTypes = {
  messages: PropTypes.arrayOf(
    PropTypes.shape({
      sender: PropTypes.string.isRequired,
      message: PropTypes.string.isRequired,
    })
  ).isRequired,
  setMessages: PropTypes.func.isRequired,
  onSendMessage: PropTypes.func.isRequired,
};

export default ChatContainer;
