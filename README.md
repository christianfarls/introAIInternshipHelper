# Introduction to AI (CSE 30124) Final Project - Internship Finder Assistant
*by Christian Farls*

## Welcome
This project was designed as an effective implementation of the GPT API as a chat assistant with the goal of helping university students find internship opportunities that suit their interests. Throughout the process, the model ended up staying true to the originally proposed concept. As I had had no experience using this API in the past, this was a completely new experience that I, honestly, thoroughly enjoyed. Extensive documentation and a sharpening of Python skills have led to this final product.

The instructions given to setup the chatbot are as follows:
> "Your job is to assist the user in finding a suitable internship.
> Assume they are a university student studying computer science.
> Use the information provided in the json string to find an appropriate job.
> The chat history is provided to you.
> Use the json string provided to give recommendations.
> If the user asks you for more information, tell them to paste the link, starting with 'https'.
> Start the conversation by asking some general information about the user, given the categories in the json."

## How to Run
Since I have a Mac, I will provide instructions in this format.

**Step 1 - Clone the repository**
Simply type the following command into your terminal to access the project directory:

```git clone https://github.com/christianfarls/introAIInternshipHelper.git```

**Step 2 - Run the program**
If you have python3 installed on your system, then a simple command like this will get the chatbot up and running:

```python3 main.py```

You may have to wait a few seconds once it first starts to run, though, as the LLM must comprehend the instructions and the provided json data.

**Step 3 - Chat!**
The chatbot should provide you with an introduction, as well as suggestions on what information to provide it in order to get the best results.

**Step 4 - Tips**
Once provided an opportunity, simply prompt the bot with the link to the application and **no other text**. If the webpage is accessible through an HTTP GET request, the LLM will scrape the webpage for more information to that specific opportunity. All webpage information was not initially provided to the chatbot in an attempt to improve performance as well as keep tokenization cost to a minimum. If the webpage cannot be accessed, the assistant will let you know and suggest that the user manually visit the webpage.

## Data
The provided data is in a json format with five keys:
- Company
- Role
- Location
- Application Link
- Date Posted

These have been manually scraped and formatted from the following repository:
[Summer2024-Internships](https://github.com/SimplifyJobs/Summer2024-Internships/blob/dev/README.md)

As mentioned in the Tips above, the chatbot has limited functionality in performing its own web scraping.

## Tokenization
One of the most interesting parts about this project was learning more about tokens and tokenization, aka how these LLMs even process natural language. When I first accessed the OpenAI website to snag my API key, I noticed that this wasn't just free to use--I was going to have to pay a price...literally. They offer a cool resource to calculate prompt tokens, so I played around with it in order to better understand how to overcome this obstacle. Since the LLM cannot scrape its own data, I was going to have to feed it all the information I had obtained in order to provide accurate and up-to-date results. If I prompted the assistant with every internship opportunity (practically the data repo I used), it would have cost a significant amount of money each time I ran the program. Instead, I only filtered the first good few diverse opportunities to test the LLM's capabilities in providing valuable info. I also opted to use the GPT-4 model (rather than 3.5) to provide a better experience for the user. While each token does have a higher cost, I think it was worth it.

This all being said, if you happen to get an error when providing a webpage for the model to scrape, it is probably due to the prompt exceeding the appropriate number of tokens-per-minute (TPM) (which counts both prompts **and** responses) or my personal funds being used up (I have like $20 of credits and only 6 have been used through my extensive testing so, when running the bot on your own, you shouldn't hit this latter issue). I only ran into the TPM limit problem a few times when trying to feed the LLM an entire webpage but have since incorporated error handling. Feel free to Slack/email me if you're having trouble, though.

## Reflection
While the program isn't too extensive, it took a while to get to this point--trust me, debugging this project was way more of a pain than expected. The first major issue I ran into was maintaining chat history. Unlike the web version of ChatGPT, the API does not remember previous prompts and responses UNLESS PROVIDED TO IT EACH TIME. This is why I continue to populate a 'messages' array with the chat information and pass it to the model each time. It's great at processing language, but token cost also increases when you have to feed the entire chat to the bot as it grows larger. This was the only effective way to keep a conversation flowing as well as force the model to consistently refer to the json data. Without a continuous reminder of the chat log, the model would forget the json data existed each time I tried to ask it to provide me info. This is another reason why the data set was truncated.

Web scraping also posed to be a much larger problem than anticipated. When I learned about 'curl' in Prof. Bui's Systems class, I thought that every webpage could just be accessed this way. I was wrong. I was so wrong. While I wish all websites were just open to giving their HTML data to anyone with Python and the 'requests' library, I had to work around this roadblock with error handling. If you'd like to test my web scraping implementation, ask the bot to provide opportunities at Okta and paste one of their application links; through my testing, I recognized that these webpages can be accessed and the bot provides pretty valuable info.

## Future Implementations
With the new GPT Vision (which can analyze photos and documents), I would love to be able to have the user submit a resumé to see if the LLM can match positions either based on distance to the user's hometown, based on previous experience, or other factors such as GPA/year of education. As you could probably guess, though, the token cost for THIS service is so much higher, so I didn't really attempt to use this model.

## Conclusion
I had a lot of fun with this project. While I didn't use any crazy linear algebra or intense search techniques, a general understanding of LLMs and their approach to processing natural language has allowed me to easily draw connections between these concepts we've studied in class and real AI. I would not be surprised if I revisit this project over winter break to add more to it--I want to be able to host it on my portfolio website that I'm currently building, but I know that this would take a lot more work re: building a frontend and all