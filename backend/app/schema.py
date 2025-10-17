from pydantic import BaseModel

class AiRequest(BaseModel):
    message: str

# Модель ответа
class AiResponse(BaseModel):
    response: str
    medicalData: dict
