from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@localhost:5432/course_website"
SQLALCHEMY_DATABASE_URL = "postgres://tugrefnkrtbjvk:7d4c031048e0e5908f90135605bda7964d85c37a1f87a5f04871dbe2d9a19af3@ec2-54-237-143-127.compute-1.amazonaws.com:5432/das7sc8jfhka1q"
#SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
