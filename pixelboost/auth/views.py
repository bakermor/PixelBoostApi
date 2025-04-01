from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from beanie import PydanticObjectId

from .models import UserRead, UserRegister, Token, RefreshRequest, UserUpdatePassword
from .service import get, get_by_username, create, login, refresh, set_password, CurrentUser
from .utils import verify_password

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(user_in: UserRegister):
    user = await get_by_username(user_in.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username in use')
    user = await create(user_in)
    return user

@router.post("/login", response_model=Token)
async def login_user(user_in: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_by_username(user_in.username)

    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password',
                            headers={"WWW-Authenticate": "Bearer"})

    token = await login(user)
    return token

@router.post("/refresh", response_model=Token)
async def refresh_user(refresh_token: RefreshRequest):
    token = await refresh(refresh_token.refresh_token)
    return token

@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user

@router.post("/{user_id}/change-password", response_model=UserRead)
async def change_password(user_id: PydanticObjectId, password_update: UserUpdatePassword, current_user: CurrentUser):
    user = await get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='A user with this id does not exist')
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(password_update.current_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid current password")
    user_out = await set_password(user, password_update)
    return user_out
