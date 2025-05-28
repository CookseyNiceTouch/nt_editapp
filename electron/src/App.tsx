import { useState } from 'react'
import './App.css'
import { FootageIngest, ChatBot } from './components'
import { TabType } from './types'

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('footage')

  return (
    <div className="app">
      <header className="app-header">
        <h1>NT Edit App</h1>
        <nav className="tab-navigation">
          <button 
            className={`tab-button ${activeTab === 'footage' ? 'active' : ''}`}
            onClick={() => setActiveTab('footage')}
          >
            Footage Analysis & Ingest
          </button>
          <button 
            className={`tab-button ${activeTab === 'chatbot' ? 'active' : ''}`}
            onClick={() => setActiveTab('chatbot')}
          >
            AI Assistant
          </button>
        </nav>
      </header>

      <main className="app-main">
        {activeTab === 'footage' && <FootageIngest />}
        {activeTab === 'chatbot' && <ChatBot />}
      </main>
    </div>
  )
}

export default App
