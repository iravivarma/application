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
	user_id = crud.get_users(db, course_name.created_by)
    