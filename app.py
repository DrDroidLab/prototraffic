import os
import requests
import json
import time

from flask import Flask, request, redirect, url_for, render_template, session

from pydoctordroid import codemarkers
dr = codemarkers.DroidEvents()

# Initialize automatic instrumentation with Flask
app = Flask(__name__)

city_dist_dict = {"BLR": 1.5, "HYD": 2.9, "NCR": 5.0}

def getDrivers(city, pickup_location):
	url = 'http://127.0.0.1:8081/drivers'
	data = {"city": city, "pickup_location": pickup_location, "distance": 3.0}

	response = requests.post(url, data=json.dumps(data))
	return response.json()['drivers']


def allocateDriverToOrderNow(city, drivers):

	allowed_distance = city_dist_dict.get(city, 3.0)
	
	if len(drivers) > 0:
		close_riders = list(filter(lambda x: x['distance'] < allowed_distance, drivers))
		if len(close_riders) > 0:
			return close_riders[0]['driver_id']

	return None


def getETAByDriverId(driver_id, drivers):
	for d in drivers:
		if d['driver_id'] == driver_id:
			return d['distance']*10
	return None


@app.route('/orders', methods=['POST'])
def PlaceOrder():

	if request.method == 'POST':

		city = request.form.get('city')
		merchant_id = request.form.get('merchant_id')
		order_value = request.form.get('order_value')

		pickup_location = request.form.get('pickup_location')
		drop_location = request.form.get('drop_location')

		order_id = request.form.get('order_id')

		dr.publish("OrderAllocation", "Initiated", (('order_id', order_id), ('city', city), ('merchant_id', merchant_id), ('order_value', order_value), ('pickup_location', pickup_location), ('drop_location', drop_location)))

		drivers = getDrivers(city, pickup_location)

		dr.publish("OrderAllocation", "DriverFetched", (('order_id', order_id), ('city', city), ('drivers_count', len(drivers))))

		driver_id = allocateDriverToOrderNow(city, drivers)
		if driver_id:
			eta = getETAByDriverId(driver_id, drivers)
			dr.publish("OrderAllocation", "AllocationSucceeded", (('order_id', order_id), ('city', city), ('driver_id', driver_id), ('eta', eta)))
			return {"order_allocated": True, 'eta_for_delivery': eta}	

		dr.publish("OrderAllocation", "AllocationFailed", (('order_id', order_id), ('city', city), ('driver_id', driver_id)))
		return {"order_allocated": False, 'eta_for_delivery': None}	
		

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8082, debug=True)
