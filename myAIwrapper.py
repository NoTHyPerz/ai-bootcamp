# day4_retry.py
import asyncio
import anthropic
import time
from dotenv import load_dotenv

load_dotenv()

class RobustAIClient:
    """An LLM client that handles failures gracefully."""
    
    def __init__(self, max_retries=3, base_delay=1.0):
        self.client = anthropic.Anthropic()
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def call(self, prompt: str, model="claude-haiku-4-5", max_tokens=512) -> str:
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                message = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
                
            except anthropic.RateLimitError:
                wait = self.base_delay * (2 ** attempt)  # 1s, 2s, 4s
                print(f"Rate limited. Waiting {wait}s before retry {attempt+1}...")
                time.sleep(wait)
                last_error = "rate_limit"
                
            except anthropic.APITimeoutError:
                wait = self.base_delay * (2 ** attempt)
                print(f"Timeout. Retrying in {wait}s...")
                time.sleep(wait)
                last_error = "timeout"
                
            except anthropic.APIError as e:
                # Don't retry on 4xx client errors — they won't fix themselves
                if 400 <= e.status_code < 500:
                    raise
                wait = self.base_delay * (2 ** attempt)
                time.sleep(wait)
                last_error = str(e)
        
        raise RuntimeError(f"Failed after {self.max_retries} attempts. Last error: {last_error}")

# Test it
client = RobustAIClient()
response = client.call("What's the capital of France?")
print(response)










#  Building my own wrapper around the anthropic client to handle retries and errors gracefully. (Doing Myself to learn better)

# import anthropic
# from dotenv import load_dotenv
# import time


# load_dotenv()

# class MyAIWrapper:

#     def __init__(self,max_retries=3, base_delay=1.0):
#         self.client = anthropic.Anthropic()
#         self.max_retries = max_retries
#         self.base_delay = base_delay

#     def call (self, prompt : str, model: str, max_tokens=512) -> str:
        
#         last_error = None

#         for attempt in range(self.max_retries):
#             try:
#                 message = self.client.messages.create(
#                     model = model,
#                     max_tokens=max_tokens,
#                     messages=[{"role":"user","content":prompt}]
#                 )
#                 return message.content[0].text.strip()
            
#             except anthropic.RateLimitError :
#                 wait = self.base_delay*(2**attempt)
#                 print(f"Rate Limit Exceeded! please wait {wait}s to retry {attempt+1}...")
#                 time.sleep(wait)
#                 last_error="Rate Limit Exceeded!"

#             except anthropic.APITimeoutError:
#                 wait = self.base_delay*(2**attempt)
#                 print(f"Timeout! please wait {wait}s to retry {attempt+1}")
#                 time.sleep(wait)
#                 last_error = "Timeout"
            
#             except anthropic.APIError as e:
#                 if 400 <= e.status_code < 500:
#                     raise
#                 wait = self.base_delay*(2**attempt)
#                 time.sleep(wait)
#                 last_error=str(e)
        
#         raise RuntimeError(f"Failed after {self.max_retries} attempts. Last error: {last_error}")
    
# client = MyAIWrapper()
# result = client.call("What are the standard errors a program should tackle while calling an api? for example APITimeout error or APIRatelimit error","claude-haiku-4-5")
# print(result)
    

                