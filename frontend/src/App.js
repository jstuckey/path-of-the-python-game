import './App.css';
import React, { useState, useRef, useEffect } from 'react';

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const [gameId, setGameId] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]); 
  const textareaRef = useRef(null);

  const handleNewGame = async () => {
    const response = await fetch(`${backendUrl}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await response.json();
    setGameId(data.game_id)
    setMessages([{ id: data.turn_id, role: 'game', text: data.reply }])
  }

  const handleSubmitPrompt = async (e) => {
    e.preventDefault();
    if (!prompt) return;

    const turnId = Date.now().toString();
    var newMessage = { id: turnId, role: 'player', text: prompt }
    setMessages((currentMessages) => [...currentMessages, newMessage]);

    const response = await fetch(`${backendUrl}/games/${gameId}/turn?prompt=${prompt}`, { method: 'POST' });
    const data = await response.json();

    newMessage = { id: data.turn_id, role: 'game', text: data.reply }
    setMessages((currentMessages) => [...currentMessages, newMessage]);
    setPrompt("");

    textareaRef.current?.focus();
  }

  useEffect(() => {
    if (!gameId) return;

    requestAnimationFrame(() => {
      textareaRef.current?.focus();
    });
  }, [gameId]);

  return (
    <div className="App">
      <h1>Path of the Python</h1>
      <div className="header-controls">
        <button onClick={handleNewGame} tabIndex={0}>New Game</button>
      </div>
      {gameId && (
        <div id="game">
          <div id="messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.role}`}>
                <div className="role-label">
                  <i>{msg.role === 'player' ? 'Player' : 'Mysterious Narrator'}</i>
                </div>
                {msg.text}
              </div>
            ))}
          </div>
          <form onSubmit={handleSubmitPrompt}>
            <textarea
              ref={textareaRef}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="What would you like to do?"
            ></textarea>
            <button type="submit" tabIndex={0}>Submit</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
