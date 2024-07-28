from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

'''
SQLITE
'''

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./predictions.db'

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

'''
POSTGRES
'''

# SQLALCHEMY_DATABASE_URL = 'postgresql://hask777:lara@localhost:5432/football'

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

'''
MYSQL
'''

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@127.0.0.1:3306/bybit'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()