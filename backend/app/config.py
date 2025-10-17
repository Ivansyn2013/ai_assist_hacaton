from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажи точный origin!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
