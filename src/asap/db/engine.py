from sqlmodel import SQLModel, create_engine

db_engine = create_engine('sqlite:///asap.db')

def create_db_tables():
    SQLModel.metadata.create_all(db_engine)
