import React, { useState, useEffect, useCallback, useRef } from 'react';
import './styles.css';

interface ChatMessage {
  type: 'user' | 'assistant' | 'thinking' | 'tool' | 'system';
  content: string;
  timestamp: string;
  conversation_id?: string;
}

const ChatbotInterface: React.FC = () => {
  // State management
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [streamingContent, setStreamingContent] = useState<string>('');
  const [currentConversationToolsEnabled, setCurrentConversationToolsEnabled] = useState<boolean>(true);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const API_BASE_URL = 'http://localhost:8000';

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  // Check API connection
  const checkConnection = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/status`);
      setIsConnected(response.ok);
    } catch (error) {
      setIsConnected(false);
    }
  }, []);

  // Create new conversation
  const createConversation = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          enable_tools: true
        })
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentConversationId(data.conversation_id);
        setMessages([{
          type: 'system',
          content: data.welcome_message,
          timestamp: new Date().toISOString()
        }]);
        
        addSystemMessage(`New conversation created: ${data.conversation_id}`);
      } else {
        const errorData = await response.json();
        addSystemMessage(`Failed to create conversation: ${errorData.detail}`);
      }
    } catch (error) {
      addSystemMessage(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  // Clear current conversation
  const clearConversation = async () => {
    if (!currentConversationId) return;

    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${currentConversationId}/clear`, {
        method: 'POST'
      });

      if (response.ok) {
        setMessages([{
          type: 'system',
          content: 'Conversation history cleared',
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (error) {
      addSystemMessage(`Failed to clear conversation: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  // Toggle tools for current conversation
  const toggleConversationTools = async () => {
    if (!currentConversationId) return;

    try {
      const newToolsState = !currentConversationToolsEnabled;
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${currentConversationId}/tools/toggle`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          enable_tools: newToolsState
        })
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentConversationToolsEnabled(newToolsState);
        addSystemMessage(data.message);
      } else {
        const errorData = await response.json();
        addSystemMessage(`Failed to toggle tools: ${errorData.detail}`);
      }
    } catch (error) {
      addSystemMessage(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  // Restart conversation
  const restartConversation = async () => {
    if (!currentConversationId) return;

    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${currentConversationId}/restart`, {
        method: 'POST'
      });

      if (response.ok) {
        const data = await response.json();
        setMessages([{
          type: 'system',
          content: data.welcome_message,
          timestamp: new Date().toISOString()
        }]);
        addSystemMessage(data.message);
        
        // Update tools status
        setCurrentConversationToolsEnabled(data.tools_enabled);
      } else {
        const errorData = await response.json();
        addSystemMessage(`Failed to restart conversation: ${errorData.detail}`);
      }
    } catch (error) {
      addSystemMessage(`Failed to restart conversation: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  // Add system message
  const addSystemMessage = (content: string) => {
    setMessages(prev => [...prev, {
      type: 'system',
      content,
      timestamp: new Date().toISOString()
    }]);
  };

  // Send message with streaming
  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentConversationId || isStreaming) return;

    const userMessage: ChatMessage = {
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsStreaming(true);
    setStreamingContent('');

    try {
      // Close any existing EventSource
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }

      // Use fetch with streaming
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${currentConversationId}/message/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          conversation_id: currentConversationId,
          stream: true
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      let assistantMessage = '';
      let thinkingMessage = '';
      let toolMessages: string[] = [];

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = new TextDecoder().decode(value);
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const eventData = JSON.parse(line.slice(6));
                
                switch (eventData.type) {
                  case 'start':
                    addSystemMessage('🤖 Assistant is thinking...');
                    break;
                    
                  case 'thinking':
                    thinkingMessage += eventData.content;
                    // Show thinking content in real-time but don't accumulate for final message
                    setStreamingContent(prev => prev + eventData.content);
                    break;
                    
                  case 'tool':
                    toolMessages.push(eventData.content);
                    addSystemMessage(`🔧 ${eventData.content}`);
                    break;
                    
                  case 'response':
                    assistantMessage += eventData.content;
                    // Show the assistant response as it streams in
                    setStreamingContent(assistantMessage);
                    break;
                    
                  case 'complete':
                    // Clear streaming content first
                    setStreamingContent('');
                    
                    // Add thinking as a separate message if present
                    if (thinkingMessage.trim()) {
                      setMessages(prev => [...prev, {
                        type: 'thinking',
                        content: thinkingMessage.trim(),
                        timestamp: new Date().toISOString()
                      }]);
                    }
                    
                    // Add final assistant message if we have content
                    if (assistantMessage.trim()) {
                      setMessages(prev => [...prev, {
                        type: 'assistant',
                        content: assistantMessage.trim(),
                        timestamp: new Date().toISOString()
                      }]);
                    }
                    
                    // Add tool summary if tools were used
                    if (eventData.tool_calls && eventData.tool_calls.length > 0) {
                      addSystemMessage(`✅ Response completed with ${eventData.tool_calls.length} tool call(s)`);
                    } else {
                      addSystemMessage(`✅ Response completed`);
                    }
                    
                    setIsStreaming(false);
                    break;
                    
                  case 'error':
                    addSystemMessage(`❌ Error: ${eventData.error}`);
                    setIsStreaming(false);
                    setStreamingContent('');
                    break;
                }
              } catch (parseError) {
                console.warn('Failed to parse event data:', parseError);
              }
            }
          }
        }
      } finally {
        reader.releaseLock();
      }

    } catch (error) {
      addSystemMessage(`❌ Streaming error: ${error instanceof Error ? error.message : 'Unknown error'}`);
      setIsStreaming(false);
      setStreamingContent('');
    }
  };

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Effects
  useEffect(() => {
    checkConnection();
    
    const interval = setInterval(() => {
      checkConnection();
    }, 10000);
    
    return () => clearInterval(interval);
  }, [checkConnection]);

  // Cleanup EventSource on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h1>💬 AI Chat</h1>
        <p>Conversational AI for video editing assistance</p>
      </div>

      {/* Connection Status */}
      <div className="chat-status">
        <div className="status-indicator">
          <span className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
          </span>
          {currentConversationId && (
            <span className="conversation-id">
              Conversation: {currentConversationId}
            </span>
          )}
        </div>
      </div>

      {/* Chat Interface */}
      <div className="section chat-interface">
        <div className="section-header">
          <h3>💬 Chat</h3>
          <div className="chat-controls">
            {!currentConversationId ? (
              <button onClick={createConversation} className="btn-success" disabled={!isConnected}>
                ➕ Start Chat
              </button>
            ) : (
              <>
                <label className="tools-toggle">
                  <input
                    type="checkbox"
                    checked={currentConversationToolsEnabled}
                    onChange={toggleConversationTools}
                  />
                  Tools: {currentConversationToolsEnabled ? '🔧' : '🚫'}
                </label>
                <button 
                  onClick={restartConversation} 
                  className="btn-small"
                  disabled={!currentConversationId}
                >
                  🔄 Restart
                </button>
                <button 
                  onClick={clearConversation} 
                  className="btn-small"
                  disabled={!currentConversationId}
                >
                  🗑️ Clear
                </button>
              </>
            )}
          </div>
        </div>

        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-header">
                <span className="message-type">
                  {message.type === 'user' && '👤 You'}
                  {message.type === 'assistant' && '🤖 Assistant'}
                  {message.type === 'thinking' && '🧠 Thinking'}
                  {message.type === 'tool' && '🔧 Tool'}
                  {message.type === 'system' && '⚙️ System'}
                </span>
                <span className="message-time">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <div className="message-content">
                <pre>{message.content}</pre>
              </div>
            </div>
          ))}
          
          {/* Streaming content */}
          {isStreaming && streamingContent && (
            <div className="message assistant streaming">
              <div className="message-header">
                <span className="message-type">🤖 Assistant</span>
                <span className="message-time">Streaming...</span>
              </div>
              <div className="message-content">
                <pre>{streamingContent}</pre>
                <span className="streaming-cursor">▊</span>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={currentConversationId ? "Type your message... (Enter to send, Shift+Enter for new line)" : "Start a chat to begin"}
            disabled={!currentConversationId || isStreaming}
            rows={3}
          />
          <button 
            onClick={sendMessage}
            className="btn-success send-btn"
            disabled={!currentConversationId || !inputMessage.trim() || isStreaming}
          >
            {isStreaming ? '⏳ Sending...' : '📤 Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotInterface;
