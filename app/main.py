from fastapi import FastAPI, HTTPException
from app.routers import users, blogs
from app.database import Base, engine
from app.utils.logger import logger
from app.utils.redis_client import get_redis_client
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
    try:
        redis_client = get_redis_client()
        redis_client.set("app_status", "running")
        logger.info("Successfully connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down BlogApp")

@app.get("/health")
async def health_check():
    try:
        redis_client = get_redis_client()
        redis_status = redis_client.get("app_status")
        return {
            "status": "healthy",
            "redis_status": redis_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis connection error: {str(e)}")

@app.post("/redis/{key}")
async def set_redis_value(key: str, value: str):
    try:
        redis_client = get_redis_client()
        redis_client.set(key, value)
        return {"message": f"Successfully set {key}={value}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/redis/{key}")
async def get_redis_value(key: str):
    try:
        redis_client = get_redis_client()
        value = redis_client.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail=f"Key {key} not found")
        return {"key": key, "value": value}
    except redis.ConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Redis connection error: {str(e)}")

app.include_router(users.router)
app.include_router(blogs.router)
