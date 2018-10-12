Solution to Vehicle Routing Problem using google maps api
Made for Centos Linux OS but works great on ubuntu aswell,
just skip step 1  and other centos specific commands

1. Install python3 on centos linux

	yum install centos-release-scl
	yum install rh-python36

2. requirements.txt contains the python dependencies required for this project. They can be installed using the command 

	sudo pip install -r requirements.txt

2. Install uwsgi, server software for production, 

	pip install uwsgi

configuration.sh script contains server configurations,
mainly port and Google maps API KEY

first enable python3 on centos linux

	scl enable rh-python36 bash

Then you can use the following commands

	start_server.bash script can be used to start the server
	stop_server.bash script can be used to stop the server

