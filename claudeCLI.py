import os
from anthropic import Anthropic

API_KEY = os.environ['CLAUDE_API_KEY']

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
        
        conversation.append(f"Human: {user_input}")
        
        prompt = "\n".join(conversation) + "\nAssistant: "
        
        response = client.completion(
            prompt=prompt,
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0,
        )
        
        assistant_response = response["completion"]
        print(f"Assistant: {assistant_response}")
        
        conversation.append(f"Assistant: {assistant_response}")

if __name__ == '__main__':
    main()