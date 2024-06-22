from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dependencies.authenticator import Settings

# create object for DB settings
settings = Settings()
# used to construct the database connection URL
DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}/"
    f"{settings.POSTGRES_DATABASE}"
)

# used to create a database engine
# the engine manages the database connection.
# The echo=True argument is optional and is often used for debugging purposes (turned off)
engine = create_engine(DATABASE_URL)

# used to create a models (tables) based on an object-oriented approach
Base = declarative_base()

# Manages information about the database schema
metadata = MetaData()

# used to manage database sessions for your application
SessionLocal = sessionmaker(bind=engine)
