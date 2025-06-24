import { useState } from 'react';
import VideoAnalyzer from './analyzer';
import ChatbotInterface from './chatbot';
import ProjectManager from './projectmanager';
import './App.css';
import './styles.css';

type TabType = 'analyzer' | 'chatbot' | 'project';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('analyzer');

  return (
    <div className="app-container">
      <nav className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'project' ? 'active' : ''}`}
          onClick={() => setActiveTab('project')}
        >
          🎬 Project Manager
        </button>
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
          💬 AI Chat
        </button>
      </nav>

      <div className="tab-content">
        {activeTab === 'analyzer' && <VideoAnalyzer />}
        {activeTab === 'chatbot' && <ChatbotInterface />}
        {activeTab === 'project' && <ProjectManager />}
      </div>
    </div>
  );
}

export default App;
