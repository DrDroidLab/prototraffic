#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import uuid
from locust import HttpUser, TaskSet, between

cities = ['BLR', 'HYD', 'NCR']

pickups = {"NCR": ["Kamla Nagar", "Lajpat Nagar"], "BLR": ["Indira Nagar", "Hebbal"], "HYD": ["Begumpet", "Jubilee Hill"]}

drops = {"NCR": ["Chandnig Chowk", "Kalkaji"], "BLR": ["HSR Layout", "Frazer Town"], "HYD": ["Gachibowli", "Kukatpally"]}

merchant_ids = {"NCR": [94, 1943, 74], "BLR": [1912, 94], "HYD": [94, 1943, 38]}

def orders(l):
	city = random.choice(cities)
	merchant_id = random.choice(merchant_ids[city])
	pickup = random.choice(pickups[city])
	drop = random.choice(drops[city])
	order_value = random.randint(180, 700)
	order_id = uuid.uuid4().hex
	l.client.post("/orders", {"order_id": order_id, "city": city, "pickup_location": pickup, "drop_location": drop, "merchant_id": merchant_id, "order_value": order_value})

class UserBehavior(TaskSet):

	def on_start(self):
		orders(self)

	tasks = {orders: 5}

class WebsiteUser(HttpUser):
	tasks = [UserBehavior]
	wait_time = between(1, 10)
