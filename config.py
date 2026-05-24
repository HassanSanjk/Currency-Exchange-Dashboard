from dotenv import load_dotenv
import os

load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    CURRENCYAPI_KEY = os.getenv("CURRENCYAPI_KEY")
    ALSOUG_URL = os.getenv("ALSOUG_URL")
    REDIS_URL = os.getenv("REDIS_URL")