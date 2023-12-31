from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "api_posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    # created_at = Column(
    #     TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    # )
    created_at = Column(String, nullable=False)
    owner_id = Column(
        Integer,
        ForeignKey(column="api_users.id", ondelete="CASCADE"),
        nullable=False,
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "api_users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
