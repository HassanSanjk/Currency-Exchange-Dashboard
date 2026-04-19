from dotenv import load_dotenv
import os

load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    CURRENCYAPI_KEY = os.getenv("CURRENCYAPI_KEY")
    ALSOUG_URL = os.getenv("ALSOUG_URL")
    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_PORT = int(os.getenv("DB_PORT"))
    MYSQL_USER = os.getenv("DB_USER")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    MYSQL_DB = os.getenv("DB_NAME")