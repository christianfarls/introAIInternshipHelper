# main.py

from openai import OpenAI
from bs4 import BeautifulSoup
import json
import requests
import time

# Create instructions for chatbot
INSTRUCTIONS = ("Your job is to assist the user in finding a suitable internship."
                "Assume they are a university student studying computer science."
                "Use the information provided in the json string to find an appropriate job."
                "The chat history is provided to you."
                "Use the json string provided to give recommendations."
                "If the user asks you for more information, "
                "tell them to paste the link, starting with 'https'."
                "Start the conversation by asking some general information about the user,"
                "given the categories in the json.")

# Use API Key to access GPT API
client = OpenAI(api_key="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")

# Import data from json file
with open('data.json', 'r') as file:
    data = json.load(file)

data_string = json.dumps(data)

def fetch_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Test for failed HTTP request
        return response.text
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    return None

def parse_webpage(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = ""

    # Collect all text from webpage
    for paragraph in soup.find_all('p'):
        text += paragraph.get_text() + "\n"

    return text

# Separating the api call to allow for rate limiting
def call_openai_api(messages, max_retries=3, delay=10):
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return completion
        except openai.RateLimitError as e:
            wait_time = e.response.json()['error'].get('retry_after', delay)
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return None


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

    # Feed chatbot website data
    if new_prompt.startswith("http"):
        url = new_prompt

        # Process and return info
        webpage_content = parse_webpage(fetch_webpage(url))
        if webpage_content != "":
            new_prompt = "Use this data for further responses: " + webpage_content
        else:
            new_prompt = ("Provide the user the link again and tell them that you"
                          "do not have the permissions to extract it.")

    # Add new question
    messages.append({"role": "user", "content": new_prompt})
    completion = call_openai_api(messages)

    if completion is None:
        return "Unable to process your request at this time due to API limits."

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