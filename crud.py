from sqlalchemy.orm import Session
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
import models, schemas
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import load_only
import datetime
from models import Users, Courses, Categories, Domain



def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()	

def get_user_email(db: Session, email: str):
	'''
	email: Input
	this gives output by Querying
	From : models-->Users(table)
	filters: email in models-->Users
	if model.email == input parameter
	it will return the User details as objects
	'''
	return db.query(models.Users).filter(models.Users.email == email).first()

def create_user(db: Session, user: schemas.NewUser):
	'''
	Input : New User Details in the NewUser calss of a Schema.py
	Create the User details From Schemas file NewUser Class
	'''
	print(user.__dict__)
	password = user.password
	user_details = models.Users(name = user.name, email = user.email, password= password, joined_on = str(datetime.datetime.now()))
	db.add(user_details)
	db.commit()
	db.refresh(user_details)
	return user_details

def create_domain(db: Session, domain: schemas.Domain_Create):

	'''
	Input: from Domain_Create class in schemas,py(validation model)
	i.e., the inputs we are going to give in Ui
'''
	domain_details = models.Domain(domain_name=domain.domain_name)
	db.add(domain_details)
	db.commit()
	db.refresh(domain_details)

	return domain_details

def get_domain(db: Session, domain_name: str):
	'''
	input: name of the domain
	return the query from Domain class in models.py and filter the
	domain_name of the Domain class by comparing with the input paramter.
	'''
	return db.query(models.Domain).filter(models.Domain.domain_name == domain_name).first()

def get_all_domains(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Domain).offset(skip).limit(limit).all()

def get_category(db: Session, category_name: str):
	'''
	input: name of the category
	return the query from Categories class in models.py and filter the
	name of the categories class by comparing with the input paramter.
	'''
	return db.query(models.Categories).filter(models.Categories.name == category_name).first()

def get_user(db: Session, user_name: str):
	'''
	input: name of the User
	return the query from Users class in models.py and filter the
	user_name of the Users class by comparing with the input paramter.
	'''
	return db.query(models.Users).filter(or_(models.Users.name == user_name, models.Users.email == user_name)).first()

def get_course(db: Session, course_name: str):
	'''
	input: name of the course
	return the query from Course class in models.py and filter the
	Course_name of the coursename class by comparing with the input paramter.
	'''
	course_details=db.query(models.Courses).filter(models.Courses.course_name == course_name).first()
	#print(course_details.upvotes)
	return course_details

def get_feedback(db: Session, question: int):
	'''
	input: feedback(questions)
	return the query from Questions class in models.py and filter the
	course_id of the question by comparing with the input paramter.
	'''
	question_details = db.query(models.Questions).filter(models.Questions.course_id==question).first()
	return question_details


def create_categories(db: Session, domain_id:int, category: schemas.categories_create):
	'''
	input from categories create class in schemas
	name: name of the category
	created_date: date of the category created
	add, commit and refresh: add, commit and update the details what the user given in UI
	'''

	category_details = models.Categories(name= category.cat_name, created_date= 123, domain_id= domain_id)
	db.add(category_details)
	db.commit()
	db.refresh(category_details)

	return category_details

def createCourses(db:Session, category_id: int, user_id: int, courses: schemas.NewCourses):
	'''
	input from NewCourse class in schemas
	created the course with the help of category_id and user_id
	returns the course details in the User Interface
	add, commit and refresh: add, commit and update the details what the user given in UI
	'''
	course_details = models.Courses(course_name= courses.course_name, course_source = courses.course_source, course_link = courses.course_link, description= courses.course_description,
		course_type= courses.course_type, course_medium= courses.course_medium, level= courses.level, upvotes=0, categories_id= category_id,
		created_by = user_id)
	db.add(course_details)
	db.commit()
	db.refresh(course_details)
	return course_details

def get_courses_by_category_name(db: Session, category_name: str):
	"""
	function returns the courses by issuing the category name
	cat-id:for category id, called the function of "get_category by giving the i/p parameters
	db, category_name" and retrive the id of a category
	then queries the Courses in Model classes if categories.id matches to the cat_id. If it is, returns all which it matches
	"""
	cat_id = get_category(db, category_name).id
	return db.query(models.Courses).filter(models.Courses.categories_id == cat_id).all()

def get_categories_by_domain_name(db: Session, domain_name: str):
	"""
	function returns the categories by issuing the domain name
	domain-id:for domain id, called the function of "get_domain by giving the i/p parameters
	db, category_name" and retrive the id of a domain_name
	then queries the Courses in Model classes if categories.domain_id matches to the domain_id. If it is, returns all which it matches
	"""
	domain_id = get_domain(db, domain_name).id
	return db.query(models.Categories).filter(models.Categories.domain_id == domain_id).all()

def upvote_course(db: Session, course_name: str):
	"""
 	Function for Upvoting a Course
 	course_id: To upvote a course we need a course_id, So, retrieved the course_details by calling the
 	function "get_course" got the coursedetails as object and
 	course: converted it to a dict
 	courseUpvote: retrieved the upvotesin a course details from course
 	course_upvote: returns the query with courses class in models and filter the course_id in models wit course_id
 	and update for every button clicks
	"""
	course_id = get_course(db, course_name)
	course=course_id.__dict__
	#print(course.upvotes)
	courseUpvote= course['upvotes']
	print(type(courseUpvote))
	#course_upvote = db.query(models.Courses).filter(models.Courses.id == course_id).update({'models.Courses.upvotes': models.Courses.upvotes + 1})
	course_upvote = db.query(models.Courses).filter(models.Courses.id == course_id.id).update({'upvotes': courseUpvote + 1})
	db.commit()
	return course_upvote
	
