# main.py

from openai import OpenAI
import json
import requests
import re

# Create instructions for chatbot
INSTRUCTIONS = ("Your job is to assist the user in finding a suitable internship."
                "Assume they are a university student studying computer science."
                "Use the information provided in the json string to find an appropriate job."
                "The chat history is provided to you."
                "Use the json string provided to give recommendations."
                "If the user asks you for more information, "
                "simply respond ONLY with the link to that application and no other text."
                "If no further information can be found from the webpage, tell that to the user."
                "If it can, suggest the extra information it provides.")

# Use API Key to access GPT API
client = OpenAI(api_key="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")

# Import data from json file
with open('data.json', 'r') as file:
    data = json.load(file)

data_string = json.dumps(data)

# Create chatbot function
def chat_with_gpt(history, new_prompt):

    # Create messages array
    messages = [
        {"role": "system", "content": INSTRUCTIONS},
        {"role": "system", "content": data_string},
    ]

    # Provide conversation history
    for prompt, response in history:
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "assistant", "content": response})

    # Add new question
    messages.append({"role": "user", "content": new_prompt})
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    if completion.choices[0].message.content.strip().startswith("["):
        url_prompt = completion.choices[0].message.content.strip()

        # Regular expression to find URLs in Markdown links
        url_pattern = r'\]\((.*?)\)'
        match = re.search(url_pattern, url_prompt)

        if match:
            url = match.group(1)
        webpage = requests.get(url)
        chat_with_gpt(history, webpage)

    # Return new response
    return completion.choices[0].message.content.strip()

if __name__ == "__main__":

    # Create array of previous prompts and responses
    history = []

    introduction = chat_with_gpt(history, "Introduce yourself and your purpose to me given your instructions.")
    print("Chatbot: ", introduction)

    while True:
        prompt = input("You: ")
        if prompt.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gpt(history, prompt)
        print("Chatbot: ", response)

        history.append((prompt, response))