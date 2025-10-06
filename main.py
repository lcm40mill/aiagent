import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types




def main():
    load_dotenv()
    
    args = sys.argv[1:]

    if not args:
        print("AI Assistant Error")
        print('\nUsage: python main.py "your prompt here."')
        print('\nExample: python main.py "Did it work?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    messages=[
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    generate_content(client, messages)

def generate_content(client, messages):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages
    )
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response: ")
    print(response.text)

if __name__ == "__main__":
    main()
