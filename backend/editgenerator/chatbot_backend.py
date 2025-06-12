import os
import sys
import json
import logging
import asyncio
from pathlib import Path
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic
from prompts.prompts_chatbot import system_prompt, user_prompt, welcome_prompt
from toolcalling.toolcaller import tool_caller, get_tool_schemas_for_claude

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get paths relative to script location (backend/editgenerator)
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Go up from backend/editgenerator to project root

# File paths (relative to project root)
CONVERSATIONS_DIR = PROJECT_ROOT / "data" / "conversations"
PROJECT_DATA_PATH = PROJECT_ROOT / "data" / "projectdata.json"

# Constants
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 12000  # Total token limit for response including thinking
THINKING_BUDGET = 8000  # Maximum tokens for Claude's extended thinking process
MAX_CONVERSATION_HISTORY = 10  # Keep last 10 exchanges for context

class ChatbotBackend:
    """Main chatbot backend class for handling conversations with Claude."""
    
    def __init__(self, conversation_id: Optional[str] = None, enable_tools: bool = True):
        """Initialize the chatbot backend with optional conversation ID."""
        self.conversation_id = conversation_id or self._generate_conversation_id()
        self.conversation_history: List[Dict[str, str]] = []
        self.client = None
        self.project_data = None
        self.enable_tools = enable_tools
        self._initialize_client()
        self._load_project_data()
        
        logger.info(f"Initialized chatbot with conversation ID: {self.conversation_id}")
        logger.info(f"Tools enabled: {self.enable_tools}")
        logger.info("Conversation saving disabled - using in-memory only")
        if self.project_data:
            logger.info(f"Loaded project context: {self.project_data.get('title', 'Unknown')}")
    
    def _generate_conversation_id(self) -> str:
        """Generate a unique conversation ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"chat_{timestamp}"
    
    def _initialize_client(self):
        """Initialize the Claude API client."""
        api_key = os.environ.get("claude_api_key")
        if not api_key:
            raise ValueError("Claude API key not found. Set claude_api_key in .env file.")
        
        self.client = Anthropic(api_key=api_key)
        logger.info("Claude client initialized successfully")
    
    def _ensure_conversations_dir(self):
        """Ensure the conversations directory exists."""
        CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_project_data(self):
        """Load project data from the standard project data file."""
        if not PROJECT_DATA_PATH.exists():
            logger.warning(f"Project data file not found at: {PROJECT_DATA_PATH}")
            self.project_data = None
            return
        
        try:
            with open(PROJECT_DATA_PATH, "r", encoding="utf-8") as f:
                project_json = json.load(f)
            
            # Extract and structure the project data
            self.project_data = {
                "title": project_json.get("projectTitle", "Unknown Project"),
                "brief": project_json.get("projectBrief", ""),
                "raw_data": project_json  # Keep the original data for reference
            }
            
            if not self.project_data["brief"]:
                logger.warning("Project brief is empty in project data file")
            
            logger.info(f"Loaded project data: {self.project_data['title']}")
            logger.info(f"Brief length: {len(self.project_data['brief'])} characters")
        
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in project data file: {e}")
            self.project_data = None
        except Exception as e:
            logger.error(f"Error loading project data: {e}")
            self.project_data = None
    
    def get_conversation_file_path(self) -> Path:
        """Get the file path for storing this conversation."""
        return CONVERSATIONS_DIR / f"{self.conversation_id}.json"
    
    def load_conversation_history(self) -> bool:
        """Load conversation history from file if it exists."""
        conversation_file = self.get_conversation_file_path()
        
        if conversation_file.exists():
            try:
                with open(conversation_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.conversation_history = data.get("messages", [])
                logger.info(f"Loaded {len(self.conversation_history)} messages from conversation file")
                return True
            
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Error loading conversation history: {e}")
                return False
        
        return False
    
    def save_conversation_history(self):
        """Save conversation history to file."""
        conversation_file = self.get_conversation_file_path()
        
        try:
            conversation_data = {
                "conversation_id": self.conversation_id,
                "created_at": datetime.now().isoformat(),
                "message_count": len(self.conversation_history),
                "messages": self.conversation_history
            }
            
            with open(conversation_file, "w", encoding="utf-8") as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved conversation to {conversation_file}")
        
        except Exception as e:
            logger.error(f"Error saving conversation history: {e}")
    
    def add_to_history(self, user_message: str, assistant_response: str):
        """Add a message exchange to the conversation history."""
        self.conversation_history.append({
            "user": user_message,
            "assistant": assistant_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only the most recent exchanges to manage context length
        if len(self.conversation_history) > MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY:]
        
        # Note: Conversation saving disabled for testing - using in-memory only
    
    def get_recent_history(self, max_exchanges: int = 5) -> List[Dict[str, str]]:
        """Get recent conversation history for context."""
        return self.conversation_history[-max_exchanges:] if self.conversation_history else []
    
    async def send_message_async(
        self,
        message: str,
        streaming_callback: Optional[Callable[[str, str], None]] = None
    ) -> Dict[str, Any]:
        """Send a message to Claude and get a response asynchronously with proper sequential tool calling."""
        
        if not self.client:
            raise ValueError("Claude client not initialized")
        
        try:
            # Get prompts with conversation history and project context
            system_prompt_text = system_prompt(self.project_data)
            user_prompt_text = user_prompt(message, self.get_recent_history(), self.project_data)
            
            # Get available tools for Claude function calling (if enabled)
            tools = get_tool_schemas_for_claude() if self.enable_tools else None
            
            logger.info(f"Sending message to Claude API (conversation: {self.conversation_id})")
            if self.enable_tools:
                logger.info(f"Available tools: {len(tools)}")
            else:
                logger.info("Tools disabled for this conversation")
            
            # Initialize conversation messages for proper sequential tool calling
            messages = [{"role": "user", "content": user_prompt_text}]
            
            # Track all tool calls made during this conversation
            all_tool_calls = []
            thinking_content = ""
            final_response = ""
            
            # Implement proper sequential tool calling loop
            while True:
                # Create completion parameters
                completion_params = {
                    "model": CLAUDE_MODEL,
                    "max_tokens": MAX_TOKENS,
                    "system": system_prompt_text,
                    "messages": messages,
                    "thinking": {"type": "enabled", "budget_tokens": THINKING_BUDGET},
                }
                
                if self.enable_tools and tools:
                    completion_params["tools"] = tools
                
                # Get Claude's response
                response = self.client.messages.create(**completion_params)
                
                # Extract thinking content if available
                if hasattr(response, 'thinking') and response.thinking:
                    thinking_content += response.thinking
                    if streaming_callback:
                        streaming_callback("thinking", response.thinking)
                
                # Check if Claude wants to use tools
                tool_calls_in_response = []
                text_content = ""
                
                for content_block in response.content:
                    if content_block.type == "text":
                        text_content += content_block.text
                        if streaming_callback:
                            streaming_callback("response", content_block.text)
                    elif content_block.type == "tool_use":
                        tool_calls_in_response.append(content_block)
                        if streaming_callback:
                            streaming_callback("tool", f"\n🔧 Using tool: {content_block.name}")
                
                # Add Claude's response to the message history
                assistant_message = {"role": "assistant", "content": response.content}
                messages.append(assistant_message)
                
                # If no tool calls, we're done
                if not tool_calls_in_response:
                    final_response = text_content
                    break
                
                # Execute all tool calls and add results to messages
                tool_result_content = []
                
                for tool_call in tool_calls_in_response:
                    tool_name = tool_call.name
                    tool_input = tool_call.input
                    tool_id = tool_call.id
                    
                    if streaming_callback:
                        streaming_callback("tool", f"\nExecuting {tool_name}...")
                    
                    # Execute the tool
                    tool_result = tool_caller.call_tool(tool_name, tool_input)
                    
                    # Track this tool call
                    all_tool_calls.append({
                        "tool_name": tool_name,
                        "tool_id": tool_id,
                        "input": tool_input,
                        "result": tool_result
                    })
                    
                    # Add tool result to the content array for this user message
                    tool_result_content.append({
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": json.dumps(tool_result)
                    })
                    
                    # Provide feedback to user
                    if streaming_callback:
                        if tool_result.get("success"):
                            streaming_callback("tool", f"✅ {tool_name} completed")
                            # Show a brief summary of the result
                            if "result" in tool_result:
                                result_summary = str(tool_result["result"])[:100]
                                streaming_callback("tool", f"Result: {result_summary}...")
                        else:
                            streaming_callback("tool", f"❌ {tool_name} failed: {tool_result.get('error', 'Unknown error')}")
                
                # Add all tool results as a single user message
                if tool_result_content:
                    tool_result_message = {
                        "role": "user",
                        "content": tool_result_content
                    }
                    messages.append(tool_result_message)
                
                # Continue the loop - Claude will now see all tool results and can make more calls or respond
                if streaming_callback:
                    streaming_callback("response", "\n\nAnalyzing results...")
            
            # Add to conversation history
            self.add_to_history(message, final_response)
            
            return {
                "success": True,
                "response": final_response,
                "thinking": thinking_content,
                "tool_calls": all_tool_calls,
                "conversation_id": self.conversation_id,
                "message_count": len(self.conversation_history)
            }
        
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "conversation_id": self.conversation_id
            }
    
    def send_message(
        self,
        message: str,
        streaming_callback: Optional[Callable[[str, str], None]] = None
    ) -> Dict[str, Any]:
        """Synchronous wrapper around the async send_message function."""
        
        # Get the current event loop or create a new one (fix deprecation warning)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    self.send_message_async(message, streaming_callback)
                )
            finally:
                loop.close()
        else:
            # There's already a running loop, we need to run in a new thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run, 
                    self.send_message_async(message, streaming_callback)
                )
                return future.result()
    
    def get_welcome_message(self) -> str:
        """Get the welcome message for new conversations."""
        return welcome_prompt(self.project_data)
    
    def clear_conversation(self):
        """Clear the current conversation history."""
        self.conversation_history.clear()
        logger.info(f"Cleared conversation history for {self.conversation_id}")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation."""
        return {
            "conversation_id": self.conversation_id,
            "message_count": len(self.conversation_history),
            "created_at": self.conversation_history[0]["timestamp"] if self.conversation_history else None,
            "last_message_at": self.conversation_history[-1]["timestamp"] if self.conversation_history else None,
            "conversation_file": str(self.get_conversation_file_path())
        }
    
    def call_tool_manually(self, tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Manually call a tool for testing purposes."""
        return tool_caller.call_tool(tool_name, parameters)
    
    def list_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        return tool_caller.get_available_tools()

def stream_to_console(stream_type: str, content: str):
    """
    Console streaming callback for testing and demonstration.
    Formats the output for better readability including tool usage.
    """
    if stream_type == "thinking":
        # For thinking content, print in gray/dim
        print(f"\033[90m[Thinking] {content}\033[0m", end="")
    elif stream_type == "tool":
        # For tool usage, print in blue/cyan
        print(f"\033[96m{content}\033[0m")
    else:
        # For response content, print in default color
        print(content, end="")

def list_conversations() -> List[Dict[str, Any]]:
    """List all available conversations."""
    if not CONVERSATIONS_DIR.exists():
        return []
    
    conversations = []
    for conv_file in CONVERSATIONS_DIR.glob("*.json"):
        try:
            with open(conv_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            conversations.append({
                "conversation_id": data.get("conversation_id", conv_file.stem),
                "created_at": data.get("created_at"),
                "message_count": data.get("message_count", 0),
                "file_path": str(conv_file)
            })
        except Exception as e:
            logger.warning(f"Error reading conversation file {conv_file}: {e}")
    
    # Sort by creation date (newest first)
    conversations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return conversations

# Main execution when script is run directly
if __name__ == "__main__":
    try:
        print("=== AI Video Editing Chatbot ===")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'clear' to start a new conversation")
        print("Type 'history' to see conversation summary")
        print("Type 'tools' to see available tools")
        print("Type 'test-tool <name>' to manually test a tool")
        print("Type 'toggle-tools' to toggle tools")
        print("="*50)
        
        # Initialize chatbot
        chatbot = ChatbotBackend()
        
        # Start fresh conversation (saving disabled for testing)
        print(f"Starting new conversation: {chatbot.conversation_id}")
        print("\n" + chatbot.get_welcome_message())
        
        print("\n" + "="*50)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                elif user_input.lower() == 'clear':
                    chatbot.clear_conversation()
                    print("Conversation cleared. Starting fresh!")
                    print("\n" + chatbot.get_welcome_message())
                    continue
                
                elif user_input.lower() == 'history':
                    summary = chatbot.get_conversation_summary()
                    print(f"\nConversation Summary:")
                    print(f"  ID: {summary['conversation_id']}")
                    print(f"  Messages: {summary['message_count']}")
                    print(f"  Created: {summary['created_at']}")
                    print(f"  Last message: {summary['last_message_at']}")
                    continue
                
                elif user_input.lower() == 'list':
                    print("\nConversation saving is disabled for testing.")
                    print("Only current in-memory conversation is available.")
                    continue
                
                elif user_input.lower() == 'tools':
                    tools = chatbot.list_available_tools()
                    print(f"\nAvailable Tools ({len(tools)}):")
                    for tool in tools:
                        print(f"  • {tool['name']}: {tool['description']}")
                    continue
                
                elif user_input.lower().startswith('test-tool '):
                    # Manual tool testing: test-tool tool_name
                    tool_name = user_input[10:].strip()
                    if tool_name:
                        print(f"\nTesting tool: {tool_name}")
                        result = chatbot.call_tool_manually(tool_name)
                        if result.get("success"):
                            print(f"✅ Tool succeeded:")
                            print(json.dumps(result.get("result"), indent=2))
                        else:
                            print(f"❌ Tool failed: {result.get('error')}")
                    else:
                        print("Usage: test-tool <tool_name>")
                    continue
                
                elif user_input.lower() == 'toggle-tools':
                    chatbot.enable_tools = not chatbot.enable_tools
                    status = "enabled" if chatbot.enable_tools else "disabled"
                    print(f"\n🔧 Tools are now {status}")
                    continue
                
                elif not user_input:
                    print("Please enter a message or command.")
                    continue
                
                # Send message to chatbot
                print("\nAssistant: ", end="")
                result = chatbot.send_message(user_input, streaming_callback=stream_to_console)
                
                print()  # New line after streaming response
                
                if not result.get("success"):
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            except KeyboardInterrupt:
                print("\n\nConversation interrupted.")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                logger.exception("Unexpected error in main loop")
    
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        logger.exception("Failed to initialize chatbot")
