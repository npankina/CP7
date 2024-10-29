from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://shop_admin:0000@localhost/shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
