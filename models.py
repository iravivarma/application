from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@localhost:5432/course_website"

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
	is_active = Column(Boolean, default=True)
	joined_on = Column(Integer, index = True)

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
	created_date = Column(Integer, index = True)

	domain_type = relationship("Domain", back_populates="cat_type")
	cat_courses = relationship("Courses", back_populates="course_cat")



class Courses(Base):
	__tablename__ = "courses"

	id = Column(Integer, primary_key =True, index =  True)
	categories_id = Column(Integer, ForeignKey("categories.id"))
	created_by = Column(Integer, ForeignKey("users.id"))
	course_name = Column(String, index = True)
	course_source = Column(String)
	course_link = Column(String, index = True)
	description = Column(String)
	course_type = Column(String)
	course_medium = Column(String)
	level = Column(String)
	views = Column(Integer)
	upvotes = Column(Integer, default = 0)
	downvotes = Column(Integer, default = 0)

	course_cat = relationship("Categories", back_populates="cat_courses")
	course_users = relationship("Users", back_populates="user_course")
	courses_feed = relationship("Questions", back_populates = "feed_on_courses")


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