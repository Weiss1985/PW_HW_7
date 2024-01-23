from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

username = 'postgres'
password = '12345'
host = 'localhost'
dbname = 'postgres'
database_url = f"postgresql+psycopg2://{username}:{password}@{host}/{dbname}"

engine = create_engine(database_url)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
    tables = Base.metadata.tables.keys()
    for table_name in reversed(list(tables)):
        logger.info(f"Executing table {table_name}")
        session.execute(text(f"DELETE FROM {table_name}"))
    session.commit()

logger.info("All table execute.")
