from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PREFIX = "/api"
    ACCESS_TOKEN_EXPIRED = 10

    class Config:
        env_file = './.env'



settings = Settings()
