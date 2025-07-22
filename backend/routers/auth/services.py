# services.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Optional
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, defer
from authlib.integrations.starlette_client import OAuth
import os
from jose import jwt, JWTError
from starlette.config import Config
from datetime import timedelta, datetime, UTC

from .validators import GoogleUser
from db.dbModels import User
from db.db import db_dependency

ALGORITHM = "HS256"

oauth_bearer = HTTPBearer(scheme_name="Bearer Auth")

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
SECRET_KEY = os.environ.get("SECRET_KEY")

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None or SECRET_KEY is None:
    raise Exception('Missing GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, or SECRET_KEY env variables')

config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}

starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}

    expires = datetime.now(UTC) + expires_delta

    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) # Use loaded SECRET_KEY


def create_refresh_token(username: str, user_id: int, expires_delta: timedelta):
    return create_access_token(username, user_id, expires_delta)

# Decodes a JWT
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}"
        )

# Dependency to get the current authenticated user from a JWT access token
# Raises HTTPException if token is invalid or user not found
def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth_bearer)], db: db_dependency):
    payload = decode_token(token.credentials)

    username: Optional[str] = payload.get("sub")
    user_id: Optional[int] = payload.get("id")

    if username is None or user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

    # Fetch user from DB
    user: Optional[User] = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

    return user

# Checks if a given JWT token has expired
def token_expired(token: str) -> bool:
    try:
        payload = decode_token(token)
        # Ensure 'exp' exists in payload
        if 'exp' not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has no expiry information.")

        # Compare expiry time (UTC) with current time (UTC)
        is_expired = not datetime.fromtimestamp(payload.get('exp'), UTC) > datetime.now(UTC)
        return is_expired
    except HTTPException: # Catch the HTTPException raised by decode_token if the token is invalid
        return True
    except Exception as e:
        # Log unexpected errors during token expiration check
        print(f"Error checking token expiry: {e}")
        return True

# Fetches a user by their Google Sub ID
def get_user_by_google_sub(google_sub: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.google_sub == google_sub).first()

# Creates a new user based on Google user information
def create_user_from_google_info(google_user: GoogleUser, db: Session) -> User:
    google_sub = google_user.sub
    email = google_user.email

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        # If user exists by email, update their google_sub if it's missing
        # Not really necessary right now since theres only google auth
        if not existing_user.google_sub:
            existing_user.google_sub = google_sub
            db.add(existing_user)
            db.commit()
            db.refresh(existing_user)
        return existing_user
    else:
        # Create a new user entry
        new_user = User(
            username=google_user.email,
            email=google_user.email,
            google_sub=google_sub,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


user_dependency = Annotated[User, Depends(get_current_user)]