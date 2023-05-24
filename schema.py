from pydantic import BaseModel


class MyResponse(BaseModel):
    code: int
    message: str
