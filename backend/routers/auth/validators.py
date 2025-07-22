# routers/auth/validators.py

from pydantic import BaseModel, Field # Import Field for optional fields

class CreateUserRequest(BaseModel):
    # Keep this if you still have a create-user route for non-Google users,
    # otherwise, you can remove it.
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class GoogleUser(BaseModel):
    # Consider if 'sub' should be str or int based on Google's actual type.
    # Google's 'sub' is typically a string, not an integer.
    sub: str # Changed from int to str
    email: str
    name: str
    picture: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

# NEW: Pydantic model for User responses
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # google_sub: str | None = None # Include if you want to expose this, make it Optional
    # If you only return users through Google, google_sub will always be present, but can be None in DB
    google_sub: str | None = Field(None, description="Google Sub ID (if user registered via Google)")


    class Config:
        # This tells Pydantic to read data from ORM objects (like SQLAlchemy models)
        # It allows you to pass a SQLAlchemy User object directly to UserResponse(**user.__dict__)
        # or UserResponse.from_orm(user)
        from_attributes = True # Pydantic v2 syntax
        # or for Pydantic v1: orm_mode = True # Pydantic v1 syntax