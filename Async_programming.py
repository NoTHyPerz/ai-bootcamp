# # day2_async.py
# import asyncio
# import anthropic
# from dotenv import load_dotenv

# load_dotenv()
# client = anthropic.AsyncAnthropic()

# async def ask(question: str, label: str) -> str:
#     """Single async call with basic error handling."""
#     try:
#         message = await client.messages.create(
#             model="claude-haiku-4-5",  # cheaper for experiments
#             max_tokens=256,
#             messages=[{"role": "user", "content": question}]
#         )
#         return f"{label}: {message.content[0].text}"
#     except anthropic.APIError as e:
#         return f"{label}: ERROR — {e}"

# async def main():
#     # Make 5 calls SIMULTANEOUSLY — this is the power of async
#     questions = [
#         ("What is 15 * 23?", "Math"),
#         ("Capital of Japan?", "Geography"),
#         ("One word: Python or JavaScript?", "Opinion"),
#         ("What year did the web start?", "History"),
#         ("Define 'latency' in one sentence.", "Tech"),
#     ]
    
#     tasks = [ask(q, label) for q, label in questions]
#     results = await asyncio.gather(*tasks)
    
#     for r in results:
#         print(r)

# asyncio.run(main())


import asyncio 
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.AsyncAnthropic()

async def Geography(question):

    try:
        stream = await client.messages.create(
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="claude-haiku-4-5",
        stream=True,
    )
        print("Geography: ", end="")

        async for event in stream:
            if event.type == "content_block_delta":
                print(event.delta.text, end="", flush=True)

        print()

    except anthropic.APIError as e:
        print(f"ERROR — {e}")
        return

async def main():
    question = "Capital of Japan?"
    await Geography(question)

asyncio.run(main())
    
