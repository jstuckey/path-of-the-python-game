import './App.css';
import React, { useState, useRef, useEffect } from 'react';
import SavedGames from './SavedGames';
import GameNavigation from './GameNavigation';

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const [gameId, setGameId] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [savedGames, setSavedGames] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('savedGames') || '[]');
    } catch {
      return []
    }
  });
  const [showSavedGames, setShowSavedGames] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const messagesRef = useRef(null);
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
    setGameId(data.id)
    setMessages([{ id: data.turn_id, role: 'game', text: data.reply }])

    setSavedGames((currentSavedGames) => {
      const newSavedGames = [
        {
          id: data.id,
          date: new Date()
        },
        ...currentSavedGames,
      ];
      return newSavedGames;
    });

    setIsSubmitting(false);
  }

  const handleResumeGame = async () => {
    setGameId(localStorage.getItem('gameId'));
    setMessages(JSON.parse(localStorage.getItem('messages')) || []);
  }

  const handleShowSavedGames = async () => {
    setSavedGames(JSON.parse(localStorage.getItem('savedGames')) || []);
    setShowSavedGames(true);
  }

  const handleLoadSavedGame = async (savedGameId) => {
    setGameId('waiting')
    setMessages([{ id: 'waiting', role: 'waiting', text: '...' }])
    setIsSubmitting(true);

    const response = await fetch(`${backendUrl}/games/${savedGameId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await response.json();

    setGameId(savedGameId)
    setMessages(data.messages);
    setIsSubmitting(false);
    setShowSavedGames(false);
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
    if (!gameId) return;

    requestAnimationFrame(() => {
      inputRef.current?.focus();
    });

    setShowSavedGames(false);
  }, [gameId]);

  const lastMessageId = messages.at(-1)?.id;

  useEffect(() => {
    const el = messagesRef.current;
    if (!el) return;

    el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
  }, [lastMessageId]);

  useEffect(() => {
    if (gameId && gameId !== 'waiting') {
      localStorage.setItem('gameId', gameId);
      localStorage.setItem('messages', JSON.stringify(messages));
    }
  }, [gameId, messages]);

  useEffect(() => {
    localStorage.setItem('savedGames', JSON.stringify(savedGames));
  }, [savedGames]);

  return (
    <div className="App">
      <a href="/"><h1>Path of the Python</h1></a>
      <GameNavigation
        gameId={gameId}
        onNewGame={handleNewGame}
        onResumeGame={handleResumeGame}
        onShowSavedGames={handleShowSavedGames}
      />
      {showSavedGames && (
        <SavedGames
          savedGames={savedGames}
          onSavedGameClicked={handleLoadSavedGame}
        />
      )}
      {gameId && (
        <div id="game">
          <div id="messages" ref={messagesRef}>
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
