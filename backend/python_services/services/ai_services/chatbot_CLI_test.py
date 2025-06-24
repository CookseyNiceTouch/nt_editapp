#!/usr/bin/env python3
"""
CLI Test Interface for AI Video Editing Chatbot

This script provides a command-line interface to test the chatbot functionality
before integrating it with the FastAPI layer.

Usage:
    python chatbot_CLI_test.py
    or
    uv run chatbot_CLI_test.py
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any

# Handle imports that work both when run directly and as a module
try:
    # Try relative imports first (when run as module)
    from .chatbot_backend import ChatbotBackend, stream_to_console
except ImportError:
    # Fall back to absolute imports (when run directly)
    from chatbot_backend import ChatbotBackend, stream_to_console

def print_banner():
    """Print the CLI chatbot banner."""
    print("=" * 60)
    print("🎬 AI VIDEO EDITING CHATBOT - CLI TEST INTERFACE 🎬")
    print("=" * 60)
    print("This is a test interface for the video editing chatbot.")
    print("You can interact with the AI assistant to get help with:")
    print("• Video editing workflows and concepts")
    print("• DaVinci Resolve automation and integration")
    print("• Timeline analysis and generation")
    print("• Project management and best practices")
    print("• Technical troubleshooting")
    print()

def print_commands():
    """Print available commands."""
    print("Available Commands:")
    print("  help         - Show this help message")
    print("  quit/exit    - Exit the chatbot")
    print("  clear        - Start a new conversation")
    print("  history      - Show conversation summary")
    print("  tools        - List available tools")
    print("  test-tool <name> - Test a specific tool manually")
    print("  toggle-tools - Enable/disable tool usage")
    print("  status       - Show chatbot status")
    print("  project      - Show current project information")
    print("  restart      - Restart the chatbot with a fresh instance")
    print()

def print_status(chatbot: ChatbotBackend):
    """Print current chatbot status."""
    summary = chatbot.get_conversation_summary()
    print(f"📊 Chatbot Status:")
    print(f"  • Conversation ID: {summary['conversation_id']}")
    print(f"  • Messages exchanged: {summary['message_count']}")
    print(f"  • Tools enabled: {'✓' if chatbot.enable_tools else '✗'}")
    print(f"  • Project loaded: {'✓' if chatbot.project_data else '✗'}")
    if chatbot.project_data:
        print(f"  • Project title: {chatbot.project_data.get('title', 'Unknown')}")
    print()

def print_project_info(chatbot: ChatbotBackend):
    """Print current project information."""
    if not chatbot.project_data:
        print("❌ No project data loaded")
        return
    
    print(f"📁 Current Project Information:")
    print(f"  • Title: {chatbot.project_data.get('title', 'Unknown')}")
    print(f"  • Brief length: {len(chatbot.project_data.get('brief', ''))} characters")
    
    # Show a preview of the brief
    brief = chatbot.project_data.get('brief', '')
    if brief:
        brief_preview = brief[:200] + "..." if len(brief) > 200 else brief
        print(f"  • Brief preview: {brief_preview}")
    print()

def enhanced_streaming_callback(stream_type: str, content: str):
    """Enhanced streaming callback with better formatting and indicators."""
    if stream_type == "thinking":
        # For thinking content, print in dim gray with thinking indicator
        print(f"\033[2;37m💭 {content}\033[0m", end="", flush=True)
    elif stream_type == "tool":
        # For tool usage, print in bright cyan with tool indicator
        print(f"\033[96m🔧 {content}\033[0m", flush=True)
    elif stream_type == "response":
        # For response content, print in normal color with response indicator
        if content.strip():  # Only print non-empty content
            print(f"{content}", end="", flush=True)

def test_tool_interactive(chatbot: ChatbotBackend):
    """Interactive tool testing interface."""
    tools = chatbot.list_available_tools()
    
    if not tools:
        print("❌ No tools available")
        return
    
    print(f"\n🔧 Available Tools ({len(tools)}):")
    for i, tool in enumerate(tools, 1):
        category = tool.get('category', 'unknown')
        print(f"  {i:2d}. {tool['name']} ({category})")
        print(f"      {tool['description']}")
    
    print("\nEnter tool number or name (or 'back' to return):")
    
    while True:
        try:
            choice = input("Tool> ").strip()
            
            if choice.lower() in ['back', 'exit', 'quit']:
                break
            
            # Try to parse as number
            try:
                tool_index = int(choice) - 1
                if 0 <= tool_index < len(tools):
                    tool_name = tools[tool_index]['name']
                else:
                    print(f"❌ Invalid tool number. Choose 1-{len(tools)}")
                    continue
            except ValueError:
                # Treat as tool name
                tool_name = choice
                if tool_name not in [t['name'] for t in tools]:
                    print(f"❌ Tool '{tool_name}' not found")
                    continue
            
            # Test the tool
            print(f"\n🧪 Testing tool: {tool_name}")
            print("-" * 40)
            
            result = chatbot.call_tool_manually(tool_name)
            
            if result.get("success"):
                print("✅ Tool executed successfully!")
                print(f"Result: {json.dumps(result.get('result'), indent=2)}")
            else:
                print(f"❌ Tool failed: {result.get('error')}")
            
            print("-" * 40)
            print("Test another tool? (Enter tool number/name or 'back' to return)")
            
        except KeyboardInterrupt:
            print("\n🔙 Returning to main interface...")
            break
        except Exception as e:
            print(f"❌ Error during tool testing: {e}")

def main():
    """Main CLI interface function."""
    print_banner()
    
    try:
        # Initialize chatbot
        print("🚀 Initializing chatbot...")
        chatbot = ChatbotBackend()
        print("✅ Chatbot initialized successfully!")
        
        # Show welcome message
        print("\n" + "🤖 " + chatbot.get_welcome_message())
        print()
        
        print_commands()
        print("Type your message or a command to get started!")
        print("=" * 60)
        
        # Main interaction loop
        while True:
            try:
                # Get user input with a nice prompt
                user_input = input("\n💬 You: ").strip()
                
                # Handle empty input
                if not user_input:
                    print("💡 Please enter a message or command. Type 'help' for available commands.")
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for testing the chatbot! Goodbye!")
                    break
                
                elif user_input.lower() == 'help':
                    print_commands()
                    continue
                
                elif user_input.lower() == 'clear':
                    chatbot.clear_conversation()
                    print("🗑️  Conversation cleared. Starting fresh!")
                    print("\n" + "🤖 " + chatbot.get_welcome_message())
                    continue
                
                elif user_input.lower() == 'history':
                    summary = chatbot.get_conversation_summary()
                    print(f"\n📊 Conversation Summary:")
                    print(f"  • ID: {summary['conversation_id']}")
                    print(f"  • Messages: {summary['message_count']}")
                    print(f"  • Created: {summary['created_at'] or 'Just now'}")
                    print(f"  • Last message: {summary['last_message_at'] or 'None'}")
                    continue
                
                elif user_input.lower() == 'tools':
                    tools = chatbot.list_available_tools()
                    print(f"\n🔧 Available Tools ({len(tools)}):")
                    for tool in tools:
                        category = tool.get('category', 'unknown')
                        print(f"  • {tool['name']} ({category}): {tool['description']}")
                    continue
                
                elif user_input.lower().startswith('test-tool'):
                    # Handle both "test-tool" and "test-tool toolname"
                    parts = user_input.split(None, 1)
                    if len(parts) > 1:
                        tool_name = parts[1].strip()
                        print(f"\n🧪 Testing tool: {tool_name}")
                        result = chatbot.call_tool_manually(tool_name)
                        if result.get("success"):
                            print("✅ Tool succeeded:")
                            print(json.dumps(result.get("result"), indent=2))
                        else:
                            print(f"❌ Tool failed: {result.get('error')}")
                    else:
                        # Interactive tool testing
                        test_tool_interactive(chatbot)
                    continue
                
                elif user_input.lower() == 'toggle-tools':
                    chatbot.enable_tools = not chatbot.enable_tools
                    status = "enabled" if chatbot.enable_tools else "disabled"
                    print(f"🔧 Tools are now {status}")
                    continue
                
                elif user_input.lower() == 'status':
                    print_status(chatbot)
                    continue
                
                elif user_input.lower() == 'project':
                    print_project_info(chatbot)
                    continue
                
                elif user_input.lower() == 'restart':
                    print("🔄 Restarting chatbot...")
                    chatbot = ChatbotBackend()
                    print("✅ Chatbot restarted successfully!")
                    print("\n" + "🤖 " + chatbot.get_welcome_message())
                    continue
                
                # Send message to chatbot
                print("\n🤖 Assistant: ", end="", flush=True)
                
                start_time = time.time()
                result = chatbot.send_message(user_input, streaming_callback=enhanced_streaming_callback)
                end_time = time.time()
                
                print()  # New line after streaming response
                
                # Show response metadata
                if result.get("success"):
                    response_time = end_time - start_time
                    tool_count = len(result.get("tool_calls", []))
                    
                    print(f"\n💡 Response completed in {response_time:.1f}s", end="")
                    if tool_count > 0:
                        print(f" (used {tool_count} tools)", end="")
                    print()
                    
                    # Show tool calls summary if any
                    if tool_count > 0:
                        print("🔧 Tools used:")
                        for tool_call in result.get("tool_calls", []):
                            tool_name = tool_call.get("tool_name", "unknown")
                            success = tool_call.get("result", {}).get("success", False)
                            status = "✅" if success else "❌"
                            print(f"  {status} {tool_name}")
                else:
                    print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            
            except KeyboardInterrupt:
                print("\n\n🛑 Conversation interrupted. Type 'quit' to exit or continue chatting.")
                continue
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("💡 Type 'restart' to reinitialize the chatbot or 'quit' to exit.")
                continue
    
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        print("\nPossible issues:")
        print("• Check that your .env file contains the claude_api_key")
        print("• Ensure all required dependencies are installed")
        print("• Verify the project structure and file paths")
        sys.exit(1)

if __name__ == "__main__":
    main()
