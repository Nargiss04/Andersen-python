from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/tasks_db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))
