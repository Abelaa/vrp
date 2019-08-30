## Solution to Vehicle Routing Problem using google maps api

This is an API written in python 

Made for Centos Linux OS but works great on ubuntu and other linux distributions aswell, just skip step 1 and other centos specific commands if you are on a different environment

1. Install python3 on centos linux

	yum install centos-release-scl
	yum install rh-python36

1. requirements.txt contains the python dependencies required for this project. They can be installed using the command 

	```bash
	sudo pip install -r requirements.txt
	```

1. Install uwsgi, server software for production, 

	```bash
	pip install uwsgi
	```

configuration.sh script contains server configurations, mainly port and Google maps API KEY

* first enable python3 on centos linux
	
	```bash
	scl enable rh-python36 bash
	```

* Then the following commands will be available for use

	Run `start_server.bash` script to start the server
	Run `stop_server.bash` script to stop the server

