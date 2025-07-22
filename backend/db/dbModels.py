#################################################################
#                     SQLAlchemy Models                         #
#################################################################

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

# Model for templates table
class DBTemplate(Base):
    __tablename__ = "templates"

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String)
    fight = Column(String)
    user = Column(String)
    description = Column(String, nullable=True)
    bookmarks = Column(Integer, default=0)
    views = Column(Integer, default=0)

    def __repr__(self):
        return f"<DBTemplate(id='{self.id}', name='{self.name}')>"

# Model for Encounters
class DBEncounter(Base):
    __tablename__ = "Encounters" 

    Id = Column(Integer, primary_key=True, autoincrement=True)
    tier = Column("tier", String)
    shorthand = Column(String(255), unique=True, index=True)
    boss = Column(String)
    imgLink = Column("imglink", String)
    def __repr__(self):
        return f"<DBEncounter(Id={self.Id}, shorthand='{self.shorthand}', tier='{self.tier}')>"
    
# model for oauth user
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    google_sub = Column(String(255), unique=True, nullable=True)
    username = Column(String(255), unique=True) # If username is always required, keep nullable=False (default)
    email = Column(String(255), unique=True) 
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"