from sqlalchemy.orm import Session
import crud, models, schemas
import uvicorn
from database import SessionLocal, engine
from fastapi import Request, APIRouter, FastAPI, Depends
import time





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
    
    insert_status = crud.create_user(db=db, user=user)
    print(insert_status)
    return insert_status.__dict__


####creating a Domain Request###
@course_router.post("/domains/create")
async def create_domain(domains: schemas.Domain_Create, db: Session = Depends(get_db)):
	create = crud.create_domain(db, domains)
	return create


###create the Categories Request#####

@course_router.post('/{domain_name}/createcategory')
async def create_category(domain_name: str, cat_name: schemas.categories_create, db: Session = Depends(get_db)):

	domain_id = crud.get_domain(db, domain_name).id
	createcat = crud.create_categories(db, domain_id, cat_name)

	return createcat

####creating the Course requests######
@course_router.post('/{category}/createcourse')
async def create_course(category: str, course_name: schemas.NewCourses, db: Session = Depends(get_db)):
	category_id = crud.get_category(db, category).id
	print(category_id)
	user_id = crud.get_user(db, course_name.created_by).id
	course_create = crud.createCourses(db, category_id, user_id, course_name)
	return course_create

@course_router.get('/{category_name}/courses')
async def get_courses_by_name_category(category_name: str, db: Session = Depends(get_db)):
	category_courses = crud.get_courses_by_category_name(db,category_name)
	return category_courses