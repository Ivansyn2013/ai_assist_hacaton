from starlette.middleware.cors import CORSMiddleware
from .schema import AiRequest, AiResponse, MedicalData
from .config import app
from fastapi import APIRouter
from .ai_assist import *


router = APIRouter()

@router.post("/ai_request", response_model=AiResponse)
async def ai_request(request: AiRequest):
    response = ai_assist(request)

    parse_answer = parse_ai_response(response)
    if not parse_answer[1]:
        answer = response.output[0].content[0].text
        medical_data = {"temperature": "",
            "pressure": "",
            "pulse": "",
            "painLocation": ""}
    else:
        answer = parse_answer[0]
        medical_data = parse_answer[1]
        print(f'Пытаюсь отправитить объукт медицинсккиъ данных{medical_data}')
    return AiResponse(
        response=answer,
        medical_data=medical_data
    )
