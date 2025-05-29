from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.logger import logger
from fastapi.security import OAuth2PasswordRequestForm
class BlogService:
    def __init__(self, db: Session):
        self.db = db

    def create_blog(self, blog: schemas.BlogCreate, current_user: models.User) -> models.Blog:
        try:
            new_blog = models.Blog(
                title=blog.title,
                content=blog.content,
                author_id=current_user.id,
                created_at=datetime.utcnow(),
                updated_at=None
            )
            self.db.add(new_blog)
            self.db.commit()
            self.db.refresh(new_blog)
            return new_blog
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def list_blogs(self, skip: int = 0, limit: int = 10):
        return self.db.query(models.Blog).offset(skip).limit(limit).all()

    def get_blog(self, blog_id: int):
        blog = self.db.query(models.Blog).filter(models.Blog.id == blog_id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog

    def update_blog(self, blog_id: int, blog: schemas.BlogCreate, current_user: models.User):
        db_blog = self.get_blog(blog_id)
        if db_blog.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this blog")
        
        for key, value in blog.model_dump().items():
            setattr(db_blog, key, value)
        db_blog.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_blog)
        return db_blog

    def delete_blog(self, blog_id: int, current_user: models.User):
        db_blog = self.get_blog(blog_id)
        if db_blog.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this blog")
        
        self.db.delete(db_blog)
        self.db.commit()
        return {"message": "Blog deleted successfully"}

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def signup(self, user: schemas.UserCreate) -> models.User:
        logger.info(f"Processing signup for email: {user.email}")
        try:
            db_user = self.db.query(models.User).filter(models.User.email == user.email).first()
            if db_user:
                logger.warning(f"Signup attempt with existing email: {user.email}")
                raise HTTPException(status_code=400, detail="Email already registered")
            
            hashed_pw = auth.get_password_hash(user.password)
            new_user = models.User(email=user.email, password=hashed_pw)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            logger.info(f"Successfully created new user with email: {user.email}")
            return new_user
        except Exception as e:
            logger.error(f"Error during signup: {str(e)}")
            raise

    def login(self, form_data: OAuth2PasswordRequestForm) -> dict:
        user = self.db.query(models.User).filter(models.User.email == form_data.username).first()
        if not user or not auth.verify_password(form_data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
            
        access_token = auth.create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}