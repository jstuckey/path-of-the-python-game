import './App.css';
import React, { useState, useRef, useEffect } from 'react';

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const [gameId, setGameId] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]); 
  const [isSubmitting, setIsSubmitting] = useState(false);

  const newGameButtonRef = useRef(null);
  const inputRef = useRef(null);

  const handleNewGame = async () => {
    setGameId('waiting')
    setMessages([{ id: 'waiting', role: 'waiting', text: '...' }])
    setIsSubmitting(true);

    const response = await fetch(`${backendUrl}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await response.json();
    setGameId(data.game_id)
    setMessages([{ id: data.turn_id, role: 'game', text: data.reply }])
    setIsSubmitting(false);
  }

  const handleSubmitPrompt = async (e) => {
    e.preventDefault();
    if (!prompt) return;

    const playerTurnId = Date.now().toString();
    const playerPrompt = prompt; 
    const playerMessage = { id: playerTurnId, role: 'player', text: playerPrompt };
    setMessages((currentMessages) => [...currentMessages, playerMessage]);

    const waitingMessage = { id: 'waiting', role: 'waiting', text: '...' };
    setMessages((currentMessages) => [...currentMessages, waitingMessage]);

    setIsSubmitting(true);
    setPrompt("");

    const response = await fetch(`${backendUrl}/games/${gameId}/turn?prompt=${playerPrompt}`, { method: 'POST' });
    const data = await response.json();

    const gameMessage = { id: data.turn_id, role: 'game', text: data.reply };
    setMessages((currentMessages) => [...currentMessages.slice(0, -1), gameMessage]);

    setIsSubmitting(false);
    inputRef.current?.focus();
  }

  useEffect(() => {
    if (gameId) return;

    requestAnimationFrame(() => {
      newGameButtonRef.current?.focus();
    });
  });

  useEffect(() => {
    if (!gameId) return;

    requestAnimationFrame(() => {
      inputRef.current?.focus();
    });
  }, [gameId]);

  return (
    <div className="App">
      <h1>Path of the Python</h1>
      <div className="header-controls">
        <button 
          ref={newGameButtonRef}
          onClick={handleNewGame} 
          tabIndex={0}
        >New Game</button>
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
            <input
              ref={inputRef}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="What would you like to do?"
              type="text"
            />
            <button type="submit" tabIndex={0} disabled={isSubmitting || !prompt}>Submit</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
