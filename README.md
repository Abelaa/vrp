## Solution to Vehicle Routing Problem using google maps api

This is an API written in python. It takes one origin and mulitiple destinations as an input and returns distance matrix in km as an output. It uses google maps api to so, it just automates the whole thing for you. You just have deploy it online with google api key.


sample input to the API
```JSON
input = 
{
	"origin" : "8.526469,39.261001",
	"locations": 
	[
		"11.571596,37.361537",
		"8.900745,38.740365",
		"7.056614,38.458647"
	],
	"maximum_distance": 2190000,
	"number_of_vehicles": 2
}
```

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

