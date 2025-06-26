from models import Exam,Subject
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASEURL=settings.database_url
engine=create_engine(DATABASEURL)
SessionLocal=sessionmaker(bind=engine)
session=SessionLocal()
exam=session.query(Exam).filter(Exam.id==1).first()
print(exam.subjects)

for subject in exam.subjects:
    print(exam.intro)
    print(subject.name)











