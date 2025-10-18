import './App.css';
import React, { useState } from 'react';

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const [gameData, setGameData] = useState(null);

  const handleNewGame = async () => {
    const response = await fetch(`${backendUrl}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    const data = await response.json();
    console.log(data)
    setGameData(data)
  }


  return (
    <div className="App">
      <h1>Path of the Python</h1>
      <button onClick={handleNewGame}>New Game</button>
      {gameData && (
        <div id="game">
          <p>{gameData.reply}</p>
          <textarea placeholder="What would you like to do?"></textarea>
        </div>
      )}
    </div>
  );
}

export default App;
