// src/components/Scene.jsx
import { useTypewriter } from '../hooks/useTypewriter';

export function Scene({ text, image }) {
  // Aquí activamos la magia. 40 es la velocidad en milisegundos.
  const animatedText = useTypewriter(text, 40);

  return (
    <div 
      className="scene-container" 
      style={{ backgroundImage: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.7)), url(${image})` }}
    >
      <div className="narrative-box">
        <p>{animatedText}<span className="cursor">|</span></p>
      </div>
    </div>
  );
}