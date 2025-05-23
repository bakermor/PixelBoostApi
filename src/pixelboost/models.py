from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, field_validator, Field


# Pydantic
class Stat(BaseModel):
    current_level: float
    last_updated: float | None = None
    equation: list[float]

    @field_validator("current_level")
    def constrain_values(cls, value: float) -> float:
        return max(0.0, min(100.0, value))

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "current_level": 50.0,
                    "last_updated": 1743654156.04459,
                    "equation": []
                }]}}

class Health(BaseModel):
    hunger: Stat
    thirst: Stat
    energy: Stat
    social: Stat
    fun: Stat
    hygiene: Stat

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "hunger": {
                        "current_level": 50.0,
                        "last_updated": 1743654156.04459,
                        "equation": []
                    },
                    "thirst": {
                        "current_level": 72.0,
                        "last_updated": 1743654156.04459,
                        "equation": []
                    },
                    "energy": {
                        "current_level": 13.0,
                        "last_updated": 1743654156.04459,
                        "equation": []
                    },
                    "social": {
                        "current_level": 45.0,
                        "last_updated": 1743654156.04459,
                        "equation": []
                    },
                    "fun": {
                        "current_level": 90.0,
                        "last_updated": 1743654178.2973874,
                        "equation": []
                    },
                    "hygiene": {
                        "current_level": 67.0,
                        "last_updated": 1743654156.04459,
                        "equation": []
                    }}]}}

class Modifiers(BaseModel):
    hunger: float | None = None
    thirst: float | None = None
    energy: float | None = None
    social: float | None = None
    fun: float | None = None
    hygiene: float | None = None

# MongoDB
class Activity(Document):
    name: str
    start_time: float | None = None
    time_limit: float | None = None
    modifiers: Modifiers

    class Settings:
        name = "activities"

class User(Document):
    username: str = Field(min_length=3, max_length=24, pattern=r"^[a-zA-Z0-9_-]+$")
    name: str
    email: EmailStr
    is_verified: bool = False
    password: str

    current_activity: Link[Activity] | None = None

    health: Health
    activities: list[PydanticObjectId] = []

    class Settings:
        name = "users"
