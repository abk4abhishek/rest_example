from sqlalchemy import Column, ForeignKey, Integer, String, null

from ..database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)


Base.metadata.create_all(bind=engine)
