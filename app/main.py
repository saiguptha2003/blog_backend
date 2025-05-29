from fastapi import FastAPI
from app.routers import users, blogs
from app.database import Base, engine
from app.utils.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up BlogApp")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down BlogApp")
app.include_router(users.router)
app.include_router(blogs.router)
