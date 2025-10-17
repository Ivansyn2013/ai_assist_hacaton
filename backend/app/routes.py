from starlette.middleware.cors import CORSMiddleware
from .schema import AiRequest,AiResponse
from .config import app



@app.post("/ai_request", response_model=AiResponse)
async def ai_request(request: AiRequest):
    # Пока — заглушка для острого аппендицита
    return AiResponse(
        response="Бэек ответ",
        medicalData={
            "temperature": "37.8°C",
            "pressure": "130/85",
            "pulse": "95 уд/мин",
            "painLocation": "!!! Правая подвздошная область"
        }
    )
