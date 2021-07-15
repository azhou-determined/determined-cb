
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from app import app

uri = f'postgresql://{app.config["DB_USER"]}:{app.config["DB_PASSWORD"]}@{app.config["DB_HOST"]}:{app.config["DB_PORT"]}/{app.config["DB_NAME"]}'
engine = create_engine(uri, echo=True)
Session = scoped_session(sessionmaker(engine, expire_on_commit=False))
Base = declarative_base()


def init_schema():
    import model
    Base.metadata.create_all(bind=engine)
