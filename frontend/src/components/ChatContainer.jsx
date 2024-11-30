import { useRef, useState, useEffect } from "react";
import PropTypes from "prop-types";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer as ChatUI,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

const ChatContainer = ({ messages, onSendMessage }) => {
  const [inputValue, setInputValue] = useState("");
  const [isRecording, setIsRecording] = useState(false);

  const messageListRef = useRef(null);

  const fullTranscriptRef = useRef("");
  const interimTranscriptRef = useRef("");

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
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = 0; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + " ";
        } else {
          interimTranscript += transcript;
        }
      }

      if (finalTranscript) {
        handleTranscriptionComplete(finalTranscript.trim(), true);
      }
      if (interimTranscript) {
        handleTranscriptionComplete(interimTranscript.trim(), false);
      }
    };

    recognition.onend = () => {
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
      toggleRecording();
    };

    // Cleanup on component unmount
    return () => {
      recognition.abort();
    };
  }, []); // Empty dependency array - only run once on mount

  if (!("webkitSpeechRecognition" in window)) {
    return null;
  }

  const handleTranscriptionComplete = (transcript, isFinal) => {
    if (isFinal) {
      // Add to full transcript and clear interim
      fullTranscriptRef.current += " " + transcript;
      interimTranscriptRef.current = "";
      setInputValue(fullTranscriptRef.current.trim());
    } else {
      // Update interim transcript
      interimTranscriptRef.current = transcript;
      // Combine full transcript with interim
      setInputValue(
        (fullTranscriptRef.current + " " + interimTranscriptRef.current).trim()
      );
    }
  };

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
      interimTranscriptRef.current = "";
    } else {
      console.log("Start recording");
      setIsRecording(true);
      toggleRecordingStyle();
      fullTranscriptRef.current = "";
      interimTranscriptRef.current = "";
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

  return (
    <MainContainer className="flex flex-col h-full">
      <ChatUI className="flex flex-col flex-1 min-h-0">
        <MessageList ref={messageListRef} className="flex-1 overflow-y-auto">
          {messages.map((msg, index) => (
            <Message
              key={index}
              model={{
                message: msg.message,
                direction: msg.sender === "User" ? "outgoing" : "incoming",
                position: "single",
              }}
            />
          ))}
        </MessageList>
        <MessageInput
          value={inputValue}
          onChange={(val) => setInputValue(val)}
          placeholder="Type message here"
          onSend={(val) => {
            const cleanMessage = stripHtmlTags(val);
            onSendMessage(cleanMessage);
            setInputValue("");
            fullTranscriptRef.current = "";
            setIsRecording(false);
          }}
          attachButton={true}
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
  onSendMessage: PropTypes.func.isRequired,
};

export default ChatContainer;
