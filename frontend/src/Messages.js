import React, { useRef, useEffect } from 'react';
import './Messages.css';

function Messages({ messages }) {
  const messagesRef = useRef(null);

  const lastMessageId = messages.at(-1)?.id;

  useEffect(() => {
    const el = messagesRef.current;
    if (!el) return;

    el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
  }, [lastMessageId]);

  return (
    <div className="messages" ref={messagesRef}>
      {messages.map((msg) => (
        <div key={msg.id} className={`message ${msg.role}`}>
          <div className="role-label">
            <i>{msg.role === 'player' ? 'Player' : 'Mysterious Narrator'}</i>
          </div>
          {msg.text}
        </div>
      ))}
    </div>
  );
}

export default Messages;
