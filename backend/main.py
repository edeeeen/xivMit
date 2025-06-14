from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
import json
import db



app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api")
def read_root():
    return {"Hello": "World1"}

# returns a list of encounters and their properties
# sorted newest to oldest
# could be worth getting xivapi to do this so it auto updates
@app.get("/api/getEncounters")
def getEncounters():
    return {
        "Cruiserweight":[
            {
                "shorthand" : "M5S",
                "boss" : "Dancing Green",
                "imgLink" : "src/content/m5s.png"
            },
            {
                "shorthand" : "M6S",
                "boss" : "Sugar Riot",
                "imgLink" : "src/content/m6s.png"
            },
            {
                "shorthand" : "M7S",
                "boss" : "Brute Abominator",
                "imgLink" : "src/content/m7s.png"
            },
            {
                "shorthand" : "M8S",
                "boss" : "Howling Blade",
                "imgLink" : "src/content/m8s.png"
            }
        ],
        "Light-Heavyweight":[  
            {
                "shorthand" : "M1S",
                "boss" : "Black Cat",
                "imgLink" : "src/content/m1s.png"
            }, 
            {
                "shorthand" : "M2S",
                "boss" : "Honey Bee Lovely",
                "imgLink" : "src/content/m2s.png"
            },
            {
                "shorthand" : "M3S",
                "boss" : "Brute Bomber",
                "imgLink" : "src/content/m3s.png"
            },
            {
                "shorthand" : "M4S",
                "boss" : "Wicked Thunder",
                "imgLink" : "src/content/m4s.png"
            }
        ]
    }

#input values for getTemplates()
class encounterNames(str, Enum):
    m1s = "M1S"
    m2s = "M2S"
    m3s = "M3S"
    m4s = "M4S"
    m5s = "M5S"
    m6s = "M6S"
    m7s = "M7S"
    m8s = "M8S"

# Returns templates for specific encounter
# Calls db.getTemplates() 
@app.get("/api/getTemplates/{fight}")
def getTemplates(fight: encounterNames):
    db.getTemplates(fight)
    return {"test" : fight}


# first 'static' specify route path, second 'static' specify html files directory.

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
