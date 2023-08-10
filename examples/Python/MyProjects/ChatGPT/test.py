import os
import pathlib
import openai

# ChatGPT key
# KEY_FILE_PATH = pathlib.Path(os.path.expanduser("~")) / "code" / "ChatGPTKey.key"
KEY_FILE_PATH = pathlib.Path.home() / "code" / "ChatGPTKey.key"
assert os.path.exists(KEY_FILE_PATH), f"FATAL: key file path {KEY_FILE_PATH} does not exist!"
os.environ["OPENAI_API_KEY"] = open(KEY_FILE_PATH, "r").read().strip()


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    # get response from ChatGPT
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temparature=0,
    )
    return response


# print(get_completion("I love to learn something new"))
print(openai.Models().list())
