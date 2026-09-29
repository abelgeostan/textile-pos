from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url:str='postgresql+psycopg://pos:pos@localhost:5432/posdb'
    jwt_secret:str='change-this-in-production'
    access_token_expire_minutes:int=480
    cors_origins:str='http://localhost:5173'
    model_config=SettingsConfigDict(env_file='.env', extra='ignore')
settings=Settings()