def downvote_course(db: Session, course_name: str):
	"""
 	Function for Downvoting a Course
 	course_id: To upvote a course we need a course_id, So, retrieved the course_details by calling the
 	function "get_course" got the coursedetails as object and
 	course: converted it to a dict
 	courseDownvote: retrieved the downvotesvotesin a course details from course
 	course_down_vote: returns the query with courses class in models and filter the course_id in models wit course_id
 	and update for every button clicks
	"""
	course_id = get_course(db, course_name)
	course=course_id.__dict__
	#print(course.upvotes)
	courseDownvote= course['downvotes']
	#$print(type(courseUpvote))
	#course_upvote = db.query(models.Courses).filter(models.Courses.id == course_id).update({'models.Courses.upvotes': models.Courses.upvotes + 1})
	course_down_vote = db.query(models.Courses).filter(models.Courses.id == course_id.id).update({'downvotes': courseDownvote - 1})
	db.commit()
	return course_down_vote
	
def create_course_feedback(db: Session, course_id: int, feed: schemas.Questions):
	'''
	Input is feed: from Question class in schemas.py(validation model)
	i.e., the inputs we are going to give in Ui
    '''

	feedback_details = models.Questions(course_id = course_id, Question_1= feed.Question_1, Question_2= feed.Question_2, Question_3= feed.Question_3, upvotes = 0, downvotes = 0)
	db.add(feedback_details)
	db.commit()
	db.refresh(feedback_details)
	return feedback_details


def get_feed_by_course(db: Session, course_name: str):
	"""
	function returns the questions or feed by issuing the course name
	course_id:for course_id, called the function of "get_course by giving the i/p parameters
	db, course_name" and retrive the id of a course
	then queries the Questions class in Model if course_id of Questions matches to the course_id(parameter)_id. If it is, returns all which it matches
	"""
	course_id = get_course(db, course_name).id
	return db.query(models.Questions).filter(models.Questions.course_id == course_id).first()

def upvoteFeedback(db: Session, course_name: str, questions: int):
	course_id = get_course(db, course_name).id
	print(course_id)
	question_id = get_feedback(db, course_id)
	print(question_id)
	feed = question_id.__dict__
	print(feed)
	feedUpvote= feed['upvotes']
	print(feedUpvote)
	feedbackupvote = db.query(models.Questions).filter(models.Questions.course_id == question_id).update({'upvotes': feedUpvote + 1 })
	db.commit()
	return feedbackupvote


def authenticate_user_email(db: Session, email: str):
    """
    useful when authenticating email to identify if the user is already present or not
    """
    details = db.query(models.Users).filter(or_(models.Users.name == email, models.Users.email == email)).first()
    print("the authenticated user email is...")
    print(details.__dict__)
    return details

def update_user_password(db: Session, Email, new_password_schema):
    try:
        details = db.query(models.Users).filter(Users.email == Email).update({'password': new_password_schema})
        db.commit()
        return True
    except:
        return False


def change_user_password(db: Session, Email, new_password_schema):
    try:
        details = db.query(models.Users).filter(Users.email == Email).update({'password': new_password_schema, 'recovered_yn': True, 'recovery_password':''})
        db.commit()
        return True
    except:
        return False


def update_code(db: Session, email, code):
    db.query(models.Users).filter(Users.email == email).update({'recovery_password':code, 'recovered_yn': False})
    db.commit()


def get_code(db: Session, email):
    code = db.query(models.Users).filter(and_(Users.email == email, Users.recovered_yn == False)).first()
    code = code.recovery_password
    return code


def get_recovery_status(db:Session, email):
    code = db.query(models.Users).filter(Users.email == email).first()
    code = code.recovered_yn
    return code


def authenticate_user_username_password(db: Session, username: str,password: str):
    """
    Authenticate user using username and password
    """
    get_my_details = get_user(db, username).first()
    if get_my_details is not None:
        my_username = get_my_details.name
        my_password = get_my_details.password
        print(my_password, password)
        if my_password == password:
            return get_my_details.__dict__
        else:
            return HTTPException(status=status.HTTP_500_NOT_FOUND, details='wrong password')
    else:
        return HTTPException(status=status.HTTP_404_NOT_FOUND, details='username not found')

def get_courses_by_username(db: Session, user_id: int):
	return db.query(models.Courses).filter(models.Courses.created_by == user_id).with_entities(Courses.course_name).all()

def get_domain_id_by_name(db:Session, domain_name: int):
	return db.query(models.Domain).filter(models.Domain.domain_name == domain_name).with_entities(Domain.id).first()

# def get all_domains(db: Session, )


def delete_questions(db:Session, question_id: int):
	return db.query(models.Questions).filter(models.Questions.id == question_id).delete()


def delete_course(db: Session, course_name: str):
	course_detail = db.query(models.Courses).filter(models.Courses.course_name==course_name).first()
	if course_detail is None:
		qrl.log_exception(logging, status.HTTP_404_NOT_FOUND)
		return HTTPException(status.HTTP_404_NOT_FOUND)
	else:
		print(course_detail.id)
		db.delete(course_detail)
		del_quest = db.query(models.Questions).filter(models.Questions.id == course_detail.id).delete()

	if del_quest is None:
		qrl.log_exception(logging, status.HTTP_404_NOT_FOUND)
		return HTTPException(status.HTTP_404_NOT_FOUND)
	else:
		course_detail = db.commit()
	return status.HTTP_200_OK


