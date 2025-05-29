from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, database, auth
from services.services import BlogService

router = APIRouter(prefix="/blogs", tags=["Blogs"])

def get_blog_service(db: Session = Depends(database.SessionLocal)) -> BlogService:
    return BlogService(db)

@router.post("/", response_model=schemas.BlogOut)
def create_blog(
    blog: schemas.BlogCreate,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: models.User = Depends(auth.get_current_user)
):
    return blog_service.create_blog(blog, current_user)

@router.get("/", response_model=List[schemas.BlogOut])
def list_blogs(
    skip: int = 0,
    limit: int = 10,
    blog_service: BlogService = Depends(get_blog_service)
):
    return blog_service.list_blogs(skip, limit)

@router.get("/{id}", response_model=schemas.BlogOut)
def get_blog(
    id: int,
    blog_service: BlogService = Depends(get_blog_service)
):
    return blog_service.get_blog(id)

@router.put("/{id}", response_model=schemas.BlogOut)
def update_blog(
    id: int,
    blog: schemas.BlogCreate,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: models.User = Depends(auth.get_current_user)
):
    return blog_service.update_blog(id, blog, current_user)

@router.delete("/{id}")
def delete_blog(
    id: int,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: models.User = Depends(auth.get_current_user)
):
    return blog_service.delete_blog(id, current_user)
