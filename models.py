from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

class MediaItem(Base):
    __tablename__ = 'media_items'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(Text)
    content = Column(Text)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_engine():
    url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(url)

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

