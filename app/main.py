import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi import FastAPI
from datetime import datetime, timedelta, timezone
from models import Product

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))

# Подключение к базе данных
engine = create_async_engine(DATABASE_URL)
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}




# Использование секретного ключа для создания JWT-токенов
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt
