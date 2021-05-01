from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@localhost:5432/course_website"
SQLALCHEMY_DATABASE_URL = "postgres://tugrefnkrtbjvk:7d4c031048e0e5908f90135605bda7964d85c37a1f87a5f04871dbe2d9a19af3@ec2-54-237-143-127.compute-1.amazonaws.com:5432/das7sc8jfhka1q"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Users(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True, index = True)
	name = Column(String, index = True)
	email = Column(String, unique = True, index = True)
	password = Column(String)
	active_yn = Column(Boolean, default=True)
	joined_on = Column(String, index = True)
	recovery_password = Column(String, default = '')
	recovery_yn = Column(Boolean, default = True)      

	user_course = relationship("Courses", back_populates="course_users")



class Domain(Base):
	__tablename__ = "domains"
	id = Column(Integer, primary_key = True, index = True)
	domain_name = Column(String, index = True)

	cat_type = relationship("Categories", back_populates="domain_type")


class Categories(Base):
	__tablename__  = "categories"

	id = Column(Integer, primary_key = True, index = True)
	domain_id =Column(Integer, ForeignKey("domains.id"), index = True)
	name = Column(String, index = True)
	created_date = Column(String, index = True)

	domain_type = relationship("Domain", back_populates="cat_type")
	cat_courses = relationship("Courses", back_populates="course_cat")
	cat_ids = relationship("filters", back_populates = "courseFilters")



class Courses(Base):
	__tablename__ = "courses"

	id = Column(Integer, primary_key =True, index =  True)
	categories_id = Column(Integer, ForeignKey("categories.id"))
	created_by = Column(Integer, ForeignKey("users.id"))
	course_name = Column(String, index = True)
	course_source = Column(String) 
	course_link = Column(String, index = True)
	description = Column(String, default = '')
	course_tags = Column(JSON)
	#level = Column(String)######give datatype Level
	views = Column(Integer, default = 0)
	upvotes = Column(Integer, default = 0)
	downvotes = Column(Integer, default = 0)


	course_cat = relationship("Categories", back_populates="cat_courses")
	course_users = relationship("Users", back_populates="user_course")
	courses_feed = relationship("Questions", back_populates = "feed_on_courses")
	course_filter = relationship("filters", back_populates = "course_filters")


class filters(Base):
	__tablename__ = "filter_tags"
	id = Column(Integer, primary_key=True, index = True)
	course_id = Column(Integer, ForeignKey("courses.id"))
	category_id = Column(Integer, ForeignKey("categories.id"))
	category=Column(String) #course_medium, Course_level, Course_mode
	c_type= Column(String)#[pdf, book, video], [beginner, intermediate, Advanced], [free,paid]


	course_filters = relationship("Courses", back_populates = "course_filter")
	courseFilters = relationship("Categories", back_populates ="cat_ids" )



class Questions(Base):
	__tablename__ = "feedback"

	id = Column(Integer, primary_key=True, index = True)
	course_id = Column(Integer, ForeignKey("courses.id"))
	Question_1 = Column(Integer)
	Question_2 = Column(Integer)
	Question_3 = Column(Integer)
	upvotes = Column(Integer, default = 0)
	downvotes = Column(Integer, default = 0)

	feed_on_courses =relationship('Courses', back_populates= "courses_feed")






    


Users.__table__.create(bind=engine, checkfirst=True)
Domain.__table__.create(bind=engine, checkfirst=True)
Categories.__table__.create(bind=engine, checkfirst=True)
Courses.__table__.create(bind=engine, checkfirst=True)
Questions.__table__.create(bind=engine, checkfirst=True)
filters.__table__.create(bind = engine, checkfirst = True)