from pydantic import BaseModel, Field, field_validator, ValidationError
import re


class UserProfile(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=18, le=100)
    email: str
    pan: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Invalid email address")
        return value

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, value):
        pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

        if not re.match(pattern, value):
            raise ValueError("Invalid PAN format")

        return value


try:
    user = UserProfile(
        name="G",
        age=15,
        email="invalid-email",
        pan="123456"
)

    print(user)

except ValidationError as e:
    print(e)