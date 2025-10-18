from typing import List

from pydantic import BaseModel

class AiRequest(BaseModel):
    temperature: float = None
    system_prompt: str = None
    message: str
    history: list = None
    medical_data: dict = None

# Модель ответа
class AiResponse(BaseModel):
    response: str


class SafeResponse:
    def __init__(self, data=None):
        self._data = data or {}

    def __getattr__(self, name):
        if name in self._data:
            value = self._data[name]
            if isinstance(value, (dict, list)):
                return SafeResponse.wrap(value)
            return value
        return SafeResponse()

    def __getitem__(self, index):
        if isinstance(self._data, list) and index < len(self._data):
            value = self._data[index]
            return SafeResponse.wrap(value)
        return SafeResponse()

    def __iter__(self):
        if isinstance(self._data, list):
            return (SafeResponse.wrap(item) for item in self._data)
        return iter([])

    @classmethod
    def wrap(cls, data):
        if isinstance(data, (dict, list)):
            return cls(data)
        return data

    @property
    def text(self):
        return self._data if isinstance(self._data, str) else ""

    def __repr__(self):
        return f"SafeResponse({self._data})"

    def __bool__(self):
        return bool(self._data)


