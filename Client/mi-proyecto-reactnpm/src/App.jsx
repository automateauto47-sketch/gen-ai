import { useState } from 'react';
import { Scene } from './components/Scene';
import './App.css';

/**
 * NARRATIVE DATA STRUCTURE
 * * Each node represents a "Scene" in the story.
 * @property {string} text - The narrative text displayed to the user.
 * @property {string} image - URL for the background visual.
 * @property {Array} options - List of choices the user can make.
 * @property {string} text - Button label.
 * @property {string} nextId - The ID of the next scene.
 * @property {string} [getItem] - (Optional) Adds an item to the inventory.
 * @property {string} [requiredItem] - (Optional) Only shows this choice if the user has the item.
 */
const storyData = {
  start: {
    text: "System initialized. You find yourself in a dimly lit server room. A 'Debug Protocol' manual lies on the floor.",
    image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc4b?q=80&w=1200",
    options: [
      { text: "Take the Manual", nextId: "hallway", getItem: "Manual" },
      { text: "Exit the room", nextId: "hallway" }
    ]
  },
  hallway: {
    text: "The hallway branches into two paths. A terminal at the end requires an administrator override.",
    image: "https://images.unsplash.com/photo-1510511459019-5dee995d3ff4?q=80&w=1200",
    options: [
      { text: "Use Manual to hack terminal", nextId: "success", requiredItem: "Manual" },
      { text: "Try to guess the password", nextId: "fail" },
      { text: "Go back to start", nextId: "start" }
    ]
  },
  success: {
    text: "Access Granted! You've successfully bypassed the security layers. The hackathon project is complete.",
    image: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1200",
    options: [{ text: "Reboot System", nextId: "start" }]
  },
  fail: {
    text: "Access Denied. Security bots have detected your presence. System Lockdown engaged.",
    image: "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=1200",
    options: [{ text: "Retry from Start", nextId: "start" }]
  }
};

/**
 * MAIN APPLICATION COMPONENT
 * Handles global state: Current Scene and Inventory Management.
 */
function App() {
  // HOOKS: State Management
  const [currentSceneId, setCurrentSceneId] = useState("start");
  const [inventory, setInventory] = useState([]);

  // DERIVED STATE: Fetching the current scene object based on the ID
  const currentScene = storyData[currentSceneId];

  /**
   * NAVIGATION HANDLER
   * Processes player choices, updates inventory, and transitions state.
   * @param {Object} option - The selected choice object.
   */
  const handleChoice = (option) => {
    // Inventory Logic: Add item if provided and not already owned
    if (option.getItem && !inventory.includes(option.getItem)) {
      setInventory((prev) => [...prev, option.getItem]);
    }

    // Reset Logic: Clear inventory if player restarts
    if (option.nextId === "start") {
      setInventory([]);
    }

    // Transition Logic: Set new scene ID
    setCurrentSceneId(option.nextId);
  };

  return (
    <main className="story-board">
      {/* 1. VISUAL & TEXT LAYER */}
      <Scene 
        text={currentScene.text} 
        image={currentScene.image} 
      />

      {/* 2. HUD LAYER (Heads-Up Display) */}
      <div className="hud-inventory" aria-label="Player Inventory">
        <span className="hud-label">LOGS:</span>
        {inventory.length === 0 ? (
          <span className="hud-empty"> No items found</span>
        ) : (
          inventory.map((item) => (
            <span key={item} className="inventory-tag">
              {item}
            </span>
          ))
        )}
      </div>

      {/* 3. INTERACTION LAYER */}
      <nav className="controls-container">
        {currentScene.options.map((option, index) => {
          // Conditional Rendering: Check if player meets requirements
          const isLocked = option.requiredItem && !inventory.includes(option.requiredItem);
          
          if (isLocked) return null;

          return (
            <button
              key={`${currentSceneId}-${index}`}
              className="action-button"
              onClick={() => handleChoice(option)}
            >
              {option.text}
            </button>
          );
        })}
      </nav>
    </main>
  );
}

export default App;