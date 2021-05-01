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

#users output as a response.
class Users(UsersCreate):
	id:int
	class config:
		orm_mode = True

class user_item:
    """
    pydantic schema for new user sign-up
    """
    def __init__(self,
                 name: str = Form(...),
                 email: EmailStr = Form(...),
                 password: str = Form(...),
                 mobile_no: str = Form(...),
                 ):

        self.name = name
        self.email = email
        self.password = password
        self.mobile_no = mobile_no



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

class CoursesScope(BaseModel):
    email: str
    #position: str
    courses: List = None


class NewCourses(BaseModel):
	created_by: str
	course_name:str
	#course_category:str
	course_source:str
	course_link:str
	course_description:str
	course_type:str
	course_medium:str
	level:str

#######contributing 0r create button that is not related to anything. If you dont know to how to contribute you can contribute using this thing####
class Courses(NewCourses):
	domain_name: str


class Questions(BaseModel):
	Question_1: int
	Question_2: int
	Question_3: int

class feedback(Questions):
	course_name: str 
##############################For Filters############################################

class CourseFilters(BaseModel):
    course_level : Optional[str] =None#= 'Docs,Video,Book'
    course_medium:Optional[str] =None#= 'Beginner,Intermediate,Advanced'
    course_mode :Optional[str] = None #'Free,Paid'
#####################For Authentication###############################


class login_user_schema(BaseModel):
    """
    Pydantic schema for user login
    Currently the username is same as email
    """
    username: str
    name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None


class Token(BaseModel):
    """
    JWT token schema
    """    
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    #scopes : str = None#List[str] = []


class EmailSchema:
    """
    Pydantic Schema for email account recovery.

    Attributes
    ----------
    email : str
        The email where the recovery mail would be sent.
    """

    def __init__(self, email: str = Form(...)):
        """
        Parameters
        ----------
        email : HTML Form
            Would initialize the email from the submitted html form.
        """

        self.email = email


# class NewPassword(BaseModel):
#     """
#     Pydantic schema for user login
#     Currently the username is same as email
#     """
#     password1: str
#     password2: str

#     def __init__(self, password1:str = Form(...), password2:str = Form(...)):
#         super().__init__(password1, password2)


class NewPassword:
    """
    Pydantic Schema for account password.

    Attributes
    ----------
    password : str
        The new password that user will enter after forgot email verification.
    """

    def __init__(self, password1: str = Form(...),
                        password2: str = Form(...)):
        """
        Parameters
        ----------
        password : HTML Form
            Would initialize the password from the submitted html form.
        """

        self.password1 = password1
        self.password2 = password2


class SentPasscode:
    """
    Pydantic Schema for email account recovery.

    Attributes
    ----------
    passcode : str
        The passcode sent to the user on their mail.
    """

    def __init__(self, passcode: str = Form(...)):
        """
        Parameters
        ----------
        passcode : HTML Form
            Would initialize the passcode from the submitted html form.
        """

        self.passcode = passcode


class Search_schema(BaseModel):
    search_word : str

class authenticate_schema(BaseModel):
    email : str
    password : str