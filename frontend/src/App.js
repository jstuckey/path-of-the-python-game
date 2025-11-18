import './App.css';
import React, { useState, useEffect } from 'react';
import GameNavigation from './GameNavigation';
import SavedGames from './SavedGames';
import Messages from './Messages';
import PromptInput from './PromptInput';

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const [gameId, setGameId] = useState(null);
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

  const handlePromptSubmit = async (promptText) => {
    const playerTurnId = Date.now().toString();
    const playerMessage = { id: playerTurnId, role: 'player', text: promptText };
    setMessages((currentMessages) => [...currentMessages, playerMessage]);

    const waitingMessage = { id: 'waiting', role: 'waiting', text: '...' };
    setMessages((currentMessages) => [...currentMessages, waitingMessage]);

    setIsSubmitting(true);

    const response = await fetch(`${backendUrl}/games/${gameId}/turn?prompt=${promptText}`, { method: 'POST' });
    const data = await response.json();

    const gameMessage = { id: data.turn_id, role: 'game', text: data.reply };
    setMessages((currentMessages) => [...currentMessages.slice(0, -1), gameMessage]);

    setIsSubmitting(false);
  };

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
      {!gameId && (
        <GameNavigation
          gameId={gameId}
          onNewGame={handleNewGame}
          onResumeGame={handleResumeGame}
          onShowSavedGames={handleShowSavedGames}
        />
      )}
      {showSavedGames && (
        <SavedGames
          savedGames={savedGames}
          onSavedGameClicked={handleLoadSavedGame}
        />
      )}
      {gameId && (
        <div id="game">
          <Messages messages={messages} />
          <PromptInput
            gameId={gameId}
            onSubmit={handlePromptSubmit}
            isSubmitting={isSubmitting}
          />
        </div>
      )}
    </div>
  );
}

export default App;
