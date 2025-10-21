import './App.css';
import React, { useState } from 'react';

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const [gameData, setGameData] = useState(null);
  const [prompt, setPrompt] = useState("");

  const handleNewGame = async () => {
    const response = await fetch(`${backendUrl}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })

    const data = await response.json();
    console.log(data)
    setGameData(data)
  }

  const handleSubmitPrompt = async (e) => {
    e.preventDefault();
    if (!prompt) return;

    const response = await fetch(`${backendUrl}/games/${gameData.game_id}/turn?prompt=${prompt}`, { method: 'POST' });

    const data = await response.json();
    setGameData(data);
    setPrompt("");
  }

  return (
    <div className="App">
      <h1>Path of the Python</h1>
      <div className="header-controls">
        <button onClick={handleNewGame} tabIndex={0}>New Game</button>
      </div>
      {gameData && (
        <div id="game">
          <p id="game-text" key={gameData.turn_id}>{gameData.reply}</p>
          <form onSubmit={handleSubmitPrompt}>
            <textarea
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
