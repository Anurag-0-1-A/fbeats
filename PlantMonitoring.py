from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from datetime import datetime, date
import os, asyncio, json, time
from dotenv import load_dotenv

#temp and humidity
import seeed_dht

#moisture
import math
import sys
import time
from grove.adc import ADC

__all__ = ["GroveMoistureSensor"]

class GroveMoistureSensor:
  '''
  Grove Moisture Sensor class
  Args:
    pin(int): number of analog pin/channel the sensor connected.
  '''
  def __init__(self, channel):
      self.channel = channel
      self.adc = ADC()

  @property
  def moisture(self):
    '''
    Get the moisture strength value/voltage
    Returns:
    (int): voltage, in mV
    '''
    value = self.adc.read_voltage(self.channel)
    return value

#sunlight
import seeed_si114x
import time
import signal

# Configuration parameters
bme_pin = 1
bme_address = 0x76
moisture_pin = 0
light_pin = 0

# Create the sensors
sensor = seeed_dht.DHT("11", 16)
moisture_sensor = GroveMoistureSensor(moisture_pin)

#light_sensor = GroveLightSensor(light_pin)

load_dotenv()
id_scope = os.getenv('0ne0036E38B')
device_id = os.getenv('Raspberry_pi')
primary_key = os.getenv('gymeiFeFoNwg2BV28flilg8slBwW6jbOq6oo96I2LJQ=')

def getTemperaturePressureHumidity():
    # for DHT11/DHT22

    humi, temp = sensor.read()
    if not humi is None:
      print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
    else:
      print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))
    time.sleep(2)
    #return bme280.sample(bus, bme_address, calibration_params)
    return(humi, temp)

def getMoisture():

    Grove = GroveMoistureSensor
     
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = 0

    sensor = GroveMoistureSensor(pin)

    print('Detecting moisture...')

    m = sensor.moisture
    if 0 <= m and m < 2000:
      result = 'Dry'
    elif 2000 <= m and m < 3000:
      result = 'Moist'
    else:
      result = 'Wet'
    print('Moisture value: {0}, {1}'.format(m, result))
    time.sleep(1)
    #return round(moisture_sensor.moisture, 2)
    return round(m, 2)

def getLight():
    SI1145 = seeed_si114x.grove_si114x()
    print("Please use Ctrl C to quit")
    light_data=SI1145.ReadVisible
    return (light_data)

def getTelemetryData():
    temp = getTemperaturePressureHumidity() # degrees Celsius
    moisture = getMoisture() # voltage in mV
    #pressure = round(getTemperaturePressureHumidity().pressure, 2)/1000 # kPa
    #humidity = round(getTemperaturePressureHumidity().humidity, 2) # % relative Humidity
    light = getLight() # % Light Strength
    data = {
        "temperature": temp[1],
        "humidity":temp[0],
        "soil_moisture": moisture,
        "sunlight": light
    }

    return json.dumps(data)

async def main():
    # provision the device
    async def register_device():
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host='global.azure-devices-provisioning.net',
            registration_id='Raspberry_pi',
            id_scope='#########',
            symmetric_key='###gymeiFeFoNwg2BV28flilg8slBwW6jbOq6oo96I2LJQ=###')

        return await provisioning_device_client.register()
    results = await asyncio.gather(register_device())
    registration_result = results[0]

    # build the connection string
    conn_str='HostName=' + registration_result.registration_state.assigned_hub + \
                ';DeviceId=' + 'Raspberry_pi' + \
                ';SharedAccessKey=' + 'gymeiFeFoNwg2BV28flilg8slBwW6jbOq6oo96I2LJQ='

    # The client object is used to interact with Azure IoT Central.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    print('Connecting')
    await device_client.connect()
    print('Connected')

    # async loop that sends the telemetry
    async def main_loop():
        while True:
            telemetry = getTelemetryData()
            print(telemetry)

            await device_client.send_message(telemetry)
            await asyncio.sleep(5)

    await main_loop()

    # Finally, disconnect
    await device_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
