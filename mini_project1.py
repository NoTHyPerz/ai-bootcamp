"""
Mini-Project: Async CSV Enrichment
- Read a CSV of company names
- For each company, ask Claude for a one-sentence description
- Write results to output CSV
- Handle rate limits, show progress
"""

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator, model_validator
import json
import time
import asyncio
from typing import Optional

load_dotenv()

class company_profile(BaseModel):
    rank:int
    name:str
    market_cap:Optional[str]=None
    country:str
    industry:Optional[str]=None

client = anthropic.Anthropic()

company_list = client.messages.create(max_tokens=1024, model="claude-haiku-4-5", messages=[{"role":"user","content":f"give me a list of top 10 valuable companies in the world currently, ONLY RETURN THE DATA IN A JSON FORMAT FOLLOWING THE SCHEMA : {company_profile.model_json_schema()}  NOTHING ELSE. DO NOT USE ANY MARKDOWN FENCES!"}])

raw_data = company_list.content[0].text.strip()
# print(raw_data)

data = json.loads(raw_data)

# print(data)

file1 = open("company.csv","w")
file1.writelines("rank,name,market_cap,country,industry\n")
for comp in data:
    file1.writelines(f"{comp['rank']},{comp['name']},{comp['market_cap']},{comp['country']},{comp['industry']}\n") 
file1.close()


file1 = open("company.csv",'+w')


