from .config import app
from .routes import router

app.include_router(router)

def web():
    pass

def ai_request():
    pass

if __name__ == "__main__":
    pass


