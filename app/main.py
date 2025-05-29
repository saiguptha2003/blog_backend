from fastapi import FastAPI
from app.routers import users, blogs
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(blogs.router)
