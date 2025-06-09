import tkinter as tk
from tkinter import scrolledtext, messagebox, font as tkFont
import asyncio
import threading
from dotenv import load_dotenv
import os
import argparse # For command-line arguments

# Attempt to import ChatAgent from the same directory
try:
    from chatagent import ChatAgent
except ImportError:
    messagebox.showerror("Import Error", "Could not import ChatAgent. Make sure chatagent.py is in the same directory.")
    exit(1)

def load_system_prompt_from_file(filepath: str) -> str | None:
    """Loads system prompt from a given filepath. Returns None if file not found or empty."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return content if content else None
        return None
    except Exception as e:
        print(f"Error loading system prompt from {filepath}: {e}")
        return None

class ChatApplication:
    def __init__(self, root, system_prompt_content: str | None):
        self.root = root
        root.title("Chat Agent")
        root.geometry("1024x768") # Set default window size
        root.configure(bg="#2E2E2E") # Dark background for the main window

        self.conversation_history = []

        # Define fonts and colors
        # Trying "Arial" to see if it renders more clearly than "Segoe UI" for the user
        self.font_main = tkFont.Font(family="Arial", size=14) 
        self.font_bold = tkFont.Font(family="Arial", size=14, weight="bold")
        self.color_bg_main = "#2E2E2E"
        self.color_bg_chat = "#3B3B3B"
        self.color_bg_input = "#4A4A4A"
        self.color_text_light = "#E0E0E0"
        self.color_text_user = "#81D4FA"  # Light blue for user text
        self.color_text_agent = "#A5D6A7" # Light green for agent text
        self.color_button = "#007ACC"
        self.color_button_fg = "#FFFFFF"
        # Button font can remain Segoe UI or be changed if Segoe UI is consistently blurry
        self.font_button = tkFont.Font(family="Segoe UI", size=12, weight="bold") 

        # Load .env file for API Key check - prioritize project root
        # Assumes chat_ui.py is in backend/chatbot/, so project root is ../../.env
        project_root_env = os.path.join(os.path.dirname(__file__), '.. ', '.. ', '.env')
        if os.path.exists(project_root_env):
            load_dotenv(dotenv_path=project_root_env, override=True)
        else:
            # Fallback to default (e.g., if .env is in current dir when running script)
            load_dotenv()

        # Check for API key before initializing agent (for early user feedback)
        if not os.getenv("ANTHROPIC_API_KEY"):
            messagebox.showerror("API Key Error", "ANTHROPIC_API_KEY not found. Please ensure it's set in your .env file at the project root.")
            root.destroy()
            return
        
        try:
            # Pass the loaded system_prompt_content to ChatAgent
            self.agent = ChatAgent(system_prompt=system_prompt_content)
        except Exception as e:
            messagebox.showerror("Agent Initialization Error", f"{str(e)}")
            root.destroy()
            return

        # Main frame
        main_frame = tk.Frame(root, bg=self.color_bg_main)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Chat history display
        self.chat_history_text = scrolledtext.ScrolledText(
            main_frame, 
            state='disabled', 
            wrap=tk.WORD, 
            height=15, 
            width=60,
            bg=self.color_bg_chat,
            fg=self.color_text_light,
            font=self.font_main, # Using Arial here
            relief=tk.FLAT,
            bd=5 # Border to make it look slightly inset
        )
        self.chat_history_text.pack(pady=(0,10), fill=tk.BOTH, expand=True)
        # Configure tags for user and agent messages
        self.chat_history_text.tag_configure("user_tag", foreground=self.color_text_user, font=self.font_main)
        self.chat_history_text.tag_configure("agent_tag", foreground=self.color_text_agent, font=self.font_main)
        self.chat_history_text.tag_configure("user_label", foreground=self.color_text_user, font=self.font_bold)
        self.chat_history_text.tag_configure("agent_label", foreground=self.color_text_agent, font=self.font_bold)

        # Input frame
        input_frame = tk.Frame(main_frame, bg=self.color_bg_main)
        input_frame.pack(fill=tk.X)

        # Message entry
        self.msg_entry = tk.Entry(
            input_frame, 
            width=50, 
            bg=self.color_bg_input, 
            fg=self.color_text_light, 
            font=self.font_main, # Using Arial here
            relief=tk.FLAT, 
            insertbackground=self.color_text_light, # Cursor color
            bd=5
        )
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0,10))
        self.msg_entry.bind("<Return>", self.send_message_event)

        # Send button
        self.send_button = tk.Button(
            input_frame, 
            text="➤", 
            command=self.send_message_event, 
            relief=tk.FLAT, 
            bg=self.color_button, 
            fg=self.color_button_fg, 
            font=self.font_button, # Using Segoe UI for button
            padx=15,
            pady=4,
            activebackground="#005f9e",
            activeforeground=self.color_button_fg
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Pass initial message without "Agent:" prefix, _display_message will add it.
        self._display_message("Hello! How can I help you today?", 'agent_initial')

    def _display_message(self, message, sender_type, is_initial=False):
        """Internal method to display messages in the UI only."""
        self.chat_history_text.config(state='normal')
        if sender_type == "user":
            self.chat_history_text.insert(tk.END, "You: ", "user_label")
            self.chat_history_text.insert(tk.END, message + "\n\n", "user_tag")
        elif sender_type == "agent" or sender_type == "agent_initial":
            self.chat_history_text.insert(tk.END, "Nice Touch: ", "agent_label")
            self.chat_history_text.insert(tk.END, message + "\n\n", "agent_tag")
            
        self.chat_history_text.see(tk.END)
        self.chat_history_text.config(state='disabled')

    def send_message_event(self, event=None):
        user_input = self.msg_entry.get()
        if not user_input.strip():
            return

        self._display_message(user_input, "user")
        self.conversation_history.append({"role": "user", "content": user_input})
        self.msg_entry.delete(0, tk.END)

        self.msg_entry.config(state='disabled')
        self.send_button.config(state='disabled', bg="#555555") # Dim button while disabled

        threading.Thread(target=self._get_agent_response, args=(user_input,), daemon=True).start()

    def _get_agent_response(self, user_input):
        # user_input is passed for context but the agent uses conversation_history now
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # Pass the full conversation history to the agent
            response_text = loop.run_until_complete(self.agent.process_user_request(user_input, conversation_history=self.conversation_history[:-1]))
            loop.close()
            
            self.conversation_history.append({"role": "assistant", "content": response_text})
            self.root.after(0, self._display_agent_ui_response, response_text)
        except Exception as e:
            error_message = f"Agent Error: {str(e)}"
            # Add a placeholder to history for the error, or decide how to handle
            # self.conversation_history.append({"role": "assistant", "content": error_message }) 
            self.root.after(0, self._display_agent_ui_response, error_message)

    def _display_agent_ui_response(self, response_text):
        self._display_message(response_text, 'agent')
        self.msg_entry.config(state='normal')
        self.send_button.config(state='normal', bg=self.color_button) # Restore button color
        self.msg_entry.focus_set()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat UI for Anthropic Agent")
    parser.add_argument("--prompt-file", type=str, help="Path to a file containing the system prompt.")
    args = parser.parse_args()

    system_prompt_content = None
    if args.prompt_file:
        prompt_filepath = os.path.abspath(args.prompt_file) # Ensure absolute path
        print(f"Attempting to load system prompt from command line file: {prompt_filepath}")
        system_prompt_content = load_system_prompt_from_file(prompt_filepath)
        if not system_prompt_content:
            print(f"Warning: Could not load or empty system prompt from {prompt_filepath}.")
    else:
        # Default prompt file path (in the same directory as chat_ui.py)
        default_prompt_filename = "default_system_prompt.txt"
        default_prompt_filepath = os.path.join(os.path.dirname(__file__), default_prompt_filename)
        print(f"Attempting to load default system prompt from: {default_prompt_filepath}")
        system_prompt_content = load_system_prompt_from_file(default_prompt_filepath)
        if not system_prompt_content:
            print(f"Warning: Could not load or empty default system prompt from {default_prompt_filepath}. ChatAgent will use its internal default.")

    root = tk.Tk()
    # Ensure the app object is stored so it's not garbage collected if __init__ returns early
    app = ChatApplication(root, system_prompt_content=system_prompt_content)
    if hasattr(app, 'agent') and app.agent: 
        root.mainloop()
    else:
        # If agent init failed, __init__ should have called root.destroy() or shown a messagebox.
        # If root wasn't destroyed, it might mean the app instance itself wasn't fully formed.
        if root.winfo_exists(): # Check if window still exists
             print("ChatApplication failed to initialize properly. Window might close or be unresponsive.")
        # No explicit root.mainloop() if agent setup failed and window was destroyed.