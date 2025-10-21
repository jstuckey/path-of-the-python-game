import './App.css';
import React, { useState, useRef, useEffect } from 'react';

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const [gameId, setGameId] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]); 
  const [isSubmitting, setIsSubmitting] = useState(false);
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

    const playerTurnId = Date.now().toString();
    const playerPrompt = prompt; 
    const playerMessage = { id: playerTurnId, role: 'player', text: playerPrompt };
    setMessages((currentMessages) => [...currentMessages, playerMessage]);

    setIsSubmitting(true);
    setPrompt("");

    const response = await fetch(`${backendUrl}/games/${gameId}/turn?prompt=${playerPrompt}`, { method: 'POST' });
    const data = await response.json();

    const gameMessage = { id: data.turn_id, role: 'game', text: data.reply };
    setMessages((currentMessages) => [...currentMessages, gameMessage]);

    setIsSubmitting(false);
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
            <button type="submit" tabIndex={0} disabled={isSubmitting || !prompt}>Submit</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
