import os
import re

import openai
import json
from .constants import INSTRUCTIONS
from .schema import AiRequest, SafeResponse, MedicalData
import re
from typing import Tuple, Optional
from pydantic_core._pydantic_core import ValidationError

def parse_ai_response(response: str) -> Tuple[str, Optional[dict]]:
    """
    Парсит ответ AI на текстовую часть и медицинские данные
    """
    # Пытаемся найти JSON в ответе
    json_pattern = 'MEDICAL_JSON:'
    part = response.output[0].content[0].text
    answer_text, json_raw = part.split(json_pattern)
    try:
        json_prepare = json_raw[json_raw.find('{'): json_raw.find('}') + 1]
        # json_data = json.loads(json_prepare)
        medical_data = MedicalData.model_validate_json(json_prepare)
        return answer_text, medical_data
    except (json.JSONDecodeError, ValidationError):
        print("Пересон json в объект не удался")
        return response, None



    # Если JSON не найден, возвращаем весь текст как ответ
    return response, None

def check_input(message):
    try:
        if not message and message.strip():
            return False
        if not bool(message and re.search(r'[a-zA-Zа-яА-Я]', message)):
            return False
    except Exception as error:
        print(error)
        return False

    return True


def ai_assist(request: AiRequest):
    YANDEX_CLOUD_MODEL = os.getenv("YANDEX_CLOUD_MODEL")
    YANDEX_CLOUD_FOLDER = os.getenv("YANDEX_CLOUD_FOLDER")
    YANDEX_CLOUD_API_KEY = os.getenv("YANDEX_CLOUD_API_KEY")
    CUSTOM_AI_MODEL = os.getenv("CUSTOM_AI_MODEL")

    message = request.message
    if not check_input(message):
        return SafeResponse({
            "output": [
                {
                    "content": [
                        {"text": "Похоже, что отправили некорректное сообщение"}
                    ]
                }
            ]
        })

    client = openai.OpenAI(
        api_key=YANDEX_CLOUD_API_KEY,
        base_url="https://rest-assistant.api.cloud.yandex.net/v1",
        project=YANDEX_CLOUD_FOLDER
    )

    response = client.responses.create(
        # model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
        model=f"{CUSTOM_AI_MODEL}",
        input=message,
        instructions=f'{INSTRUCTIONS}',
        temperature=0.8,
        max_output_tokens=1500
    )

    answer_text = response.output[0].content[0].text
    print(answer_text)
    return response


if __name__ == "__main__":

    request = AiRequest(message='Добрый день. Какой у вас возраст и '
                                'температура')
    responce = ai_assist(request)
    answer, med_data = parse_ai_response(responce)
    print(answer)