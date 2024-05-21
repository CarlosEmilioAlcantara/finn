import random
import json
import torch
from model import NeuralNet
from main import bag_of_words, tokenize

# Getting data from flask
import sys
sys.path.append(r'D:\agqxyz\Documents\School\ITEP203-1 AnalysisAndDesignOfAlgo\Python\financial-adviser\flask')

import app

# If GPU usable then use for processing
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Loading the json file as an associative array
with open(r'D:\agqxyz\Documents\School\ITEP203-1 AnalysisAndDesignOfAlgo\Python\final-out\intents.json', 'r') as f:
    intents = json.load(f)

FILE = r"D:\agqxyz\Documents\School\ITEP203-1 AnalysisAndDesignOfAlgo\Python\financial-adviser\ai\training-data\data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Yukari Takeba"
# print("I love you! Type 'stupei' to exit")

# while True: 
# sentence = str(app.sentence)

# sentence = tokenize(sentence)
# x = bag_of_words(sentence, all_words)
# x = x.reshape(1, x.shape[0])
# x = torch.from_numpy(x).to(device)

# output = model(x)
# _, predicted = torch.max(output, dim=1)
# tag = tags[predicted.item()]

# probs = torch.softmax(output, dim=1)
# prob = probs[0][predicted.item()]

# if prob.item() > 0.75:
#     for intent in intents["intents"]:
#         if tag == intent["tag"]:
#             answer = (f"{bot_name}: {random.choice(intent['responses'])}")
# else:
#     answer = (f"{bot_name}: I do not understand...")