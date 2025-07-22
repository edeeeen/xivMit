#################################################################
#               OAuth Implementation routed to /auth            #
#################################################################

from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from typing import Annotated
from starlette import status
from db.dbModels import User
from .validators import GoogleUser, Token, RefreshTokenRequest, UserResponse 
from .services import create_access_token, create_refresh_token, \
    create_user_from_google_info, get_user_by_google_sub, token_expired, decode_token, user_dependency, oauth_bearer 
from db.db import db_dependency # Correct import for db_dependency
from .services import oauth # Import the oauth client
from fastapi import Request
from fastapi.responses import RedirectResponse
import os


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# Ensure GOOGLE_REDIRECT_URI matches your Google Cloud Console setup
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google" # Use full URL for clarity
FRONTEND_URL = "http://localhost:5127"




####################### GOOGLE OAUTH #######################

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initiates google oauth login
@router.get("/login/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)

# Handles oauth callback
@router.get("/google")
async def auth_google(request: Request, db: db_dependency):
    try:
        # Fetches user info and token from google
        user_response: OAuth2Token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate Google credentials: {e}"
        )

    # user_info contains profile data from google
    user_info = user_response.get("userinfo")

    if not user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No user info received from Google.")

    # Validate user_info
    google_user = GoogleUser(**user_info) 

    existing_user = get_user_by_google_sub(google_user.sub, db)

    # Initialize user
    user = None 
    if existing_user:
        user = existing_user
    else:
        user = create_user_from_google_info(google_user, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create or retrieve user.")

    # Create JWTs for the authenticated user
    access_token = create_access_token(user.username, user.id, timedelta(minutes=15)) # Shorter access token
    refresh_token = create_refresh_token(user.username, user.id, timedelta(days=7)) # Longer refresh token

    # Redirect to frontend with tokens as query parameters
    # The frontend will then store these tokens
    return RedirectResponse(f"{FRONTEND_URL}/auth?access_token={access_token}&refresh_token={refresh_token}", status_code=status.HTTP_302_FOUND)



@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_authenticated_user(user: user_dependency):
    return user

@router.post("/refresh", response_model=Token)
async def refresh_access_token(db: db_dependency, refresh_token_request: RefreshTokenRequest):
    """
    Refreshes an access token using a valid refresh token.
    Raises HTTPException if the refresh token is expired or invalid.
    """
    token = refresh_token_request.refresh_token

    # token_expired already raises HTTPException on invalid token now
    if token_expired(token): # This will now return True for invalid/expired tokens
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is expired or invalid.")

    # decode_token will raise HTTPException if token is invalid
    user_payload = decode_token(token) # Renamed to user_payload for clarity

    # You might want to re-fetch the user from the DB to ensure they still exist and are active
    # based on user_payload['id'] or user_payload['sub']
    # user = db.query(User).filter(User.id == user_payload['id']).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User associated with refresh token not found.")
    # access_token = create_access_token(user.username, user.id, timedelta(minutes=15))
    # refresh_token = create_refresh_token(user.username, user.id, timedelta(days=7))


    # For simplicity, if you trust the refresh token's payload directly:
    access_token = create_access_token(user_payload["sub"], user_payload["id"], timedelta(minutes=15))
    refresh_token = create_refresh_token(user_payload["sub"], user_payload["id"], timedelta(days=7))


    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}