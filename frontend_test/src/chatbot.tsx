import React, { useState, useEffect, useCallback, useRef } from 'react';
import './styles.css';

interface ChatMessage {
  type: 'user' | 'assistant' | 'thinking' | 'tool' | 'system';
  content: string;
  timestamp: string;
  conversation_id?: string;
}

interface Conversation {
  conversation_id: string;
  message_count: number;
  created_at?: string;
  last_message_at?: string;
  tools_enabled: boolean;
}

interface Tool {
  name: string;
  description: string;
  parameters?: any;
}

interface ApiStatus {
  status: string;
  isConnected: boolean;
  active_conversations?: number;
  error?: string;
}

const ChatbotInterface: React.FC = () => {
  // State management
  const [apiStatus, setApiStatus] = useState<ApiStatus>({ status: 'Checking...', isConnected: false });
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [availableTools, setAvailableTools] = useState<Tool[]>([]);
  const [toolsEnabled, setToolsEnabled] = useState<boolean>(true);
  const [streamingContent, setStreamingContent] = useState<string>('');
  
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

  // API Status Check
  const checkApiStatus = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/status`);
      if (response.ok) {
        const data = await response.json();
        setApiStatus({
          status: `✅ Connected - ${data.status}`,
          isConnected: true,
          active_conversations: data.active_conversations
        });
      } else {
        setApiStatus({
          status: `❌ API Error (${response.status})`,
          isConnected: false
        });
      }
    } catch (error) {
      setApiStatus({
        status: '❌ Chatbot API Not Available',
        isConnected: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }, []);

  // Load available tools
  const loadAvailableTools = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/tools`);
      if (response.ok) {
        const data = await response.json();
        setAvailableTools(data.tools || []);
      }
    } catch (error) {
      console.error('Failed to load tools:', error);
    }
  }, []);

  // Load conversations
  const loadConversations = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations`);
      if (response.ok) {
        const data = await response.json();
        setConversations(data.conversations || []);
      }
    } catch (error) {
      console.error('Failed to load conversations:', error);
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
          enable_tools: toolsEnabled
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
        
        // Reload conversations list
        loadConversations();
        
        addSystemMessage(`New conversation created: ${data.conversation_id}`);
      } else {
        const errorData = await response.json();
        addSystemMessage(`Failed to create conversation: ${errorData.detail}`);
      }
    } catch (error) {
      addSystemMessage(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  // Switch to existing conversation
  const switchConversation = (conversationId: string) => {
    setCurrentConversationId(conversationId);
    setMessages([{
      type: 'system',
      content: `Switched to conversation: ${conversationId}`,
      timestamp: new Date().toISOString()
    }]);
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

  // Delete conversation
  const deleteConversation = async (conversationId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/conversations/${conversationId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        loadConversations();
        if (conversationId === currentConversationId) {
          setCurrentConversationId(null);
          setMessages([]);
        }
        addSystemMessage(`Conversation ${conversationId} deleted`);
      }
    } catch (error) {
      addSystemMessage(`Failed to delete conversation: ${error instanceof Error ? error.message : 'Unknown error'}`);
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

      // Create new EventSource for streaming
      const eventSource = new EventSource(
        `${API_BASE_URL}/chatbot/conversations/${currentConversationId}/message/stream`,
        {
          // Note: EventSource doesn't support POST directly, so we'll use fetch with streaming
        }
      );

      // Actually, let's use fetch with streaming instead
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
                    setStreamingContent(prev => prev + eventData.content);
                    break;
                    
                  case 'tool':
                    toolMessages.push(eventData.content);
                    setMessages(prev => [...prev, {
                      type: 'tool',
                      content: eventData.content,
                      timestamp: new Date().toISOString()
                    }]);
                    break;
                    
                  case 'response':
                    assistantMessage += eventData.content;
                    setStreamingContent(assistantMessage);
                    break;
                    
                  case 'complete':
                    // Add final assistant message
                    if (assistantMessage) {
                      setMessages(prev => [...prev, {
                        type: 'assistant',
                        content: assistantMessage,
                        timestamp: new Date().toISOString()
                      }]);
                    }
                    
                    // Add thinking as separate message if present
                    if (thinkingMessage) {
                      setMessages(prev => [...prev, {
                        type: 'thinking',
                        content: thinkingMessage,
                        timestamp: new Date().toISOString()
                      }]);
                    }
                    
                    setStreamingContent('');
                    setIsStreaming(false);
                    
                    if (eventData.tool_calls && eventData.tool_calls.length > 0) {
                      addSystemMessage(`✅ Completed with ${eventData.tool_calls.length} tool call(s)`);
                    }
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
    checkApiStatus();
    loadAvailableTools();
    loadConversations();
    
    const interval = setInterval(() => {
      checkApiStatus();
      loadConversations();
    }, 10000);
    
    return () => clearInterval(interval);
  }, [checkApiStatus, loadAvailableTools, loadConversations]);

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
        <h1>🤖 AI Video Editing Chatbot</h1>
        <p>Conversational AI with tool calling capabilities</p>
      </div>

      {/* API Status */}
      <div className="section api-status">
        <div className="section-header">
          <h3>API Status</h3>
          <button onClick={checkApiStatus} className="btn-small">
            🔄 Refresh
          </button>
        </div>
        <div className="status-display">
          <span className={`status-indicator ${apiStatus.isConnected ? 'connected' : 'disconnected'}`}>
            {apiStatus.status}
          </span>
          {apiStatus.active_conversations !== undefined && (
            <span className="conversation-count">
              Active conversations: {apiStatus.active_conversations}
            </span>
          )}
        </div>
      </div>

      {/* Conversation Management */}
      <div className="section conversation-management">
        <div className="section-header">
          <h3>Conversations</h3>
          <div className="conversation-controls">
            <label className="tools-toggle">
              <input
                type="checkbox"
                checked={toolsEnabled}
                onChange={(e) => setToolsEnabled(e.target.checked)}
              />
              Tools Enabled
            </label>
            <button onClick={createConversation} className="btn-success" disabled={!apiStatus.isConnected}>
              ➕ New Chat
            </button>
          </div>
        </div>
        
        <div className="conversations-list">
          {conversations.length === 0 ? (
            <div className="no-conversations">No active conversations</div>
          ) : (
            conversations.map(conv => (
              <div 
                key={conv.conversation_id} 
                className={`conversation-item ${conv.conversation_id === currentConversationId ? 'active' : ''}`}
              >
                <div className="conversation-info" onClick={() => switchConversation(conv.conversation_id)}>
                  <span className="conversation-id">{conv.conversation_id}</span>
                  <span className="message-count">{conv.message_count} messages</span>
                  <span className="tools-status">{conv.tools_enabled ? '🔧' : '🚫'}</span>
                </div>
                <button 
                  onClick={() => deleteConversation(conv.conversation_id)}
                  className="btn-small delete-btn"
                >
                  🗑️
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Chat Interface */}
      <div className="section chat-interface">
        <div className="section-header">
          <h3>Chat {currentConversationId && `- ${currentConversationId}`}</h3>
          <div className="chat-controls">
            <button 
              onClick={clearConversation} 
              className="btn-small"
              disabled={!currentConversationId}
            >
              🗑️ Clear
            </button>
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
            placeholder={currentConversationId ? "Type your message... (Enter to send, Shift+Enter for new line)" : "Create a conversation to start chatting"}
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

      {/* Tools Panel */}
      <div className="section tools-panel">
        <div className="section-header">
          <h3>Available Tools</h3>
          <button onClick={loadAvailableTools} className="btn-small">
            🔄 Refresh
          </button>
        </div>
        
        <div className="tools-list">
          {availableTools.length === 0 ? (
            <div className="no-tools">No tools available</div>
          ) : (
            availableTools.map(tool => (
              <div key={tool.name} className="tool-item">
                <div className="tool-name">{tool.name}</div>
                <div className="tool-description">{tool.description}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatbotInterface;
