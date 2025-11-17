import React from 'react';
import './SavedGames.css';

function SavedGames({ savedGames, onSavedGameClicked }) {
  return (
    <div className="saved-games">
      <ul>
        {savedGames.map((game) => (
          <li key={game.id}>
            <p onClick={() => onSavedGameClicked(game.id)}>
              Game started on {
                new Date(game.date).toLocaleDateString('en-US', {
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SavedGames;
