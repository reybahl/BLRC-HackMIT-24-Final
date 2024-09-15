import React, { useState, useRef, useEffect } from 'react';
import { Send, X, MessageCircle } from 'lucide-react';

const ChatBox = ({ croppedImage }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const boxStyle = {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    border: 'none',
    backgroundColor: isExpanded ? '#f9f9f9' : 'transparent',
    borderRadius: '20px',
    boxShadow: isExpanded ? '0 8px 30px rgba(0, 0, 0, 0.15)' : 'none',
    width: isExpanded ? '400px' : '60px',
    height: isExpanded ? '650px' : '60px',
    transition: 'all 0.3s ease-in-out',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  const headerStyle = {
    padding: '10px',
    backgroundColor: '#0052CC',
    color: '#fff',
    borderTopLeftRadius: '20px',
    borderTopRightRadius: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  };

  const chatContentStyle = {
    flex: 1,
    padding: '20px',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    backgroundColor: '#f9f9f9',
    color: '#333',
  };

  const messageStyle = {
    backgroundColor: '#e6e6e6',
    padding: '10px 15px',
    borderRadius: '15px',
    maxWidth: '70%',
    alignSelf: 'flex-start',
    fontSize: '14px',
  };

  const botMessageStyle = {
    ...messageStyle,
    backgroundColor: '#D1E9FC',
    alignSelf: 'flex-end',
  };

  const inputContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    padding: '10px',
    borderTop: '1px solid #eee',
    backgroundColor: '#f9f9f9',
    margintop: '30px'
  };

  const inputStyle = {
    flex: 1,
    padding: '12px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    marginRight: '10px',
    outline: 'none',
    fontSize: '14px',
  };

  const sendButtonStyle = {
    backgroundColor: '#0052CC',
    border: 'none',
    borderRadius: '50%',
    padding: '10px',
    cursor: 'pointer',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'transform 0.2s ease',
  };

  const handleSendMessage = () => {
    if (inputMessage.trim() === '') return;

    const newMessage = { text: inputMessage, isUser: true };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    // Simulate bot response
    setTimeout(() => {
      const botResponse = { text: 'response', isUser: false };
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    }, 1000);

    setInputMessage('');
  };

  return (
    <div style={boxStyle}>
      {!isExpanded ? (
        <div onClick={() => setIsExpanded(true)} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1 }}>
          <MessageCircle size={28} style={{ color: '#0052CC' }} />
        </div>
      ) : (
        <>
          <div style={headerStyle}>
            <h3 style={{ margin: 0 }}>Chat</h3>
            <button onClick={() => setIsExpanded(false)} style={{ background: 'none', border: 'none', color: '#fff', cursor: 'pointer' }}>
              <X size={24} />
            </button>
          </div>
          <div>
		 	<h3 style={{ color: '#333' , margin: '0 20px' }}> octopus</h3>
			{croppedImage && (
				<div style={{ padding: '10px', textAlign: 'center' }}>
				<img
					src={croppedImage}
					alt="Cropped Thumbnail"
					style={{ width: '100%', borderRadius: '10px', marginBottom: '10px' }}
				/>
				</div>
			)}
            <p style={{ color: '#333' , margin: '0 20px' }}>
            Octopuses are intelligent marine creatures known for their adaptability and unique features. With eight flexible arms and the ability to 
            </p>
            <hr style={{ border: '1px solid #ddd', margin: '20px 0' }} />
            </div>
          <div style={chatContentStyle}>
            {messages.map((message, index) => (
              <div key={index} style={message.isUser ? messageStyle : botMessageStyle}>
                {message.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div style={inputContainerStyle}>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type a message..."
              style={inputStyle}
            />
            <button
              onClick={handleSendMessage}
              style={sendButtonStyle}
              onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.1)')}
              onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
            >
              <Send size={20} />
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatBox;