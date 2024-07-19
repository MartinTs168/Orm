from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, Relationship
from decouple import config

DB_NAME = config("DB_NAME")
USER = config("USER")
PASSWORD = config("PASSWORD")

# variable = <dialect>+<drivers>://<username>:<password>@<host>:<port>/<database>
CONNECTION_STRING = f"postgresql+psycopg2://{USER}:{PASSWORD}@localhost:5432/{DB_NAME}"

engine = create_engine(CONNECTION_STRING)
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    chef_id = Column(Integer, ForeignKey('chefs.id'))
    chef = Relationship(
        'Chef',
        back_populates='recipes'
    )


class Chef(Base):
    __tablename__ = 'chefs'

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    recipes = Relationship('Recipe', back_populates='chef')

