from fastapi import FastAPI
from .routers import blog, user
from . import models
from .database import engine

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)
