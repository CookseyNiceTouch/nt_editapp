import React, { useState, useEffect, useCallback, useRef } from 'react';
import './styles.css';

interface ChatMessage {
  type: 'user' | 'assistant' | 'thinking' | 'tool' | 'system';
  content: string;
  timestamp: string;
  conversation_id?: string;
}

const ChatbotInterface: React.FC = () => {
  // State management - no localStorage, use backend history
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [streamingContent, setStreamingContent] = useState<string>('');
  const [currentConversationToolsEnabled, setCurrentConversationToolsEnabled] = useState<boolean>(true);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isInitializing, setIsInitializing] = useState<boolean>(false);
  
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

  // Create conversation when needed
  const createConversationIfNeeded = useCallback(async () => {
    if (currentConversationId || !isConnected) return currentConversationId;
    
    setIsInitializing(true);
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
        setCurrentConversationToolsEnabled(data.tools_enabled);
        
        // Add welcome message
        setMessages(prev => [{
          type: 'system',
          content: data.welcome_message,
          timestamp: new Date().toISOString()
        }, ...prev]);
        
        return data.conversation_id;
      } else {
        const errorData = await response.json();
        addSystemMessage(`Failed to create conversation: ${errorData.detail}`);
        return null;
      }
    } catch (error) {
      addSystemMessage(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
      return null;
    } finally {
      setIsInitializing(false);
    }
  }, [currentConversationId, isConnected]);

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
      } else if (response.status === 404) {
        // Conversation doesn't exist anymore, start fresh
        setCurrentConversationId(null);
        setMessages([]);
        addSystemMessage('Conversation no longer exists. Ready for new conversation.');
      } else {
        const errorData = await response.json().catch(() => ({}));
        addSystemMessage(`Failed to clear conversation: ${errorData.detail || 'Unknown error'}`);
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
      } else if (response.status === 404) {
        // Conversation doesn't exist anymore, start fresh
        setCurrentConversationId(null);
        setMessages([]);
        addSystemMessage('Conversation no longer exists. Ready for new conversation.');
      } else {
        const errorData = await response.json().catch(() => ({}));
        addSystemMessage(`Failed to toggle tools: ${errorData.detail || 'Unknown error'}`);
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
      } else if (response.status === 404) {
        // Conversation doesn't exist anymore, start fresh
        setCurrentConversationId(null);
        setMessages([]);
        addSystemMessage('Conversation no longer exists. Ready for new conversation.');
      } else {
        const errorData = await response.json().catch(() => ({}));
        addSystemMessage(`Failed to restart conversation: ${errorData.detail || 'Unknown error'}`);
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
    if (!inputMessage.trim() || isStreaming || !isConnected) return;
    
    // Create conversation if we don't have one
    let conversationId = currentConversationId;
    if (!conversationId) {
      conversationId = await createConversationIfNeeded();
      if (!conversationId) {
        addSystemMessage('Failed to create conversation. Please try again.');
        return;
      }
    }

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
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${conversationId}/message/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          conversation_id: conversationId,
          stream: true
        })
      });

      if (!response.ok) {
        if (response.status === 404) {
          // Conversation doesn't exist, clear it and let user try again
          setCurrentConversationId(null);
          setMessages([]);
          addSystemMessage('Conversation no longer exists. Please send your message again to start a new conversation.');
          setIsStreaming(false);
          return;
        }
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

  // Check for existing conversations on startup
  const checkForExistingConversations = useCallback(async () => {
    if (!isConnected) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations`);
      if (response.ok) {
        const data = await response.json();
        const conversations = data.conversations || [];
        
        // If we have active conversations, use the most recent one
        if (conversations.length > 0 && !currentConversationId) {
          const mostRecent = conversations.reduce((latest: any, current: any) => {
            const latestTime = new Date(latest.last_message_at || latest.created_at || 0);
            const currentTime = new Date(current.last_message_at || current.created_at || 0);
            return currentTime > latestTime ? current : latest;
          });
          
          setCurrentConversationId(mostRecent.conversation_id);
          setCurrentConversationToolsEnabled(mostRecent.tools_enabled);
        }
      }
    } catch (error) {
      console.warn('Failed to check for existing conversations:', error);
    }
  }, [isConnected, currentConversationId]);

  // Effects
  useEffect(() => {
    checkConnection();
    
    const interval = setInterval(() => {
      checkConnection();
    }, 10000);
    
    return () => clearInterval(interval);
  }, [checkConnection]);

  // Check for existing conversations when connected
  useEffect(() => {
    if (isConnected && !currentConversationId) {
      checkForExistingConversations();
    }
  }, [isConnected, currentConversationId, checkForExistingConversations]);

  // Load conversation history from backend when we have a conversation ID
  const loadConversationHistory = useCallback(async (conversationId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${conversationId}/messages`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
      } else if (response.status === 404) {
        // Conversation doesn't exist anymore
        setCurrentConversationId(null);
        setMessages([]);
      }
    } catch (error) {
      console.warn('Failed to load conversation history:', error);
    }
  }, []);

  // Load conversation history when we have a conversation ID
  useEffect(() => {
    if (currentConversationId && isConnected && messages.length === 0) {
      loadConversationHistory(currentConversationId);
    }
  }, [currentConversationId, isConnected, messages.length, loadConversationHistory]);

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
            {currentConversationId && (
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
          {/* Show initialization status */}
          {isInitializing && (
            <div className="message system">
              <div className="message-header">
                <span className="message-type">⚙️ System</span>
                <span className="message-time">Initializing...</span>
              </div>
              <div className="message-content">
                <pre>🔄 Creating chat conversation...</pre>
              </div>
            </div>
          )}
          
          {/* Show connection status if not connected */}
          {!isConnected && !isInitializing && (
            <div className="message system">
              <div className="message-header">
                <span className="message-type">⚙️ System</span>
                <span className="message-time">Disconnected</span>
              </div>
              <div className="message-content">
                <pre>🔴 Waiting for connection to chatbot API...</pre>
              </div>
            </div>
          )}
          
          {/* Show welcome message when connected but no conversation */}
          {isConnected && !currentConversationId && !isInitializing && messages.length === 0 && (
            <div className="message system">
              <div className="message-header">
                <span className="message-type">💬 Welcome</span>
                <span className="message-time">Ready</span>
              </div>
              <div className="message-content">
                <pre>🤖 Welcome! Send a message to start your conversation with the AI assistant.</pre>
              </div>
            </div>
          )}
          
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
            placeholder={
              isInitializing ? "Creating conversation..." :
              !isConnected ? "Connecting to chatbot..." :
              "Type your message to start chatting... (Enter to send, Shift+Enter for new line)"
            }
            disabled={!isConnected || isStreaming || isInitializing}
            rows={3}
          />
          <button 
            onClick={sendMessage}
            className="btn-success send-btn"
            disabled={!isConnected || !inputMessage.trim() || isStreaming || isInitializing}
          >
            {isInitializing ? '⏳ Creating...' : 
             isStreaming ? '⏳ Sending...' : 
             '📤 Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotInterface;
