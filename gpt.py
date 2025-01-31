import os
import openai
import time
import keys

done = False
written = True
client = openai.AzureOpenAI(azure_endpoint=keys.azure_openai_endpoint,
                            api_key=keys.azure_openai_key,
                            api_version=keys.azure_openai_api_version)
discourse = [{"role": "system",
              "content":
              "You are a python-programming ide that only outputs valid python code based on user requests, nothing except code should be printed and no examples or markdown should be output, specifically ```python and ```"}]

def gpt(request):
    discourse.append({"role": "user", "content": request})
    chat = client.chat.completions.create(
        messages = discourse, model = "gpt-4")
    reply = chat.choices[0].message.content
    discourse.append({"role": "assistant", "content": reply})
    return reply

print(gpt("create a fibonacci function"))
while(1):
    print(gpt(input()))

