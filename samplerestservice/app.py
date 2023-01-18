import os
import requests
import json
import time
import random

from flask import Flask, request

# Initialize automatic instrumentation with Flask
app = Flask(__name__)

coupons = [
	{'ID': "1", 'Name': "NEW200", 'Type': "Flat", 'Value': 200, 'Status': True},
	{'ID': "2", 'Name': "MISSEDYOU15", 'Type': "Percent", 'Value': 15, 'Status': True},
	{'ID': "3", 'Name': "NEW100", 'Type': "Flat", 'Value': 100, 'Status': True},
	{'ID': "4", 'Name': "NEW50", 'Type': "Flat", 'Value': 50, 'Status': False},
	{'ID': "5", 'Name': "ICICI20", 'Type': "Percent", 'Value': 20, 'Status': False},
]

drivers = [
	{'driver_id': "5138", 'distance': 3.5},
	{'driver_id': "2501", 'distance': 1.8},
	{'driver_id': "61097", 'distance': 0.4},
	{'driver_id': "2052", 'distance': 1.3},
	{'driver_id': "6553", 'distance': 0.9},
	{'driver_id': "3002", 'distance': 4.3},
	{'driver_id': "65672", 'distance': 5.2},
]

def get_drivers(city):
	k = random.choice(range(0, len(drivers)))
	return random.choices(drivers, k=k)


@app.route('/coupons', methods=['GET'])
def GetAllCoupons():
   return {'coupons': coupons}


@app.route('/coupons/<c_type>', methods=['GET'])
def GetCouponsByType(c_type):
	coups = []
	for coup in coupons:
		if c_type == coup['Type']:
			coups.append(coup)
	return {'coupons': coups}


@app.route('/drivers', methods=['POST'])
def GetDrivers():
	if request.method == "POST":
		search_data = request.form

		# print(search_data)

		city = request.form.get('city')
		pickup_location = request.form.get('pickup_location')
		distance = request.form.get('distance')

		return {"drivers": get_drivers(city)}


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8081, debug=True)
