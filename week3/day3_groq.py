from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[ {"role": "system", "content": "you are a rude and sarcastic assistant who gives very short answers and complains about everything."},
{"role": "user", "content": "Hi, what can you help me with?"}])

print(response.choices[0].message.content)
