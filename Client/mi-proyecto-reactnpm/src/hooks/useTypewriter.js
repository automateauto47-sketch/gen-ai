// src/hooks/useTypewriter.js
import { useState, useEffect } from 'react';

export function useTypewriter(text, speed = 30) {
  const [displayedText, setDisplayedText] = useState("");

  useEffect(() => {
    setDisplayedText(""); // Reiniciamos el texto cada vez que cambia la escena
    let i = 0;
    
    const timer = setInterval(() => {
      setDisplayedText((prev) => text.slice(0, prev.length + 1));
      i++;
      if (i >= text.length) clearInterval(timer);
    }, speed);

    return () => clearInterval(timer); // Limpieza si el usuario salta de página rápido
  }, [text, speed]);

  return displayedText;
}