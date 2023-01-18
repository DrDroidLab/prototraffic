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

## Generating custom events for Doctor Droid 
```
// Put it on top of the app.py file
from pydoctordroid import codemarkers
dr = codemarkers.DroidEvents()

// Add events like this
dr.publish("Order", "Created", (("ID", "13432"), ("City", "BLR"), ("IS_COD", False)))
```
You'll be required to Read documentation here for the [pydoctordroid](https://github.com/DrDroidLab/drdroid-py)

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