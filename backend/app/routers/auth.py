from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.auth_schema import AuthResponse, LoginRequest, MessageResponse, SignupRequest, UserProfile
from app.services.auth_service import login, signup, user_profile

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse)
async def signup_route(payload: SignupRequest) -> AuthResponse:
    return await signup(payload)


@router.post("/login", response_model=AuthResponse)
async def login_route(payload: LoginRequest) -> AuthResponse:
    return await login(payload)


@router.get("/me", response_model=UserProfile)
async def me_route(current_user: dict = Depends(get_current_user)) -> UserProfile:
    return user_profile(current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout_route(_: dict = Depends(get_current_user)) -> MessageResponse:
    return MessageResponse(message="Logout successful. Remove the token on the client.")
