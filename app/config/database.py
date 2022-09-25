from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root:mahicircle@192.168.0.140:3306/mahicircle'         #local docker

SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root:mahicircle@3.111.232.15:3306/mahicircle'        #aws docker

# SQLALCHEMY_DATABASE_URL='mysql+mysqlconnector://root@localhost:3306/mahicircle'                      #localhost

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()