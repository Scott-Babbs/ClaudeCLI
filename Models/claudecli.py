import os
import time
import threading
import argparse
from anthropic import Anthropic

API_KEY = os.environ['CLAUDE_API_KEY']

parser = argparse.ArgumentParser(description="Scotts claudeCLI")
model_group = parser.add_mutually_exclusive_group()
model_group.add_argument("-s", "--sonnet", action="store_true", help="Use the Sonnet model")
model_group.add_argument("-o", "--opus", action="store_true", help="Use the Opus model")
model_group.add_argument("-k", "--haiku", action="store_true", help="Use the Haiku model")
parser.add_argument("question", nargs="*", help="The question to ask the model")
args = parser.parse_args()

# defaults to haiku if no flag is provided
if args.sonnet:
    MODEL = "claude-3-sonnet-20240229"
elif args.opus:
    MODEL = "claude-3-opus-20240229"
else:
    MODEL = "claude-3-haiku-20240307"

def display_loading_indicator(stop_event):
    while not stop_event.is_set():
        print("thinking", end="", flush=True)
        for _ in range(3):
            if stop_event.is_set():
                break
            print(".", end="", flush=True)
            time.sleep(0.5)
        print("\r       \r", end="", flush=True)

def main():
    client = Anthropic(api_key=API_KEY)
    
    print(f"Welcome to claudeCLI. You are using the {MODEL} model.")
    
    if args.question:
        question = " ".join(args.question)
        conversation = [{"role": "user", "content": question}]
        
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=display_loading_indicator, args=(stop_event,))
        loading_thread.start()
        
        response = client.messages.create(
            model=MODEL,
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
    else:
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
                model=MODEL,
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
