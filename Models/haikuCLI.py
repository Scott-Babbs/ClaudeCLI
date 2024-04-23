import os
import time
import threading
from anthropic import Anthropic

API_KEY = os.environ['CLAUDE_API_KEY']

def display_loading_indicator(stop_event):
    while not stop_event.is_set():
        for _ in range(3):
            if stop_event.is_set():
                break
            print(".", end="", flush=True)
            time.sleep(0.5)
        print("\r   \r", end="", flush=True)

def main():
    client = Anthropic(api_key=API_KEY)
    
    print("Welcome to Scotts claudeCLI!")
    print("Type 'quit' to exit the conversation.")
    
    conversation = []
    
    while True:
        user_input = input("You: ")
        
        if user_input.strip().lower() == 'quit':
            print("Goodbye!")
            break
        
        conversation.append({"role": "user", "content": user_input})
        
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=display_loading_indicator, args=(stop_event,))
        loading_thread.start()
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            messages=conversation,
            max_tokens=1024,
        )
        
        stop_event.set()
        loading_thread.join()
        print("\r   \r", end="", flush=True)
        
        assistant_response = response.content
        
        if isinstance(assistant_response, list):
            text_content = "\n".join(item.text.strip() for item in assistant_response)
        else:
            text_content = assistant_response.text.strip()
        
        print(f"Assistant: {text_content}")
        
        conversation.append({"role": "assistant", "content": text_content})

if __name__ == '__main__':
    main()