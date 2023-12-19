from fastapi import  FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine,Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router


app = FastAPI()
app.title="Mi aplicacion con FastAPI"
app.version="0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(movie_router)



Base.metadata.create_all(bind=engine)
