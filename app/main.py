from fastapi import FastAPI
from app.routers import users, blogs
from app.database import Base, engine
from app.utils.logger import logger
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://blogify-x.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up BlogApp")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down BlogApp")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(users.router)
app.include_router(blogs.router)
