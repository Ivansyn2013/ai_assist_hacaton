from .config import app
from .routes import router
app.include_router(router)

