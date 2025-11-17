import React, { useState, useRef, useEffect } from 'react';
import './PromptInput.css';

function PromptInput({ gameId, onSubmit, isSubmitting }) {
  const [prompt, setPrompt] = useState("");

  const inputRef = useRef(null);

  useEffect(() => {
    if (!gameId) return;

    requestAnimationFrame(() => {
      inputRef.current?.focus();
    });
  }, [gameId]);

  const onPromptChange = (value) => {
    setPrompt(value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt) return;

    onSubmit(prompt);

    setPrompt("");
    inputRef.current?.focus();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        ref={inputRef}
        value={prompt}
        onChange={(e) => onPromptChange(e.target.value)}
        placeholder="What would you like to do?"
        type="text"
      />
      <button type="submit" tabIndex={0} disabled={isSubmitting || !prompt}>
        Submit
      </button>
    </form>
  );
}

export default PromptInput;
