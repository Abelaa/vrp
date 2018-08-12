#load the virtual environment for this service
source ./venv/bin/activate
#load configuration file
source ./configuration.sh
#start server in the background
#flask run --host=0.0.0.0 --port=$FLASK_PORT (development server)
uwsgi --http :$FLASK_PORT --wsgi-file wsgi.py --master --processes 2 --threads 2 --safe-pidfile pid_list.txt
