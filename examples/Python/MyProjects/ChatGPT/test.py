import os
import pathlib
import openai

# ChatGPT key
# KEY_FILE_PATH = pathlib.Path(os.path.expanduser("~")) / "code" / "ChatGPTKey.key"
KEY_FILE_PATH = pathlib.Path.home() / "code" / "ChatGPTKey.key"
assert os.path.exists(KEY_FILE_PATH), f"FATAL: key file path {KEY_FILE_PATH} does not exist!"
# os.environ["OPENAI_API_KEY"] = open(KEY_FILE_PATH, "r").read().strip()
openai.api_key = open(KEY_FILE_PATH, "r").read().strip()


def get_completion(prompt, max_tokens=64, outputs=3, model="text-davinci-003"):
    messages = [{"role": "user", "content": prompt}]
    # get response from ChatGPT
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=outputs,
    )
    output = list()
    for k in response["choices"]:
        output.append(k["text"].strip())
    return output


# print(get_completion("I love to learn something new"))
print(get_completion("Give me a plan to learn Python"))
