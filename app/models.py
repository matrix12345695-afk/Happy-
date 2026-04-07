from sqlalchemy import Column, Integer, BigInteger, String, Date, TIMESTAMP
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    birth_date = Column(Date)
    chat_id = Column(BigInteger)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
