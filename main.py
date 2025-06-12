from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
#import api



app = FastAPI()

@app.get("/api")
def read_root():
    return {"Hello": "Hello World"}

# first 'static' specify route path, second 'static' specify html files directory.
app.mount('/', StaticFiles(directory='static',html=True))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
