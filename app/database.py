from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# # Base de datos local
# SQLALCHEMY_DATABASE_URL = 'postgresql://sismosu:123@localhost:5432/sismosdb'
# # SQLALCHEMY_DATABASE_URL = "sqlite:///./sismos.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Base de datos Cloud
engine = create_engine('postgresql://earthdata:PAyGeCDZPbqYqGWKaUofHW2JTolrSB8S@dpg-ce9vl3p4reb52up9aol0-a.oregon-postgres.render.com/sismosearthdata', pool_size=50, max_overflow=0) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()