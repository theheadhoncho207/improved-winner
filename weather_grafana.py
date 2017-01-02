#! /usr/bin/python

# To install and run the script as a service under SystemD. See: https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux

import requests
import time
from influxdb import InfluxDBClient

HOSTNAME = "jarvis" #Pi-hole hostname to report in InfluxDB for each measurement
INFLUXDB_SERVER = "dashboard" #IP or hostname to InfluxDB server
INFLUXDB_PORT = 8086 #Port on InfluxDB server
DELAY = 70 # seconds

def send_msg(visibility, windSpeed, temperature, precipProbability, nearestStormDistance):

	json_body = [
	    {
	        "measurement": "weatherstats",
	        "tags": {
	            "host": HOSTNAME
	        },
	        "fields": {
	            "nearestStormDistance": int(nearestStormDistance),
                    "precipProbability": int(precipProbability),
                    "temperature": float(temperature),
                    "windSpeed": float(windSpeed),
		    "visibility": float(visibility)
	        }
	    }
	]

	client = InfluxDBClient('10.10.20.234', 8086, 'admin', 'admin', 'weather') #InfluxDB host, InfluxDB port, Username, Password, database
	#client.create_database('telegraf') #Uncomment to create the database (expected to exist prior to feeding it data)
	client.write_points(json_body)

if __name__ == '__main__':
        while True:
          api = requests.get('https://api.darksky.net/forecast/<API_KEY>/37.8267,-122.4233') #URI to pihole server api
	  API_out = api.json()
	  API_out = API_out['currently']
          nearestStormDistance = (API_out['nearestStormDistance'])
          precipProbability = (API_out['precipProbability'])
          temperature = (API_out['temperature'])
          windSpeed = (API_out['windSpeed'])
	  visibility = (API_out['visibility'])
	

          send_msg(visibility, windSpeed, temperature, precipProbability, nearestStormDistance)
          time.sleep(DELAY)
