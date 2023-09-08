import sys, random
from transformers import pipeline
from datasets import load_dataset

random.seed(41)

# create a sentiment analysis pipeline
pipeline = pipeline("sentiment-analysis")

# load the dataset
dataset = load_dataset("imdb")

# print the 5th test sample
sample = dataset["test"][4]
print(f"{sample}")
sys.exit(-1)

# get a random review
index = 45  # random.randint(0, len(dataset["train"]))
review = dataset["train"][index]["text"]

# get the sentiment of the review
sentiment = pipeline(review)[0]

print(f"{review} -> {sentiment}")
