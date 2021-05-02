
######################file to push the coureses ans filtertags to database################################

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
import ast



#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@localhost:5432/course_website"

SQLALCHEMY_DATABASE_URL = "postgres://tugrefnkrtbjvk:7d4c031048e0e5908f90135605bda7964d85c37a1f87a5f04871dbe2d9a19af3@ec2-54-237-143-127.compute-1.amazonaws.com:5432/das7sc8jfhka1q"
SQLALCHEMY_DATABASE_URL2 = "postgres://pdszntpmoaxibt:3bf9c2ecb5a8b51b0dec9099fee6277c6070117918489869ddec6dfe1f4e029c@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d9a6vbq4d0d2q8"

engine2 = create_engine(
    SQLALCHEMY_DATABASE_URL2
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()
db2 = SessionLocal2()



models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine2)


# for filename in os.listdir('C://Users//Ravi Varma Injeti/Desktop/hackrio/application/design/'):
# 	print(filename)
# 	if filename.endswith('.csv'):
# 		# with open('E://coursewebsite/website/application/programming/' + filename, mode='r') as curr_file:
# 		# 	print(curr_file)
# 		#df = pd.read_csv(curr_file)
# 		file_name = filename.split('_')[1]
# 		print(file_name)
# 		cat_name = file_name.split('-')
# 		name = cat_name[1:]
# 		category = '-'.join(name)
# 		df = pd.read_csv('C://Users//Ravi Varma Injeti/Desktop/hackrio/application/design/'+filename)
		
# 		df.columns=["course_name",
# 			"course_link",
# 			"course_source",
# 			"course_tags"]
# 		cat_id = crud.get_category(db, category).id
# 		user_id = crud.get_user(db, 'Ravi').id
# 		for index, data in df.iterrows():
# 			# print(data.course_name)
# 			# print(data.course_link)
# 			# print(data.course_source)
# 			# print(data.course_tags)
# 			db_record = models.Courses(categories_id = cat_id, created_by = user_id, course_name = data.course_name, course_link = data.course_link,
# 				course_source = data.course_source, course_tags = data.course_tags )

# 			db.add(db_record)
# 		db.commit()
# 	db.close()

def insert_filters(category_name):
	course_mode = ['Free', 'Paid'];
	course_level = ['Beginner', 'Intermediate', 'Advanced']
	course_medium = ['Book', 'pdf', 'video', 'Docs']
	for filename in os.listdir('C://Users//Ravi Varma Injeti/Desktop/hackrio/application/'+category_name+'/'):
		print(filename)
		if filename.endswith('.csv'):
			# with open('E://coursewebsite/website/application/programming/' + filename, mode='r') as curr_file:
			# 	print(curr_file)
			#df = pd.read_csv(curr_file)
			file_name = filename.split('_')[1]
			print(file_name)
			cat_name = file_name.split('-')
			name = cat_name[1:]
			category = '-'.join(name)
			print(category)
			df = pd.read_csv('C://Users//Ravi Varma Injeti/Desktop/hackrio/application/'+category_name+'/'+filename)
			
			df.columns=["course_name",
			"course_link",
 			"course_source","course_tags"]
			
			cat_id = crud.get_category(db, category).id
			
			for index, data in df.iterrows():
				# print(data.course_name)
				# print(data.course_link)
				# print(data.course_source)

				tags_list = data.course_tags[1:-1].split(', ')
				print(data.course_tags[1:-1])
				course_id = crud.get_course(db, data.course_name).id
				# for tags in tags_list:
				# 	tags = tags.replace(' ','')
				# 	print(tags)
				# 	print(str(tags) in course_mode)
				# 	print(tags,course_mode)
				# 	print(type(tags),type(course_mode))
				# 	print(str(tags) in course_level)
				# 	print(tags,course_level)
				# 	print(type(tags),type(course_level))
				# 	print(str(tags) in course_medium)
				# 	print(tags,course_medium)
				# 	print(type(tags),type(course_medium))
				# break;
				for tags in tags_list:
					tags = tags.replace(' ','').strip("'")
					print(tags)
					print(str(tags) in course_mode)
					print(course_mode)
					print(str(tags) in course_level)
					print(course_level)
					print(str(tags) in course_medium)
					print(course_medium)

					medium = False
					level = False
					mode = False


					for i in course_mode:
						print("Comparing %r with %r" % (str(i), str(tags)))

						if str(i) == str(tags):
							mode = True
							break

					for i in course_level:
						print("Comparing %r with %r" % (str(i), str(tags)))
						if str(i) == str(tags):
							level = True
							break

					for i in course_medium:
						print("Comparing %r with %r" % (str(i), str(tags)))
						if str(i) == str(tags):
							medium = True
							break


					print(mode)
					print(level)
					print(medium)
					if mode == True:
						db_record = models.filters(course_id = course_id, category_id = cat_id, category = 'course_mode',
					c_type = tags)

					
					elif level == True:
						db_record = models.filters(course_id = course_id, category_id = cat_id, category= 'course_level',
					c_type = tags)

					
					else:
						db_record = models.filters(course_id = course_id, category_id = cat_id, category= 'course_medium',
					c_type = tags)



					# for tags in course_mode:
					# 	print("course_mode")
					# 	course_mode = True
					# 	if course_mode ==
					# 	db_record = models.filters(course_id = course_id, category_id = cat_id, category = 'course_mode',
					# 		c_type = tags)

					# elif tags in course_level:
					# 	print("course_level")
					# 	db_record = models.filters(course_id = course_id, category_id = cat_id, category= 'course_level',
					# 		c_type = tags)

					# else:
					# 	print("course_medium")
					# 	db_record = models.filters(course_id = course_id, category_id = cat_id, category= 'course_medium',
					# 		c_type = tags)
					
					# db_record = models.filter_tags(course_id = data.course_id, category_id = data.category_id, course_tags = data.course_tags)
					db2.add(db_record)
				db2.commit()
		db2.close()
	db.close()







		
files = insert_filters('data-science')	
print(files)

