from starlette.middleware.cors import CORSMiddleware

from config import app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get("/send_to_ai/*")
async def root():
    pass
