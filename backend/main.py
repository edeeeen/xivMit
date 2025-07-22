#################################################################
#                         FastAPI functions                     #
#################################################################

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows, OAuthFlowAuthorizationCode, OAuthFlowPassword

from contextlib import asynccontextmanager # Import asynccontextmanager
from enum import Enum
import json
import os
import logging
from routers.auth.auth import router as auth_router 
from starlette.middleware.sessions import SessionMiddleware 
from typing import Optional, List, Dict
from dotenv import load_dotenv

import model
import db.dbModels as dbModels
from db.db import db_dependency
import parameters as p

load_dotenv()

connection_string = ""

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
if SESSION_SECRET_KEY is None:
    raise Exception("SESSION_SECRET_KEY environment variable not set. Please add it to your .env file.")

SECRET_KEY = os.getenv("SECRET_KEY") # Ensure this is loaded if not already in services.py check
if SECRET_KEY is None:
    raise Exception("SECRET_KEY environment variable not set. Please add it to your .env file.")

bearer_scheme = HTTPBearer(
    description="Bearer authentication using a JWT. Obtain token from Google OAuth flow.",
    scheme_name="Bearer Auth" # This is the name that will appear in the docs UI
)

# Configure logging
# By default, Python's logging module sends messages to stderr.
# Azure App Services capture stdout and stderr, making them visible in the Log Stream.
logging.basicConfig(
    level=logging.INFO, # Set the desired logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get a logger instance for your application
logger = logging.getLogger(__name__)

# Startup function
# Init db connection and create db object
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.error("Application starting")
    yield
    logger.error("Application shutting down, cleaning up")

descript = """
*XIVMit API*
"""

app = FastAPI(
    lifespan=lifespan,
    description=descript
)

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

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

app.include_router(auth_router)


# Test function for the API
@app.get("/api")
def read_root():
    return {"Hello": "World"}


# returns a list of encounters and their properties
# sorted newest to oldest
# could be worth getting xivapi to do this so it auto updates
# Might not be worth using db for this at all since it update so infrequently and its small
@app.get("/api/getEncounters", response_model=model.CategorizedEncounterResponse)
async def get_fights_by_category(db: db_dependency):
    all_encounters = db.query(dbModels.DBEncounter).all()

    categorized_data: Dict[str, List[model.EncounterDetail]] = {}

    for encounter in all_encounters:
        # Use the 'tier' column for categorization
        category = encounter.tier
        if category not in categorized_data:
            categorized_data[category] = []

        Encounter_detail = model.EncounterDetail(
            shorthand=encounter.shorthand,
            boss=encounter.boss,
            imgLink=encounter.imgLink
        )
        categorized_data[category].append(Encounter_detail)

    return categorized_data
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


# Unimplemented test function
# Returns templates for specific encounter
# Calls db.getTemplates() 
@app.get("/api/getTemplates/{fight}")
def getTemplates(fight: p.encounterNames):
    #app.db.getTemplates(fight)
    return {
        0 : {
            "name" : "johns cool template",
            "fight" : "M5S",
            "user" : "john smith",
            "description" : "test templates",
            "bookmarks" : 10,
            "views" : 20,
            "id" : "asdf"
        }, 
        1 : {
            "name" : "johns cool template",
            "fight" : "M5S",
            "user" : "john smith 1",
            "description" : "test templates",
            "bookmarks" : 10,
            "views" : 20,
            "id" : "asdf"
        }, 
        2 : {
            "name" : "johns cool template",
            "fight" : "M5S",
            "user" : "john smith 2",
            "description" : "test templates",
            "bookmarks" : 10,
            "views" : 20,
            "id" : "asdf"
        }, 
        3 : {
            "name" : "johns cool template",
            "fight" : "M5S",
            "user" : "john smith 3",
            "description" : "test templates",
            "bookmarks" : 10,
            "views" : 20,
            "id" : "asdf"
        }, 
        4 : {
            "name" : "johns cool template",
            "fight" : "M5S",
            "user" : "john smith 4",
            "description" : "test templates",
            "bookmarks" : 10,
            "views" : 20,
            "id" : "asdf"
        }, 
        5 : {
            "name" : "johns cool template",
            "fight" : "M5S",
            "user" : "john smith 5",
            "description" : "test templates",
            "bookmarks" : 10,
            "views" : 20,
            "id" : "asdf"
        }
    }
