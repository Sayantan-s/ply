from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    PORT: int

    GEMINI_API_KEY: str
    CHROME_PATH: str

    API_URL: str
    DB_URI: str

    DOC_TO_PDF_API_URL: str

    QSTASH_URL: str
    QSTASH_TOKEN: str
    QSTASH_CURRENT_SIGNING_KEY: str
    QSTASH_NEXT_SIGNING_KEY: str

    REDIS_DB: str
    REDIS_HOST: str
    REDIS_PORT: str

    def get_redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()
