#load configuration file
source configuration.sh
#start server
flask run --host=0.0.0.0 --port=$FLASK_PORT
