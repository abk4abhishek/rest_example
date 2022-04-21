from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_DATABASE_HOST : str
    APP_DATABASE_PORT : int
    APP_DATABASE_USERNAME : str
    APP_DATABASE_PASSWORD : str
    APP_DATABASE_NAME : str
    APP_AUTH_TOKEN_SECRET_KEY : str
    APP_AUTH_TOKEN_ALGORITHM : str
    APP_AUTH_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()