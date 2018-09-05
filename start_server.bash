#start server in the background
#load configuration file
source ./configuration.sh
#enable python3 on centos linux
#scl enable rh-python36 bash
#run production server
uwsgi --http-socket 0.0.0.0:$FLASK_PORT --wsgi-file wsgi.py --master --processes $NUM_PROCESSES --threads $NUM_THREADS --safe-pidfile pid_list.txt &
#uwsgi --socket 0.0.0.0:6000 --protocol=http -w wsgi &
