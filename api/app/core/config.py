from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str
    GEMINI_API_KEY:str
    CHROME_PATH:str
    API_URL:str
    REDIS_URL:str
    DB_URI:str    
    PORT:int
    DOC_TO_PDF_API_URL:str
    QSTASH_URL:str
    QSTASH_TOKEN:str
    QSTASH_CURRENT_SIGNING_KEY:str
    QSTASH_NEXT_SIGNING_KEY:str

settings = Settings()