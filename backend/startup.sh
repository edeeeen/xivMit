apt-get update
apt-get install -y unixodbc-dev

curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update

ACCEPT_EULA=Y apt-get install -y msodbcsql17 # Or msodbcsql18 for ODBC Driver 18

pip install  -r  requirements.txt
fastapi run main.py