from sqlalchemy import Column, Integer, String, Float
from database import Base

class Password(Base):
	__tablename__ = 'passwords'

	id = Column(Integer, primary_key=True, autoincrement=True)
	password = Column(String, nullable=False, unique=True)
	hashed_password = Column(String, nullable=True, unique=True)
	service_name = Column(String, nullable=True, index=True)