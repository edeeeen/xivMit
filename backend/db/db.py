import os
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
import logging
import json
import urllib
from .dbModels import *

logger = logging.getLogger(__name__)

load_dotenv()

connection_string = os.environ.get('SQL_CONNECTION_STRING')
# Check if env variable is found or not
if connection_string is None:
    try:
        # Try to open creds.json and read db connection string
        with open('creds.json', 'r') as file:
            credentials = json.load(file)
            server = credentials.get('server')
            database = credentials.get('database')
            uid = credentials.get('username')
            pwd = credentials.get('password')
            # If everything is found in creds.json then create connection string
            if server and database and uid and pwd:
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={uid};"
                    f"PWD={pwd};"
                    f"Encrypt=yes;"
                    f"TrustServerCertificate=no;"
                    f"Connection Timeout=30;"
                )
                logger.info(f"Connection string constructed from cred.json")
            else:
                # Raise error if not all db creds are found
                logger.error(f"Error: Missing one or more required credentials (server, database, username, password) in cred.json.")
                raise ValueError("Missing database credentials for startup.")
    except FileNotFoundError:
        logger.error(f"Error: creds.json not found.")
        raise FileNotFoundError("creds.json missing for database connection.")
    except json.JSONDecodeError:
        logger.error(f"Error: creds.json is not valid JSON.")
        raise ValueError("Invalid JSON in creds.json.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during creds.json processing: {e}")
        raise Exception(f"Failed to process creds.json: {e}")
    
# Check that connection_string was found properly and make connection
if connection_string:
    # parse string for sqlalchemy
    connection_string_encoded = urllib.parse.quote_plus(connection_string)
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={connection_string_encoded}"
    
    
    
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True # Shows SQL statements in console, might want to turn off for release
    )
    logger.info("db handler instance created")
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    logger.info("Created tables")
else:
    logger.error("No valid connection string found. Cannot establish db connection")
    raise RuntimeError("No valid db connection string found")
    



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger.info("DB handler instance created.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
