# main.py

from openai import OpenAI
import json

# Create instructions for chatbot
INSTRUCTIONS = ("Your job is to assist the user in finding a suitable internship."
                "Assume they are a university student studying computer science."
                "Use the information provided in the json file to find an appropriate job."
                "The chat history is provided to you."
                "Use the json string provided to give recommendations.")

# Use API Key to access GPT API
client = OpenAI(api_key="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")

# Import data from json file
with open('data.json', 'r') as file:
    data = json.load(file)


# Create chatbot function
def chat_with_gpt(instructions, history, new_prompt):

    # Create messages array
    messages = [
        {"role": "system", "content": instructions},
    ]

    # Provide conversation history
    for prompt, response in history:
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": response})

    # Add new question
    messages.append({"role": "user", "content": new_prompt})
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    # Return new response
    return completion.choices[0].message.content.strip()


setup_prompt = ()

if __name__ == "__main__":
    setup = chat_with_gpt(setup_prompt)
    print(setup)
    next_step = chat_with_gpt(json.dumps(data))
    print(next_step)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        mess

        response = chat_with_gpt(user_input)
        print("Chatbot: ", response)