import PropTypes from 'prop-types';

const ChatMessage = ({ role, content }) => {
  const alignment = role === 'AI' ? 'flex-start' : 'flex-end';

  return (
    <div style={{ display: 'flex', justifyContent: alignment }}>
      <div style={{
        marginBottom: '1em',
        padding: '1em',
        border: '0.5px solid var(--pico-border-color)',
        borderRadius: '24px',
        maxWidth: '70%',
        position: 'relative',
        boxShadow: '0 0 10px rgba(0,0,0,0.1)'
      }}>
        <div style={{ fontSize: '0.9em', letterSpacing: '0.05em' }}>
          <strong>{role}</strong>
        </div>
        <div style={{ marginTop: '0.5em' }}>
          <p>{content}</p>
        </div>
      </div>
    </div>
  );
};

ChatMessage.propTypes = {
  role: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired
};

export default ChatMessage;
