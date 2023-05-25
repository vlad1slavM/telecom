from pydantic import BaseModel


class MyResponse(BaseModel):
    """Модель ответа на ошибку из базы данных"""
    code: int
    message: str
