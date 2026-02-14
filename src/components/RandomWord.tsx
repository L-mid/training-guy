import React, { useEffect, useMemo, useState } from "react";

type Props = {
  words: string[];
  storageKey?: string; // so you can have multiple rollers on different pages
  title?: string;
  buttonText?: string;
};

export default function RandomWord({
  words,
  storageKey = "random_word_once",
  title = "Random",
  buttonText = "Roll",
}: Props) {
  const clean = useMemo(() => words.map(w => w.trim()).filter(Boolean), [words]);

  const [word, setWord] = useState<string | null>(null);
  const [locked, setLocked] = useState(false);

  // On load: restore from sessionStorage
  useEffect(() => {
    try {
      const saved = sessionStorage.getItem(storageKey);
      if (saved) {
        setWord(saved);
        setLocked(true);
      }
    } catch {
      // sessionStorage can be unavailable in rare cases; ignore
    }
  }, [storageKey]);

  function rollOnce() {
    if (locked) return;
    if (clean.length === 0) return;

    const i = Math.floor(Math.random() * clean.length);
    const picked = clean[i];

    setWord(picked);
    setLocked(true);

    try {
      sessionStorage.setItem(storageKey, picked);
    } catch {
      // ignore if storage fails
    }
  }

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 12, margin: "12px 0" }}>
      <div style={{ display: "flex", gap: 8, alignItems: "center", justifyContent: "space-between" }}>
        <strong>{title}</strong>
        <button
          className="button button--sm button--primary"
          onClick={rollOnce}
          disabled={locked || clean.length === 0}
          title={locked ? "Already rolled this session" : ""}
        >
          {locked ? "Locked" : buttonText}
        </button>
      </div>

      {word && (
        <div style={{ marginTop: 10, fontSize: 18 }}>
          <code>{word}</code>
        </div>
      )}

      {clean.length === 0 && (
        <div style={{ marginTop: 10, opacity: 0.7 }}>
          (No words provided)
        </div>
      )}
    </div>
  );
}
