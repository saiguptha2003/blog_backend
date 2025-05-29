from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, database
from services.services import UserService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_user_service(db: Session = Depends(database.SessionLocal)) -> UserService:
    return UserService(db)

@router.post("/signup", response_model=schemas.UserOut)
def signup(
    user: schemas.UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.signup(user)

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.login(form_data)
