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

  return (
    <MainContainer className="flex-1 px-4 py-2 bg-gray-700 shadow-md text-white rounded">
      <ChatUI className="flex-1">
        <MessageList 
          ref={messageListRef} 
          style={{ maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}
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
          onSend={onSendMessage}
          attachButton={false}
        />
      </ChatUI>
    </MainContainer>
  );
};

ChatContainer.propTypes = {
  messages: PropTypes.arrayOf(PropTypes.shape({
    sender: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired
  })).isRequired,
  onSendMessage: PropTypes.func.isRequired
};

export default ChatContainer;
