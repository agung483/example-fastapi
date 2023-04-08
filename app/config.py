from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "Akalku12"
    database_name: str = "restokita"
    database_username: str = "agung"
    secret_key: str = "8293f8f38963e538e798b377de6d16005aef2734662c54a39159c33115c7628f"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    class Config:
        env_file = ".env"

settings = Settings()