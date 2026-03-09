// src/components/Scene.jsx
export function Scene({ text }) {
  return (
    <div className="scene-container">
      {/* Aquí luego podríamos agregar la imagen correspondiente */}
      <div className="narrative-box">
        <p>{text}</p>
      </div>
    </div>
  );
}