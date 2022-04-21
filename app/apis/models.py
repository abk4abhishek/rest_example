from sqlalchemy import Column, ForeignKey, Integer, String, null
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    access_code = Column(Integer, server_default="001")
    created_on = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

Base.metadata.create_all(bind=engine)