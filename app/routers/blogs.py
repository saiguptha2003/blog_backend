from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, database, auth
from services.services import BlogService
from app.utils.logger import logger

router = APIRouter(prefix="/blogs", tags=["Blogs"])

def get_blog_service(db: Session = Depends(database.get_db)) -> BlogService:
    return BlogService(db)

@router.post("/", response_model=schemas.BlogOut)
async def create_blog(
    blog: schemas.BlogCreate,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"Creating blog with title: {blog.title}")
    try:
        return blog_service.create_blog(blog, current_user)
    except Exception as e:
        logger.error(f"Error creating blog: {str(e)}")
        raise

@router.get("/", response_model=List[schemas.BlogOut])
async def list_blogs(
    skip: int = 0,
    limit: int = 10,
    blog_service: BlogService = Depends(get_blog_service)
):
    logger.info(f"Listing blogs with skip={skip}, limit={limit}")
    return blog_service.list_blogs(skip, limit)

@router.get("/{id}", response_model=schemas.BlogOut)
async def get_blog(
    id: int,
    blog_service: BlogService = Depends(get_blog_service)
):
    logger.info(f"Fetching blog with id: {id}")
    return blog_service.get_blog(id)

@router.put("/{id}", response_model=schemas.BlogOut)
async def update_blog(
    id: int,
    blog: schemas.BlogCreate,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"Updating blog with id: {id}")
    return blog_service.update_blog(id, blog, current_user)

@router.delete("/{id}")
async def delete_blog(
    id: int,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"Deleting blog with id: {id}")
    return blog_service.delete_blog(id, current_user)
