import openai
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_pr(pr_data):
    # Prepare the prompt
    prompt = f"""
    Summarize this GitHub pull request:

    Title: {pr_data['title']}
    Description: {pr_data['body']}
    Files Changed:
    {''.join([f"\nFile: {f['filename']}\nPatch:\n{f['patch'][:1000]}" for f in pr_data['files']])}

    Summary:
    """

    try:
        # Make API request using GPT-3.5 model instead of GPT-4 (if you don't have GPT-4 access)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Switch to GPT-3.5 here
            messages=[
                {"role": "system", "content": "You are a senior software engineer reviewing a PR."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response["choices"][0]["message"]["content"]

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        raise Exception(f"An error occurred with the OpenAI API: {str(e)}")

    except Exception as e:
        # Handle other unexpected errors
        raise Exception(f"An error occurred: {str(e)}")
