from starlette.middleware.cors import CORSMiddleware
from .schema import AiRequest,AiResponse
from .config import app
from fastapi import APIRouter
from .ai_assist import *

router = APIRouter()

@router.post("/ai_request", response_model=AiResponse)
async def ai_request(request: AiRequest):

    response = ai_assist(request)
    answer = response.output[0].content[0].text

    return AiResponse(
        response=answer,
        medicalData={
            "temperature": "37.8°C",
            "pressure": "130/85",
            "pulse": "95 уд/мин",
            "painLocation": "!!! Правая подвздошная область"
        }
    )
