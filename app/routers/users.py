from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import schemas, database
from services.services import UserService
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_user_service(db: Session = Depends(database.get_db)) -> UserService:
    return UserService(db)

@router.post(
    "/signup",
    response_model=schemas.UserOut,
    summary="Create new user",
    description="Register a new user with email and password"
)
async def signup(
    user: schemas.UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    logger.info(f"Received signup request for email: {user.email}")
    try:
        new_user = user_service.signup(user)
        logger.info(f"Successfully created user with email: {user.email}")
        return new_user
    except Exception as e:
        logger.error(f"Error during signup for email {user.email}: {str(e)}")
        raise

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    logger.info(f"Login attempt for user: {form_data.username}")
    try:
        token = user_service.login(form_data)
        logger.info(f"Successful login for user: {form_data.username}")
        return token
    except Exception as e:
        logger.error(f"Login failed for user {form_data.username}: {str(e)}")
        raise
