#load configuration file
source configuration.sh
# kill process on port $FLASK_PORT
# then hide error message if no process found on that port
sudo kill $(sudo lsof -t -i:$FLASK_PORT) > /dev/null 2>&1
echo done.