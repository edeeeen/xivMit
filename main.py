from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
import json 
#import api



app = FastAPI()

@app.get("/api")
def read_root():
    return {"Hello": "World"}

@app.get("/encounters")
def getEncounters():
    return {
        "Cruiserweight":[
            {
                "shorthand" : "M5S",
                "boss" : "Dancing Green",
                "imgLink" : "content/m5s.png"
            },
            {
                "shorthand" : "M6S",
                "boss" : "Sugar Riot",
                "imgLink" : "content/m6s.png"
            },
            {
                "shorthand" : "M7S",
                "boss" : "Brute Abominator",
                "imgLink" : "content/m7s.png"
            },
            {
                "shorthand" : "M8S",
                "boss" : "Howling Blade",
                "imgLink" : "content/m8s.png"
            }
        ],
        "Light-Heavyweight":[  
            {
                "shorthand" : "M1S",
                "boss" : "Black Cat",
                "imgLink" : ""
            }, 
            {
                "shorthand" : "M2S",
                "boss" : "Honey Bee Lovely",
                "imgLink" : ""
            },
            {
                "shorthand" : "M3S",
                "boss" : "Brute Bomber",
                "imgLink" : ""
            },
            {
                "shorthand" : "M4S",
                "boss" : "Wicked Thunder",
                "imgLink" : ""
            }
        ]
    }



# first 'static' specify route path, second 'static' specify html files directory.
app.mount('/', StaticFiles(directory='static',html=True))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
