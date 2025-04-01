
# import modules
from machine import Pin, I2C
from lsm6dsox import LSM6DSOX
import network
from time import sleep, sleep_ms
import requests
import json

# setup hardware led and sensor
led = machine.Pin("LED", machine.Pin.OUT)
sensor = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))

# load config file
with open("config.txt", "r") as file:
    ssid = file.readline().strip()
    password = file.readline().strip()
    server = file.readline().strip()
    
# connect to the wifi network
def connect():

    # Init Wi-Fi Interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Connect to your network
    wlan.connect(ssid, password)

    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status():
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep_ms(500)
        led.high()
        sleep_ms(500)
        led.low()
        
    # Check if connection is successful
    if not wlan.status():
        led.low()
        raise RuntimeError('Failed to establish a network connection')
    else:
        led.high()
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
    
# send a json message to the server
def send_message(content):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"payload": content})
    
    response = requests.post(server, data=data, headers=headers)

    response_code = response.status_code
    
    return response_code == 200

# send the sensor data to the server
def send_sensors():
    accelerometer = sensor.accel()
    gyroscope = sensor.gyro()
    
    send_message({"accelerometer": accelerometer, "gyroscope": gyroscope})

# connect to the wifi network
connect()

# send the data forever!
while True:
    send_sensors()
