import { useRef, useState, useEffect, useContext } from "react";
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
  assessment:
    "Well done! You've completed the interview. Now, I'll analyze our conversation and your solution. Please wait for a moment ☺️",
};

const ChatContainer = ({
  messages,
  setMessages,
  onSendMessage,
  handleSendMessage,
}) => {
  const [inputValue, setInputValue] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDisabled, setRecordingDisabled] = useState(false);
  const { id } = useParams();
  const messageListRef = useRef(null);
  const {
    setDidUserConfirm,
    setCurrentStep,
    nextStep,
    showUserConfirmation,
    setShowUserConfirmation,
  } = useContext(StageContext);

  const fullTranscriptRef = useRef("");

  const recognitionRef = useRef(null);

  useEffect(() => {
    if (!("webkitSpeechRecognition" in window)) {
      console.error("Speech recognition is not supported in this browser");
      return;
    }

    recognitionRef.current = new window.webkitSpeechRecognition();
    const recognition = recognitionRef.current;

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onstart = () => {};

    recognition.onresult = (event) => {
      let interimTranscription = "";
      for (let i = 0; i < event.results.length; i++) {
        if (event.results[i].isFinal && i != event.results.length - 1) {
          continue;
        }

        if (event.results[i].isFinal && i === event.results.length - 1) {
          fullTranscriptRef.current += " " + event.results[i][0].transcript;
          setInputValue(fullTranscriptRef.current.trim());
        }

        if (!event.results[i].isFinal) {
          interimTranscription += " " + event.results[i][0].transcript;
          setInputValue(
            (fullTranscriptRef.current + " " + interimTranscription).trim()
          );
        }

        if (!event.results[i].isFinal && i === event.results.length - 1) {
          setInputValue(
            (fullTranscriptRef.current + " " + interimTranscription).trim()
          );
        }
      }
    };

    recognition.onend = () => {
      console.log("onend");

      // Only restart if we're still supposed to be listening
      if (isRecording) {
        console.log("Restarting recognition");
        try {
          recognition.start();
        } catch (error) {
          console.error("Error restarting recognition:", error);
        }
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      console.log("Stop recording");
      setIsRecording(false);
      try {
        recognitionRef.current.stop();
      } catch (error) {
        console.error("Error stopping recognition:", error);
      }
      toggleRecordingStyle();
      if (event.error === "network") {
        setInputValue(
          "Sorry, this browser does not support speech recognition. Please use the latest Chrome or Safari."
        );
        setRecordingDisabled(true);
      }
    };

    // Cleanup on component unmount
    return () => {
      recognition.abort();
    };
  }, []); // Empty dependency array - only run once on mount

  if (!("webkitSpeechRecognition" in window)) {
    console.log("Speech recognition is not supported in this browser");
    setRecordingDisabled(true);
  }

  const toggleRecording = () => {
    if (isRecording) {
      console.log("Stop recording");
      setIsRecording(false);
      try {
        recognitionRef.current.stop();
      } catch (error) {
        console.error("Error stopping recognition:", error);
      }
      toggleRecordingStyle();
    } else {
      console.log("Start recording");
      setIsRecording(true);
      toggleRecordingStyle();
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error("Error starting recognition:", error);
      }
    }
  };

  const toggleRecordingStyle = () => {
    const attachmentButton = document.querySelector(".cs-button--attachment");
    if (attachmentButton) {
      attachmentButton.classList.toggle("recording");
    }
  };

  const stripHtmlTags = (html) => {
    const tmp = document.createElement("div");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
  };

  const handleResponse = async (accepted) => {
    if (accepted) {
      const stageIntroductionMessage = stageIntroductionMessages[nextStep];

      try {
        const res = await fetch("/chat_stage_introduction", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            interview_id: id,
            stage: nextStep,
            stage_introduction_message: stageIntroductionMessage,
          }),
        });

        if (res.ok) {
          setCurrentStep(nextStep);
          setDidUserConfirm(true);
          setShowUserConfirmation(false);

          // Add 1 second delay before updating messages
          setTimeout(() => {
            setMessages((prevMessages) => [
              ...prevMessages,
              {
                message: stageIntroductionMessage,
                sentTime: new Date().toISOString(),
                sender: "AI",
              },
            ]);
          }, 1500);

          if (nextStep === "assessment") {
            handleSendMessage("");
          }
          
        } else {
          console.error("Failed to revert stage");
        }
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

  const handlePaste = (e) => {
    e.preventDefault();
    const text = e.clipboardData.getData("text/plain");
    setInputValue(text);
  };

  return (
    <MainContainer className="flex flex-col h-full">
      <ChatUI className="flex flex-col flex-1 min-h-0">
        <MessageList ref={messageListRef} className="flex-1 overflow-y-auto">
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
          value={inputValue}
          onChange={(val) => setInputValue(val)}
          placeholder="Type message here"
          onPaste={handlePaste}
          onSend={(val) => {
            const cleanMessage = stripHtmlTags(val);
            onSendMessage(cleanMessage);
            if (isRecording) {
              try {
                recognitionRef.current.stop();
                setIsRecording(false);
                toggleRecordingStyle();
                fullTranscriptRef.current = "";
              } catch (error) {
                console.error("Error stopping recognition:", error);
              }
            }
            setInputValue("");
          }}
          sendButton={true}
          sendDisabled={false}
          attachButton={!recordingDisabled}
          onAttachClick={toggleRecording}
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
