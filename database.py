from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
db_url="mysql+pymysql://root:Inter1906@localhost:3306/urbaneye"
engine=create_engine(db_url)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

