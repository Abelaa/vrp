
1. Install python3 if on centos linux

	yum install centos-release-scl
	yum install rh-python36

2. requirements.txt contains the python dependencies required for this project. They can be installed using the command 

	sudo pip install -r requirements.txt

2. Install uwsgi, server software for production, 

	pip install uwsgi
	sudo apt install uwsgi # on ubuntu

configuration.sh script contains server configurations,
mainly port and Google maps API KEY

start_server.bash script can be used to start the server

stop_server.bash script can be used to stop the server

cd into the scripts folder before running them
