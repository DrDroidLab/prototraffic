# prototraffic
This repository contains with the following:
- A basic Flask application with instrumentation setup for generating events using pydoctordroid
- A traffic simulator for the above Flask application
- A sample flask rest service that is being called from the first application


## Install dependencies
Run the following command to setup python packages for both flask application and traffic simulator
```
pip3 install -r requirements.txt
```

## Setup DrDroid Auth token
Add the auth token as an environment variable to allow the DrDroid SDK to publish events to the platform backend. You can request for beta access to DrDroid platform [here](https://drdroid.io).
```
export DRDROID_AUTH_TOKEN=<TOKEN>
```

## Generating custom events for Doctor Droid 
```
// Put it on top of the app.py file
from pydoctordroid import DrDroid
dr = DrDroid()

// Add events like this
dr.publish("Order", "Created", {"ID": "13432", "City": "BLR", "IS_COD": False})
```

You'll need to setup a few environment variables for the SDK configuration. Here is complete documentation about the SDK [pydoctordroid](https://github.com/DrDroidLab/drdroid-py) and how to configure it.

## Run the Flask application
Running the following command starts the Flask application on port 8082. It is not dockerized. 
```
python3 app.py
```

## Run the Secondary sample Flask Rest Service application
Running the following command starts the Flask application on port 8082. It is not dockerized. 
```
python3 samplerestservice/app.py
```

## Run the traffic simulation
Run the following command to start the simulated traffic. You can change the number of concurrent users to increase or decrease the traffic.
```
locust --host="http://localhost:8082" --headless -f traffic/locustfile.py -u 1
```

this is an example change using doctor droid playbooks