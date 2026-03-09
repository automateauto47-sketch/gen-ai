import { useState } from 'react';
import { Scene } from './components/Scene';
import './App.css';

// 1. Aquí definimos nuestra historia
const storyData = [
  { id: 1, text: "our baby is amazing doing well for us, I really love it" },
  { id: 2, text: "Suddenly, it appeared in the horizon promising moving with the speed and inmediate charges" },
  { id: 3, text: "Nuestro héroe tecleó 'npm run dev' y el mundo cambió para siempre. Fin." }
];

function App() {
  // 2. Creamos el estado para saber en qué página estamos. Empezamos en la 0 (la primera)
  const [currentPage, setCurrentPage] = useState(0);

  // 3. Funciones para avanzar y retroceder
  const handleNext = () => {
    // Solo avanzamos si NO estamos en la última página
    if (currentPage < storyData.length - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrev = () => {
    // Solo retrocedemos si NO estamos en la primera página
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <main className="story-board">
      {/* Pasamos el texto de la página actual a nuestra Escena */}
      <Scene text={storyData[currentPage].text} />

      {/* 4. Los controles de navegación */}
      <div className="controls">
        <button 
          onClick={handlePrev} 
          disabled={currentPage === 0} // Desactiva el botón si estamos al inicio
        >
          Anterior
        </button>
        
        <span className="page-indicator">
          Página {currentPage + 1} de {storyData.length}
        </span>

        <button 
          onClick={handleNext} 
          disabled={currentPage === storyData.length - 1} // Desactiva si es el final
        >
          Siguiente
        </button>
      </div>
    </main>
  );
}

export default App;