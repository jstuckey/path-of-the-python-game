class GameService {
  constructor() {
    this.baseUrl = process.env.REACT_APP_BACKEND_URL;
  }

  async createGame() {
    const response = await fetch(`${this.baseUrl}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      throw new Error(`Failed to create game: ${response.status}`);
    }

    return response.json();
  }

  async loadGame(gameId) {
    const response = await fetch(`${this.baseUrl}/games/${gameId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      throw new Error(`Failed to load game: ${response.status}`);
    }

    return response.json();
  }

  async submitTurn(gameId, prompt) {
    const response = await fetch(
      `${this.baseUrl}/games/${gameId}/turn?prompt=${encodeURIComponent(prompt)}`,
      { method: 'POST' }
    );

    if (!response.ok) {
      throw new Error(`Failed to submit turn: ${response.status}`);
    }

    return response.json();
  }
}

export default new GameService();
