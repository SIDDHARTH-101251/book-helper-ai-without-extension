from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_core import ValidationError

class Settings(BaseSettings):
    # required → app will refuse to start if the key is missing
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")

    class Config:
        env_file = ".env"          # look here while developing
        env_file_encoding = "utf-8"

try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add it to a .env file or set the environment variable."
    ) from e
