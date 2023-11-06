import { Configuration, OpenAIApi } from "openai";

const configuration = new Configuration({
    organization: "org-GTsflkUjqjf16n4XV3uimJ5p",
    apiKey: "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",
});

const openai = new OpenAIApi(configuration);

const completion = await openai.createChatCompletion({
    model: "gpt-3.5-turbo",
    messages: [
        {role: "user", content: "Hello World"},
    ]
})

console.log(completion.data.choices[0].message);