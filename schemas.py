from typing import List, Optional, Dict

from pydantic import BaseModel, EmailStr
from fastapi import Form


class UserCreate(BaseModel):

	name:str
	email: str


class UsersCreate(UserCreate):
	password: str

class NewUser(BaseModel):
	name:str
	email:str
	password:str


class Users(UsersCreate):
	id:int
	class config:
		orm_mode = True



########Domain_Schema#######

class Domain_Create(BaseModel):
	
	domain_name:str



####categories_Schema####

class categories_create(BaseModel):

	cat_name:str



######Courses_Schema####

# class Courses_Create(BaseModel):

# 	course_name:str
# 	course_category:str
# 	course_source:str
# 	course_link:str
# 	course_description:str
# 	course_type:str
# 	course_medium:str
# 	level:str

# class Courses(Courses_Create):
# 	creeated_by: str


class NewCourses(BaseModel):
	created_by: str
	course_name:str
	course_category:str
	course_source:str
	course_link:str
	course_description:str
	course_type:str
	course_medium:str
	level:str

#######contributing 0r create button that is not related to anything. If you dont know to how to contribute you can contribute using this thing####
class Courses(NewCourses):
	domain_name: str