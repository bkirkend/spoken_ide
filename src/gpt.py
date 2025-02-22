import openai
import src.keys as keys

client = openai.AzureOpenAI(azure_endpoint=keys.azure_openai_endpoint,
                            api_key=keys.azure_openai_key,
                            api_version=keys.azure_openai_api_version)
discourse = [{"role": "system",
              "content":
              "You are a python-programming ide that only outputs valid python code based on user requests, nothing except code should be printed and no examples or markdown should be output, specifically ```python and ```. Your job is to create a single string input string output function. Helper functions are permitted."}]

def gpt(request):
    discourse.append({"role": "user", "content": request})
    chat = client.chat.completions.create(
        messages = discourse, model = "gpt-4")
    reply = chat.choices[0].message.content
    discourse.append({"role": "assistant", "content": reply})
    return reply

def clear_discourse():
    global discourse
    discourse = [{"role": "system",
                  "content":
                  "You are a python-programming ide that only outputs valid python code based on user requests, nothing except code should be printed and no examples or markdown should be output, specifically ```python and ```"}]


# def __main__():
#     print(gpt(input("write a function prompt: ")))
#     while(1):
#         print(gpt(input()))

# if __name__ == "__main__":
#     __main__()

