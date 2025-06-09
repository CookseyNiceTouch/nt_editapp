import anthropic
import os
from dotenv import load_dotenv

# Load .env file from the project root (expected to be two levels up from this script)
# or from the current working directory as a fallback.
project_root_env = os.path.join(os.path.dirname(__file__), '.. ', '.. ', '.env')

if os.path.exists(project_root_env):
    load_dotenv(dotenv_path=project_root_env, override=True)
    # print(f"[DEBUG] Loaded .env from: {project_root_env}") # Optional: for confirmation
else:
    # Fallback to default behavior (checks current dir, or if .env is in a parent handled by python-dotenv default)
    load_dotenv()
    # print("[DEBUG] Loaded .env using default load_dotenv() behavior (e.g., current directory or auto-detect).")

class ChatAgent:
    def __init__(self, system_prompt: str = None):
        """
        Initializes the ChatAgent.
        The Anthropic API key is loaded from the ANTHROPIC_API_KEY environment variable.
        This agent interacts with the user to understand their needs and context,
        then triggers processes provided by other parts of the project.

        Args:
            system_prompt (str, optional): A system prompt to guide the agent's behavior.
                                           Defaults to a generic prompt if None.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Make sure it's set in your .env file.")
        self.client = anthropic.Anthropic(api_key=api_key)
        
        if system_prompt is None:
            self.system_prompt = (
                "You are ChatAgent, a helpful AI assistant for a video editing application. "
                "Your primary role is to understand the user's needs and what they want to achieve with their video project. "
                "You do not perform video editing tasks yourself. Instead, you clarify requirements, "
                "understand context, and then determine the appropriate next steps, which might involve passing instructions to other specialized agents or tools. "
                "Be clear, concise, and ask clarifying questions if the user's request is ambiguous. "
                "Do not offer to perform the tasks yourself. Explain that you will initiate the process."
            )
        else:
            self.system_prompt = system_prompt

    async def process_user_request(self, user_query: str, conversation_history: list = None) -> str:
        """
        Processes the user's query to understand their intent and returns a response.
        This will involve interacting with the Anthropic API.
        Further development will involve triggering other project components based on the intent.

        Args:
            user_query (str): The user's current query.
            conversation_history (list, optional): A list of previous user/assistant turns.
                                                 Each turn should be a dict like {"role": "user"/"assistant", "content": ...}.
                                                 Defaults to None for no history.
        """
        if not user_query:
            return "I need a query to process."

        # Construct messages for the API call (user and assistant turns only)
        api_messages = []
        if conversation_history:
            api_messages.extend(conversation_history)
        api_messages.append({"role": "user", "content": user_query})

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229", 
                max_tokens=1500,
                system=self.system_prompt,  # System prompt passed as a top-level parameter
                messages=api_messages      # Only user and assistant messages in this list
            )
            
            if response.content and isinstance(response.content, list) and len(response.content) > 0:
                return response.content[0].text
            return "Sorry, I received an unexpected response structure."
        except Exception as e:
            return f"An error occurred while communicating with the AI: {e}"

# Example usage (optional, for testing)
if __name__ == '__main__':
    import asyncio

    # Ensure your .env file is in the project root (C:/Users/simon/Development/nt_editapp/.env)
    # or accessible by default load_dotenv() from CWD when running this script directly.
    
    custom_system_prompt = (
        "You are a specialized assistant for understanding video editing commands. "
        "Your goal is to break down user requests into actionable steps for a video editing pipeline. "
        "Do not perform the edits, just identify the tasks."
    )
    # agent = ChatAgent(system_prompt=custom_system_prompt) # Example with custom prompt
    agent = ChatAgent() # Uses default system prompt

    async def main():
        print("ChatAgent direct test mode. Type 'quit' to exit.")
        history = [] # This will store dicts: {"role": "user"/"assistant", "content": ...}
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            
            if not user_input.strip():
                continue
            
            print("Agent thinking...")
            # Pass the current history. The new user_input will be appended inside process_user_request logic for the API call.
            agent_response = await agent.process_user_request(user_input, conversation_history=history)
            print(f"Agent: {agent_response}")
            
            # Add user input and agent response to history for the next turn
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": agent_response})

    if agent:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nExiting ChatAgent test.")
        except Exception as e:
            print(f"An error occurred during asyncio.run(main()): {e}")
