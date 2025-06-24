import { useState } from 'react';
import VideoAnalyzer from './analyzer';
import ChatbotInterface from './chatbot';
import './App.css';
import './styles.css';

type TabType = 'analyzer' | 'chatbot';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('analyzer');

  return (
    <div className="app-container">
      <nav className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'analyzer' ? 'active' : ''}`}
          onClick={() => setActiveTab('analyzer')}
        >
          🎬 Video Analyzer
        </button>
        <button
          className={`tab-button ${activeTab === 'chatbot' ? 'active' : ''}`}
          onClick={() => setActiveTab('chatbot')}
        >
          🤖 AI Chatbot
        </button>
      </nav>

      <div className="tab-content">
        {activeTab === 'analyzer' && <VideoAnalyzer />}
        {activeTab === 'chatbot' && <ChatbotInterface />}
      </div>
    </div>
  );
}

export default App;
