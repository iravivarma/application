from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@localhost:5432/course_website"
SQLALCHEMY_DATABASE_URL = "postgres://tugrefnkrtbjvk:7d4c031048e0e5908f90135605bda7964d85c37a1f87a5f04871dbe2d9a19af3@ec2-54-237-143-127.compute-1.amazonaws.com:5432/das7sc8jfhka1q"
SQLALCHEMY_DATABASE_URL2 = "postgres://pdszntpmoaxibt:3bf9c2ecb5a8b51b0dec9099fee6277c6070117918489869ddec6dfe1f4e029c@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d9a6vbq4d0d2q8"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

engine2 = create_engine(
    SQLALCHEMY_DATABASE_URL2
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

Base = declarative_base()
