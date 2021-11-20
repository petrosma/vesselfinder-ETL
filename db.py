from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./vessels.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#SQLALCHEMY_DATABASE_URL = "mysql://Ln1ki1vjdf:2hMrrqsHGn@remotemysql.com/Ln1ki1vjdf"
#SQLALCHEMY_DATABASE_URL = "postgres://645297:173238235@localhost/WIMS"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
