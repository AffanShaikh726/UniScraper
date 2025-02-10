from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

jsonFormat = ""
# Method 1: Read entire file as string
with open("jsonFormat.txt", "r", encoding="utf-8") as file:
    jsonFormat = file.read()

def jsonifyDataAI(text) :
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
         messages=[
            {
                "role": "system",
                "content": "You are a JSON converter. Output only valid JSON without any additional text or formatting."
            },
            {
                "role": "user",
                "content": f"Convert to JSON object:\n{text} similar to {jsonFormat}" 
            }
        ]
    )
    
    return response.choices[0].message.content