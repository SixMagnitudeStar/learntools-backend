from pydantic import BaseModel


class AddWordRequest(BaseModel):
    word: str