import pandas as pd
import os
from sqlalchemy.orm import Session
import crud, models, schemas
import uvicorn
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Users, Courses, Categories, Domain
import csv 	
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime




SQLALCHEMY_DATABASE_URL = "postgres://tugrefnkrtbjvk:7d4c031048e0e5908f90135605bda7964d85c37a1f87a5f04871dbe2d9a19af3@ec2-54-237-143-127.compute-1.amazonaws.com:5432/das7sc8jfhka1q"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

for filename in os.listdir('E://coursewebsite/website/application/data-science/'):
	print(filename)
	if filename.endswith('.csv'):
		# with open('E://coursewebsite/website/application/programming/' + filename, mode='r') as curr_file:
		# 	print(curr_file)
		#df = pd.read_csv(curr_file)
		file_name = filename.split('_')[-2]
		print(file_name)
		df = pd.read_csv('E://coursewebsite/website/application/data-science/'+filename)
		
		df.columns=["course_name",
			"course_link",
			"course_source",
			"course_tags"]
		cat_id = crud.get_category(db, file_name).id
		user_id = crud.get_user(db, 'Ravi').id
		for index, data in df.iterrows():
			# print(data.course_name)
			# print(data.course_link)
			# print(data.course_source)
			# print(data.course_tags)
			db_record = models.Courses(categories_id = cat_id, created_by = user_id, course_name = data.course_name, course_link = data.course_link,
				course_source = data.course_source, course_tags = data.course_tags)

			db.add(db_record)
		db.commit()
	db.close()


		


