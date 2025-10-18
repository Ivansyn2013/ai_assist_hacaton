import os
import re

import openai

from .constants import INSTRUCTIONS
from .schema import AiRequest, SafeResponse


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
    request = AiRequest(message='Как дела')
    ai_assist(request)
