import React, { useRef, useEffect } from 'react';
import './HeaderControls.css';

function HeaderControls({
  gameId,
  onNewGame,
  onResumeGame,
  onShowSavedGames
}) {
  const newGameButtonRef = useRef(null);

  useEffect(() => {
    if (gameId) return;

    requestAnimationFrame(() => {
      newGameButtonRef.current?.focus();
    });
  });

  if (gameId) return null;

  return (
    <div className="header-controls">
      <button
        ref={newGameButtonRef}
        onClick={onNewGame}
        tabIndex={0}
      >
        New Game
      </button>

      {localStorage.getItem('gameId') && (
        <button
          onClick={onResumeGame}
          tabIndex={0}
        >
          Resume Game
        </button>
      )}

      {localStorage.getItem('savedGames') && (
        <button
          onClick={onShowSavedGames}
          tabIndex={0}
        >
          Load Game
        </button>
      )}
    </div>
  );
}

export default HeaderControls;
