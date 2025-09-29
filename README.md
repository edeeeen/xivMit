WIP available at [sleepycat.me](https://sleepycat.me)

# Build instructions

## Backend:

Create a venv and run:
```pip install -r requirements.txt```

make a text file called `.env` and paste this and fill it out
```USERNAME="<SQL USERNAME>"
PASSWORD="<SQL PASSWORD>"
SERVER="<SQL SERVER URL>"
DATABASE="<SQL DB NAME>"
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
SECRET_KEY=""
SESSION_SECRET_KEY=""
GOOGLE_REDIRECT_URI=""
```

While in the venv run
`fastapi run`

The backend will be available on port 8000 by default

## Frontend

run 
`npx vite`

The frontend will be available on port 5173

