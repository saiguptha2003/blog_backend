from sqlalchemy.orm import Session
from app import models, schemas, auth
from fastapi import HTTPException
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

class BlogService:
    def __init__(self, db: Session):
        self.db = db

    def create_blog(self, blog: schemas.BlogCreate, current_user: models.User) -> models.Blog:
        new_blog = models.Blog(**blog.dict(), author_id=current_user.id)
        self.db.add(new_blog)
        self.db.commit()
        self.db.refresh(new_blog)
        return new_blog

    def list_blogs(self, skip: int = 0, limit: int = 10) -> List[models.Blog]:
        return self.db.query(models.Blog).offset(skip).limit(limit).all()

    def get_blog(self, id: int) -> models.Blog:
        blog = self.db.query(models.Blog).filter(models.Blog.id == id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog

    def update_blog(self, id: int, blog: schemas.BlogCreate, current_user: models.User) -> models.Blog:
        db_blog = self.db.query(models.Blog).filter(models.Blog.id == id).first()
        if not db_blog or db_blog.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        for key, value in blog.dict().items():
            setattr(db_blog, key, value)
            
        self.db.commit()
        self.db.refresh(db_blog)
        return db_blog

    def delete_blog(self, id: int, current_user: models.User) -> dict:
        db_blog = self.db.query(models.Blog).filter(models.Blog.id == id).first()
        if not db_blog or db_blog.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        self.db.delete(db_blog)
        self.db.commit()
        return {"detail": "Blog deleted"}

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def signup(self, user: schemas.UserCreate) -> models.User:
        db_user = self.db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_pw = auth.get_password_hash(user.password)
        new_user = models.User(email=user.email, password=hashed_pw)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def login(self, form_data: OAuth2PasswordRequestForm) -> dict:
        user = self.db.query(models.User).filter(models.User.email == form_data.username).first()
        if not user or not auth.verify_password(form_data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
            
        access_token = auth.create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}