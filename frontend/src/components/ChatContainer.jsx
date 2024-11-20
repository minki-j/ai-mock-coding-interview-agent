import { useRef, useState } from "react";
import PropTypes from 'prop-types';
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer as ChatUI,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";
import VoiceInput from './VoiceInput';

const ChatContainer = ({ messages, onSendMessage }) => {
  const messageListRef = useRef(null);
  const [inputValue, setInputValue] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const fullTranscriptRef = useRef('');
  const interimTranscriptRef = useRef('');

  const handleTranscriptionComplete = (transcript, isFinal) => {
    console.log('Transcription received:', { transcript, isFinal }); // Debug log
    
    if (isFinal) {
      // Add to full transcript and clear interim
      fullTranscriptRef.current += ' ' + transcript;
      interimTranscriptRef.current = '';
      setInputValue(fullTranscriptRef.current.trim());
    } else {
      // Update interim transcript
      interimTranscriptRef.current = transcript;
      // Combine full transcript with interim
      setInputValue((fullTranscriptRef.current + ' ' + interimTranscriptRef.current).trim());
    }
  };

  const handleStartRecording = () => {
    console.log('Starting recording'); // Debug log
    setIsRecording(true);
    fullTranscriptRef.current = '';
    interimTranscriptRef.current = '';
    setInputValue('');
  };

  const handleStopRecording = () => {
    console.log('Stopping recording'); // Debug log
    setIsRecording(false);
    interimTranscriptRef.current = '';
  };

  // Add helper function to strip HTML tags
  const stripHtmlTags = (html) => {
    const tmp = document.createElement('div');
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || '';
  };

  // Wrap onSendMessage to clean the input
  const handleSendMessage = (message) => {
    const cleanMessage = stripHtmlTags(message);
    onSendMessage(cleanMessage);
  };

  return (
    <MainContainer className="flex flex-col h-full">
      <VoiceInput 
        onTranscriptionComplete={handleTranscriptionComplete}
        onStart={handleStartRecording}
        onStop={handleStopRecording}
        isRecording={isRecording}
      />
      <ChatUI className="flex flex-col flex-1 min-h-0">
        <MessageList
          ref={messageListRef}
          className="flex-1 overflow-y-auto"
        >
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
          onChange={val => setInputValue(val)}
          placeholder="Type message here"
          onSend={(val) => {
            onSendMessage(val);
            setInputValue('');
            fullTranscriptRef.current = '';
            setIsRecording(false);
          }}
          attachButton={false}
        />
      </ChatUI>
    </MainContainer>
  );
};

ChatContainer.propTypes = {
  messages: PropTypes.arrayOf(PropTypes.shape({
    sender: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired
  })).isRequired,
  onSendMessage: PropTypes.func.isRequired
};

export default ChatContainer;
