from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PREFIX = "/api"
    ACCESS_TOKEN_EXPIRED = 10
    vnp_TmnCode = ""
    vnp_HashSecret = ""
    vnp_Url = ""
    vnp_ReturnUrl = ""
    curr_code = ""
    locale = "vn"
    
    class Config:
        env_file = './.env'



settings = Settings()
