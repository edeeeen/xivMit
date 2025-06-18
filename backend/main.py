#################################################################
#                         FastAPI functions                     #
#################################################################

from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
import json
import db as dbConnection
import parameters as p
import os
import pyodbc
import logging

connection_string = ""
app = FastAPI()

# Allowed origins by CORS
origins = [
    "http://localhost:5173",
    "https://sleepycat.me"
]

# Allow API to be used at different hosts named by origins variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



# Startup function
# Init db connection and create db object
@app.on_event("startup")
async def startup_event():
    # if on azure then this will get the db credentials from the enviornment variable
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
                    logging.info(f"Connection string constructed from cred.json")
                else:
                    # Raise error if not all db creds are found
                    logging.info(f"Error: Missing one or more required credentials (server, database, username, password) in cred.json.")
                    raise ValueError("Missing database credentials for startup.")
        except FileNotFoundError:
            logging.info(f"Error: creds.json not found.")
            raise FileNotFoundError("creds.json missing for database connection.")
        except json.JSONDecodeError:
            logging.info(f"Error: creds.json is not valid JSON.")
            raise ValueError("Invalid JSON in creds.json.")
        except Exception as e:
            logging.info(f"An unexpected error occurred during creds.json processing: {e}")
            raise Exception(f"Failed to process creds.json: {e}")
        # Check that connection_string was found properly and make connection
        if connection_string:
            try:
                # Establish db connection
                db_connection_object = pyodbc.connect(connection_string)
                logging.info("Successfully established pyodbc connection.")
                
                # Create db object and pass connection
                app.db = dbConnection.db(db_connection_object)
                logging.info("DB handler instance created and stored on app.db.")
            except pyodbc.Error as ex:
                logging.info(f"ODBC Error during database connection: {ex}")
                raise HTTPException(status_code=500, detail="Database connection error during startup.")
            except Exception as e:
                logging.info(f"General Error during startup connection: {e}")
                raise HTTPException(status_code=500, detail="Application startup failed due to database error.")
        else:
            logging.info("No valid connection string found. Cannot establish DB connection for startup.")
            raise HTTPException(status_code=500, detail="No database connection string provided for startup.")

# Function runs on shutdown
# Close db connection
@app.on_event("shutdown")
async def shutdown_event():
    # Ensure the connection object exists before trying to close it
    if hasattr(app, 'db') and hasattr(app.db, 'cnxn') and app.db.cnxn:
        app.db.cnxn.close()
        print("Database connection closed during shutdown.")



# Test function for the API
@app.get("/api")
def read_root():
    return {"Hello": "World"}


# returns a list of encounters and their properties
# sorted newest to oldest
# could be worth getting xivapi to do this so it auto updates
# Might not be worth using db for this at all since it update so infrequently and its small
@app.get("/api/getEncounters")
def getEncounters():
    # Check db connection is good
    if not hasattr(app, 'db'):
        raise HTTPException(status_code=500, detail="Database handler not initialized during startup.")
    
    # Get encounters from db
    results = app.db.getEncounters() # This will now call the method on the correct instance
    transformed_output = {}

    # Format output json and remove whitespace
    for encounter in results:
        # Get tier and strip whitespace
        tier = encounter.get("tier")
        if tier and isinstance(tier, str):
            tier = tier.strip()

        if tier:
            # Create a dictionary for the current encounter's details, stripping whitespace
            encounter_details = {
                "shorthand": encounter.get("shorthand").strip() if isinstance(encounter.get("shorthand"), str) else encounter.get("shorthand"),
                "boss": encounter.get("boss").strip() if isinstance(encounter.get("boss"), str) else encounter.get("boss"),
                "imgLink": encounter.get("imgLink").strip() if isinstance(encounter.get("imgLink"), str) else encounter.get("imgLink")
            }
            # If the tier is not yet a key in the transformed_output, add it
            if tier not in transformed_output:
                transformed_output[tier] = []
            # Append the encounter details to the list for the corresponding tier
            transformed_output[tier].append(encounter_details)
    
    return transformed_output
    '''return {
        "Cruiserweight":[
            {
                "shorthand" : "M5S",
                "boss" : "Dancing Green",
                "imgLink" : "m5s.png"
            },
            {
                "shorthand" : "M6S",
                "boss" : "Sugar Riot",
                "imgLink" : "m6s.png"
            },
            {
                "shorthand" : "M7S",
                "boss" : "Brute Abominator",
                "imgLink" : "m7s.png"
            },
            {
                "shorthand" : "M8S",
                "boss" : "Howling Blade",
                "imgLink" : "m8s.png"
            }
        ],
        "Light-Heavyweight":[  
            {
                "shorthand" : "M1S",
                "boss" : "Black Cat",
                "imgLink" : "m1s.png"
            }, 
            {
                "shorthand" : "M2S",
                "boss" : "Honey Bee Lovely",
                "imgLink" : "m2s.png"
            },
            {
                "shorthand" : "M3S",
                "boss" : "Brute Bomber",
                "imgLink" : "m3s.png"
            },
            {
                "shorthand" : "M4S",
                "boss" : "Wicked Thunder",
                "imgLink" : "m4s.png"
            }
        ]
    }'''

# Unimplemented
# Returns templates for specific encounter
# Calls db.getTemplates() 
@app.get("/api/getTemplates/{fight}")
def getTemplates(fight: p.encounterNames):
    app.db.getTemplates(fight)
    return {"test" : fight}
