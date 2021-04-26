from sqlalchemy.orm import Session
import crud, models, schemas
import uvicorn
from database import SessionLocal, engine
from fastapi import Request, APIRouter, FastAPI, Depends
import time, ast
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import load_only
# from fastapi_pagination import Page, pagination_params
# from fastapi_pagination.paginator import paginate





course_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###calling the db from the database###########
models.Base.metadata.create_all(bind=engine)

####creating the user API###
@course_router.post("/users", response_model=schemas.Users)
async def create_user(user: schemas.NewUser, db: Session = Depends(get_db)):
	'''
	path: create Users Page
	This api creates the user by calling the create_user function in crud.py
    '''
	insert_status = crud.create_user(db=db, user=user)
	print(insert_status)
	return insert_status.__dict__


####creating a Domain Request###
@course_router.post("/domains/create")
async def create_domain(domains: schemas.Domain_Create, db: Session = Depends(get_db)):
	'''
	path:domains/create
	inputes: domains: Domain_create class from schemas
	To create the domain this api calls the function "create_domain" where it creates the domains from the models.py
	and compared them with Domain_create in schemas 
	'''
	create = crud.create_domain(db, domains)
	return create


###create the Categories Request#####

@course_router.post('/{domain_name}/createcategory')
async def create_category(domain_name: str, cat_name: schemas.categories_create, db: Session = Depends(get_db)):
	'''
	Inputs: Domain_name and Create_CAtegories
	To create the Categories, need to get the domain_name first and then can create the category
	so to get the domain called the function " get_domain"
	to create the categoried called the function "create_categories"--> get the details categories_create in schemas

	'''

	domain_id = crud.get_domain(db, domain_name).id
	createcat = crud.create_categories(db, domain_id, cat_name)

	return createcat

@course_router.get("/userbase")#, response_model=List[schemas.Users])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    json_compatible_item_data = jsonable_encoder(users)
    print(users)
    return json_compatible_item_data

@course_router.get("/domains")
async def get_domains(domain_name: str, db: Session = Depends(get_db)):
	domain_names = crud.get_domain(db, domain_name)	
	return domain_names

