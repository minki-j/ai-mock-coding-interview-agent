import { useRef } from "react";
import PropTypes from 'prop-types';
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer as ChatUI,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

const ChatContainer = ({ messages, onSendMessage }) => {
  const messageListRef = useRef(null);

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
      <ChatUI className="flex flex-col flex-1 min-h-0">
        <MessageList
          ref={messageListRef}
          className="flex-1 overflow-y-auto"
          style={{}}
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
