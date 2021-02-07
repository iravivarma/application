from sqlalchemy.orm import Session
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
import models, schemas
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import load_only

from models import Users, Courses, Categories, Domain



def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()	

def get_user_email(db: Session, email: str):
	return db.query(models.Users).filter(models.Users.email == email).first()

def create_user(db: Session, user: schemas.NewUser):
	print(user.__dict__)
	password = user.password
	user_details = models.Users(name = user.name, email = user.email, password= password)
	db.add(user_details)
	db.commit(user_details)
	db.refresh(user_details)
	return user_details

def create_domain(db: Session, domain: schemas.Domain_Create):

	domain_details = models.Domain(domain_name=domain.domain_name)
	db.add(domain_details)
	db.commit()
	db.refresh(domain_details)

	return domain_details

def get_domain(db: Session, domain_name: str):
	return db.query(models.Domain).filter(models.Domain.domain_name == domain_name).first()

def get_category(db: Session, category_name: str):
	return db.query(models.Categories).filter(models.Categories.name == category_name).first()

def get_user(db: Session, user_name: str):
    return db.query(models.Users).filter(models.Users.name == user_name).first()




def create_categories(db: Session, domain_id:int, category: schemas.categories_create,):

	category_details = models.Categories(name= category.cat_name, created_date= 123, domain_id= domain_id)
	db.add(category_details)
	db.commit()
	db.refresh(category_details)

	return category_details