@course_router.get("/domainbase")
async def all_domains(skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
	return crud.get_all_domains(db, skip = skip, limit = limit)

@course_router.get("/categorybase")
async def all_categories(skip: int = 0, db: SessionLocal = Depends(get_db)):
	result =  crud.get_all_categories(db, skip = skip)
	category_names = [category[0] for category in result]
	return category_names

####creating the Course requests######
@course_router.post('/{category}/createcourse')
async def create_course(category: str, course_name: schemas.NewCourses, db: Session = Depends(get_db)):
	'''
	POst request to insert the course details
	To post the Course details used the user_id and category_id
	for category called the function in crud file called get_category wich gets the details from categories class in model
	returns te result by calling te function"create_courses"

	'''
	category_id = crud.get_category(db, category).id
	print(category_id)
	user_id = crud.get_user(db, course_name.created_by).id
	course_create = crud.createCourses(db, category_id, user_id, course_name)
	return course_create

@course_router.get('/{category_name}/courses')
async def get_courses_by_name_category(category_name: str, db: Session = Depends(get_db)):
	"""
	function return the courses related to the category name by calling the function "get_courses_by_category_name"
	in crud file.
    
	"""
	category_courses = crud.get_courses_by_category_name(db,category_name)
	#print(category_courses)
	# for cat_course in category_courses:
	#     print(cat_course.course_tags)
	#     if isinstance(cat_course.course_tags, str):
	#         cat_course.course_tags = ast.literal_eval(cat_course.course_tags)
	final_courses = []
	for cat_course in category_courses:
		#course = list(cat_course)#.__dict__
		#print(course)
		temp = []
		temp.append(cat_course[0])
		temp.append(cat_course[1])
		temp.append(cat_course[3])
		temp.append(cat_course[2][1:-1].replace("'",'').split(', '))
		# temp[2] = temp[2][1:-1].replace("'",'').split(', ')
		final_courses.append(temp)
	return final_courses

@course_router.get('/{domain_name}/categories')
async def get_categories_by_name_domain(domain_name: str, db: Session = Depends(get_db)):
	"""
	function return the categories related to the domain name by calling the function "get_categories_by_domain_name"
	in crud file.
    
	"""
	domain_categories = crud.get_categories_by_domain_name(db, domain_name)
	category_names = [category[0] for category in domain_categories]
	return category_names

# @course_router.get('/{domain}/categories')
# def getCategories_of_domain(domain : str, db:Session = Depends(get_db)):
# 	return crud.categories_by_domains(db, domain)

@course_router.post('/{course_name}/upvote')
async def course_upvotes(course_name:str, db: Session = Depends(get_db)):
	"""
	Function returns the upvotes for a course 
	queries the api by calling the function"upvote_course"in crud
	"""
	courseupvote = crud.upvote_course(db, course_name)
	return {'votesCount':courseupvote }

@course_router.get('/{course_name}/upvotes')
async def get_course_upvotes(course_name:str , db: Session = Depends(get_db)):
	courseUpvotes = crud.get_upvotes(db, course_name)
	return {'upvotes':courseUpvotes[0]}

@course_router.post('/{course_name}/downvote')
async def course_downvote(course_name: str, db: Session = Depends(get_db)):
	"""
	Function returns the downvotes for a course 
	queries the api by calling the function"downvote_course"in crud
	"""
	coursedownvote = crud.downvote_course(db, course_name)
	return {'votesCount':coursedownvote - 1}

@course_router.get('/{course_name}/downvote')
async def get_course_downvotes(course_name:str, db:Session = Depends(get_db)):
	coursedownvote = crud.get_downvotes(db, course_name)
	return {'downvotes': coursedownvote[0]}


@course_router.post('/{course_name}/questions')
async def create_questions(course_name: str, question: schemas.Questions, db: Session = Depends(get_db)):
	course_id = crud.get_course(db, course_name).id
	questions = crud.create_course_feedback(db, course_id, question)
	return questions

@course_router.get('/{course_name}/feedback')
async def get_feedback_by_course(course_name: str, db: Session = Depends(get_db)):
	course_feedback= crud.get_feed_by_course(db, course_name)
	return course_feedback


@course_router.post('/{course_name}/{questions}/upvote')
async def feedback_upvote(course_name: str, questions: str, db: Session= Depends(get_db)):
	feedbackUpvote= crud.upvoteFeedback(db, course_name, questions)
	print(feedbackUpvotes)
	return feedbackUpvote

@course_router.post('/courses/delete/{course_name}')
async def del_course_name(course_name: str, db: Session= Depends(get_db)):
	return crud.delete_course(db, course_name = course_name)

@course_router.post('questions/delete/{question_id}')
async def dele_questions(question_id: int, db: Session=Depends(get_db)):
	return crud.delete_questions(db, question_id = question_id)


@course_router.post('/{category_name}/courses')
async def get_courses_by_filter(category_name: str, filters: schemas.CourseFilters, db: Session=Depends(get_db)):

	
	# print(domain_name, category_name)
	# domainID = crud.get_domain(db, domain_name).id
	categoryID = crud.get_category(db, category_name).id
	# print(domainID, categoryID)
	# print(filters.__dict__)
	course_ids = []
	mode_result, level_result, medium_result = crud.get_course_by_filter(db, category_name, filters)
	
	# print(len(mode_result),len(level_result),len(medium_result))
	if mode_result not in ['', None]:
		if len(course_ids) ==0:
			course_ids = [result[0] for result in mode_result]
		else:
			mode_result = [course_ids[i] for i in range(len(course_ids)) if course_ids[i] in mode_result]
	#print(len(course_ids))
	#print(course_ids)


	if level_result not in ['', None]:
		level_result = [result[0] for result in level_result]
		# print(level_result)
		# print(course_ids)
		if len(course_ids) == 0:
			course_ids = level_result
		else:
			course_ids = [course_ids[i] for i in range(len(course_ids)) if course_ids[i] in level_result]
		
		#print(len(course_ids))


	if medium_result not in ['', None]:
		medium_result = [result[0] for result in medium_result]
		if len(course_ids) == 0:
			course_ids = medium_result
		else:
			course_ids = [course_ids[i] for i in range(len(course_ids)) if course_ids[i] in medium_result]
		
		#print(len(course_ids))

	all_courses = crud.get_courses_by_course_id(db, course_ids)
	#print(course_ids)
	final_courses = []
	for course in range(len(all_courses)):
		temp = []
		temp.extend(all_courses[course][0:])
		temp[2] = temp[2][1:-1].replace("'",'').split(', ')
		final_courses.append(temp)

	



	return final_courses


