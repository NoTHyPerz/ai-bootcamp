# from pydantic import BaseModel, field_validator,model_validator

# class User(BaseModel):
#     name: str
#     age: int=25

#     @field_validator('age')
#     def validate_age(cls, value):
#         if value < 0:
#             raise ValueError('Age must be a non-negative integer')
#         return value
    
# # Example usage

# try:
#     user = User(name="Alice")
#     print(user)
# except ValueError as e:
#     # print(f"Validation error: {e}")
#     print(e)

# class PasswordModel(BaseModel):
#     password: str
#     confirm_password: str

#     @model_validator(mode='after')
#     def validate_passwords(cls, model):
#         if model.password != model.confirm_password:
#             raise ValueError('Passwords do not match')
#         return model
    
# # Example usage
# try:
#     password_data = PasswordModel(password="secret123", confirm_password="secret123")
#     print(password_data)
# except ValueError as e:
#     print(e)


# # Pydantic JSON parsing example
# from pydantic import BaseModel

# class UserProfile(BaseModel):
#     name: str
#     age: int
#     email: str

# data = '{"name": "Noah Kim", "age": 28, "email": "noah.kim@example.kr"}'
# user = UserProfile.model_validate_json(data)
# print(user)


# # Pydantic JSON serialization example
# from pydantic import BaseModel
# from typing import Optional

# class UserProfile(BaseModel):
#     name: str
#     age: Optional[int] = None
#     email: str

# user = UserProfile(name="Luca Rossi", age=29, email="luca.rossi@example.it")
# json_data = user.model_dump_json()
# print(json_data)


# mini Project : Person Extractor using an LLM and Pydantic

import anthropic
from pydantic import BaseModel, field_validator, model_validator
from dotenv import load_dotenv
from typing import Optional
import json
import asyncio

load_dotenv()
# using async anthropic
client = anthropic.AsyncAnthropic()

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str
    fun_fact: Optional[str] = None

    @field_validator('age')
    def validate_age(cls,value):
        if value<0 or value>120:
            raise ValueError('Age must be between 0 and 120')
        return value
    
async def extract_person_info(text: str) -> PersonInfo:
    message = await client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        messages=[{"role": "user","content":f"""Extract the person's information.

                    Return ONLY valid JSON.

                    Do not include markdown.
                    Do not include explanations.
                    Do not wrap in triple backticks.

                    Schema : {PersonInfo.model_json_schema()}

                    Text : {text}"""
                }]
    )
        
    # print (message)
    raw = message.content[0].text.strip()
    # print (raw)
    data = json.loads(raw)
    return PersonInfo.model_validate(data)


# Test it
async def main():

    result = await extract_person_info(
        "Elon Musk, born in 1971, is a tech entrepreneur and CEO of multiple companies. "
        "He once ate a whole cake in one sitting at a party."
    )
    # print(result)
    print(f"Name: {result.name}, Age: {result.age}")
    
asyncio.run(main())