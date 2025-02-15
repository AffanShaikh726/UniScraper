from openAI import jsonifyDataAI

text = ""
# Method 1: Read entire file as string
with open("baseData.txt", "r", encoding="utf-8") as file:
    text = file.read()

print(jsonifyDataAI(text))