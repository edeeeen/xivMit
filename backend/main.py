#################################################################
#                         FastAPI functions                     #
#################################################################

from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
import json
import db
import parameters as p

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

# Test function for the API
@app.get("/api")
def read_root():
    return {"Hello": "World"}

# returns a list of encounters and their properties
# sorted newest to oldest
# could be worth getting xivapi to do this so it auto updates
# in the future will be saved in db
@app.get("/api/getEncounters")
def getEncounters():
    return {
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
    }

# Unimplemented
# Returns templates for specific encounter
# Calls db.getTemplates() 
@app.get("/api/getTemplates/{fight}")
def getTemplates(fight: p.encounterNames):
    db.getTemplates(fight)
    return {"test" : fight}


# If its the main function then start the server on port 8000 using uvicorn
#if __name__ == '__main__':
#    uvicorn.run(app, host='0.0.0.0', port=8000)
