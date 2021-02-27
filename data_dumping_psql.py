#import pandas as pd
from sqlalchemy.orm import Session
import crud, models, schemas
import uvicorn
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Users, Courses, Categories, Domain
import csv 	
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import time




SQLALCHEMY_DATABASE_URL = "postgres://tugrefnkrtbjvk:7d4c031048e0e5908f90135605bda7964d85c37a1f87a5f04871dbe2d9a19af3@ec2-54-237-143-127.compute-1.amazonaws.com:5432/das7sc8jfhka1q"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

##########################################################################################################################
# domain = pd.read_csv('E:/website/testing/Domains.csv')
# print(type(domain))

# domain_dict = domain.to_dict('records')
# print(domain_dict[0].keys())


# ####output of area dict[{'domain_name': 'programming'}, {'domain_name': 'data-science'}, {'domain_name': 'devops'}, {'domain_name': 'design'}]


# domain_names = [names['domain_name'] for names in domain_dict]

# print(domain_names)


# for names in domain_dict:
# 	print(names)



# 	crud.create_domain(Session, names['domain_name'])

db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

with open('E://coursewebsite/website/application/Domains.csv', "r") as f:
	csv_reader = csv.DictReader(f)	

	for row in csv_reader:
		print(row)
		time.sleep(1)
		db_record = models.Domain(
			domain_name = row["domain_name"])

		db.add(db_record)

	db.commit()

db.close()

with open("E://coursewebsite/website/application/design-categories.csv", "r") as f:
	csv_reader = csv.DictReader(f)
	domain_id = crud.get_domain_id_by_name(db, 'design').id
	print(domain_id)
	print(type(domain_id))
	today = datetime.datetime.now()
	print(today)
	print(type(today))
	for row in csv_reader:
		print(row)
		# time.sleep(1)

		db_record = models.Categories(name = row["name"], domain_id = domain_id, created_date = str(today))

		db.add(db_record)
	db.commit()

db.close()	




