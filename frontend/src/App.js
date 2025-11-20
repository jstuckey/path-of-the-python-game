import './App.css';
import React, { useState, useEffect } from 'react';
import GameNavigation from './GameNavigation';
import SavedGames from './SavedGames';
import Messages from './Messages';
import PromptInput from './PromptInput';
import useGame from './useGame';

function App() {
  const game = useGame();

  return (
    <div className="App">
      <a href="/"><h1>Path of the Python</h1></a>
      {!game.gameId && (
        <GameNavigation
          gameId={game.gameId}
          onNewGame={game.handleNewGame}
          onResumeGame={game.handleResumeGame}
          onShowSavedGames={game.handleShowSavedGames}
        />
      )}
      {game.showSavedGames && (
        <SavedGames
          savedGames={game.savedGames}
          onSavedGameClicked={game.handleLoadSavedGame}
        />
      )}
      {game.gameId && (
        <div id="game">
          <Messages messages={game.messages} />
          <PromptInput
            gameId={game.gameId}
            onSubmit={game.handlePromptSubmit}
            isSubmitting={game.isSubmitting}
          />
        </div>
      )}
    </div>
  );
}

export default App;
