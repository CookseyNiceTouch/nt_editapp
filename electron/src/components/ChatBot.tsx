import { useState } from 'react'
import { Message } from '../types'

interface ChatBotProps {
  // No props needed for now, but we can add them later if needed
}

export default function ChatBot({}: ChatBotProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')

  // Handle chat message
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage: Message = { text: inputMessage, sender: 'user' }
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')

    try {
      // Call orchestrator API for chatbot
      const response = await fetch('http://localhost:4000/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
        }),
      })
      
      const result = await response.json()
      const botMessage: Message = { 
        text: result.response || result.message || 'Chatbot service ready (not yet implemented)', 
        sender: 'bot'
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage: Message = { 
        text: 'Error connecting to chatbot service', 
        sender: 'bot'
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="chatbot-panel">
      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <p>Welcome! Ask me anything about video editing, or request specific edits.</p>
              <p>I can help with:</p>
              <ul>
                <li>Generate edit suggestions</li>
                <li>Automate editing tasks</li>
                <li>Answer questions about your footage</li>
              </ul>
            </div>
          ) : (
            messages.map((message, index) => (
              <div key={index} className={`message ${message.sender}`}>
                <div className="message-content">
                  {message.text}
                </div>
              </div>
            ))
          )}
        </div>
        
        <div className="chat-input-area">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
            className="chat-input"
            rows={3}
          />
          <button 
            onClick={handleSendMessage}
            disabled={!inputMessage.trim()}
            className="send-button"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
} 