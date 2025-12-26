"""User email DTO."""

from pydantic import BaseModel, Field, EmailStr


class UserEmailDto(BaseModel):
    """Input requiring only a user email."""

    email: EmailStr = Field(..., description="Email address of the user to find")
