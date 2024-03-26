from pydantic import BaseModel, EmailStr, Field
from datetime import date


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    second_name: str = Field(min_length=3, max_length=50)
    email_add: EmailStr
    phone_num: str = Field()
    birth_date: date


class ContactSchemaResponse(BaseModel):
    id: int = 1
    first_name: str
    second_name: str
    email_add: EmailStr
    phone_num: str
    birth_date: date

    class Config:
        from_attributes = True

