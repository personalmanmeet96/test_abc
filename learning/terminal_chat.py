import openai
import sys
import time

# Configure the OpenAI client to point to LM Studio's local server
client = openai.OpenAI(
    base_url="http://localhost:1234/v1",  # Default LM Studio API endpoint
    api_key="lm-studio"  # Dummy API key (LM Studio doesn't require a real one)
)

# Function to get a streaming response from the LLM
def get_llm_streaming_response(messages):
    try:
        stream = client.chat.completions.create(
            model="local-model",  # Placeholder for the loaded model
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=True  # Enable streaming
        )
        return stream
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

# Function to print the streaming response with a typewriter effect
def print_streaming_response(stream):
    full_response = ""
    print("Assistant: ", end="", flush=True)
    
    if stream is None:
        print("Sorry, I encountered an error.")
        return ""
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            print(content, end="", flush=True)
            # Optional: Add a slight delay for typewriter effect (adjust as needed)
            time.sleep(0.02)
    
    print()  # Newline after the response
    return full_response

# Main chat loop with streaming
def chat_interface():
    print("=== Terminal Chat Interface (Streaming) ===")
    print("Type 'exit' to quit.\n")
    
    # Initialize conversation history
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        # Get and print streaming LLM response
        stream = get_llm_streaming_response(messages)
        assistant_response = print_streaming_response(stream)
        
        # Add assistant response to history
        if assistant_response:
            messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    try:
        chat_interface()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Goodbye!")