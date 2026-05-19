# day1_basics.py
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

# Exercise 1: Basic call
message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain what an API is in 3 sentences."}]
)
print(message.content[0].text)

# Exercise 2: Streaming (way more satisfying)
with client.messages.stream(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a haiku about Python."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()