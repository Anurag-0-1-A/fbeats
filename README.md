# Azure Farmbeats: Plant Monitoring System

## About Farmbeats 
Several studies have demonstrated the need to significantly increase the world’s food production by 2050. However, there is a limited amount of additional arable land, and water levels have also been receding. Although technology could help the farmer, its adoption is limited because the farms usually do not have power or Internet connectivity, and the farmers are typically not technology savvy. I am working towards an end-to-end approach, from sensors to the cloud, to solve the problem. 

## Components Required
-	Raspberry Pi 4 
-	Grove Base Hat for Raspberry Pi
-	Screwdriver, screws, and standoffs for Base Hat
-	Grove Connectors
-	SD Card USB Adapter
-	SD Card 32GB
-	Grove Temperature and 
-	Humidity Sensor Sunlight sensor
-	Capacitive Soil Moisture Sensor

## STEP 1: INSTALL RASPBERRY PI OS (RASPBIAN) ON YOUR SD CARD
### Preparation
-	This step can be completed using Windows, macOS, or Ubuntu
-	Have a Micro SD Card with an adapter to be able to use it on your PC

### Download the Raspberry Pi Imager
-	You will need to install the latest version of Raspbian Lite on a micro-SD card. An easy way to do this is to install the Raspberry Pi Imager
-	Go to the Official Raspberry Pi Downloads Page.
-	Select the correct version of the Raspberry Pi Imager for your OS.
-	Install the Raspberry Pi Imager application and open it.
-	Installing Raspberry Pi OS
-	Insert the microSD card into your computer or laptop. You may need to use the SD card adapter and plug it into a USB port on your PC.
-	Select CHOOSE OS to see a list of the available operating systems
-	Select Raspberry Pi OS (32-bit)
-	Next, select CHOOSE SD CARD and find the SD card that you would like to install the OS on
-	Before hitting WRITE, press “Ctrl-Shift-X” to open a configuration menu like this.
-	Will display a window in which we will select the “Enable SSH” box, it will also request that we enter a password for the pi user, which is the user that comes by default in Raspberry pi, usually, the password is Raspberry for this user, but with this option, you can enter the one you like.
-	Going down further in this window we can find the “configure wifi” box where we enter the network name and password
-	Select WRITE and wait for the process to complete before removing your SD card.

### Assemble your DIY Sensor Device Hardware
Add the Grove Base Hat to your Raspberry Pi. Match the end pins up and press down firmly. Look at it from all angles to ensure that it is correctly connected.

### Insert the Micro SD Card
On the bottom of the Raspberry Pi, there is a micro–SD card slot. Place your micro-SD card into this slot so that the printed side is visible. Push the card into the slot firmly. The SD card included in your kit will already be ready to use.  If there are any issues with the SD card see Appendix: Flashing the SD Card. Always remember to unplug the Raspberry Pi when inserting or removing the SD card.

-	Plug the Capacitive Soil Moisture Sensor into socket A2. If you have a second one plug it into A4.
-	Plug the Light Sensor into socket A0.
-	Plug the Temperature & Humidity into the bottom left I2C socket.
-	Once all your sensors are plugged in you should have something that looks like this.

### Power on your device
-	Plug the large end of the micro-USB cable into the power adapter and insert the power adapter into a power source
-	Plug the small end of the micro-USB cable into the Raspberry Pi and Power Up! A red light should shine on the motherboard.

### Configuring the Network Settings
#### Setting up your Pi
When powered on for the first time you need to do a few steps on the device. You will need to change your login password, set up or test your connection to the internet, and enable the I2C interface (required for using the grove sensors). Try SSHing into your Pi. From your computer connect to pi@raspberrypi.local.
```
ssh pi@raspberrypi.local
```
If the host cannot be found then if you know the IP address (for example by using your router's management software) then you can log in to pi@192.168.0.1, replacing 192.168.0.1 with the IP address of your Pi. This can be found by typing the following command into the terminal on your pi:
```
hostname -I
```
### Turn on the I2C interface
For the grove sensor to work, the I2C interface needs to be enabled.
1.	Launch the configuration tool on the Pi, found under Menu > Preferences > Raspberry Pi Configuration
2.	Select the “Interfaces” tab
3.	Set I2C to “Enabled”
4.	Select OK to confirm the changes
5.	Select Yes to reboot the system if prompted.

The SSH connection will be terminated, so you will need to reconnect. Once the Pi reboots the I2C interface will be enabled.

## STEP 2: AZURE SERVICES INTEGRATION
### Create App using IoT Central
Azure IoT Central is an IoT application platform that allows us to interact with cloud services and interact with them.
IoT central has a user-friendly UI that allows us to monitor device conditions, create rules, and manage millions of devices easily.
### Create IoT Central Application from Portal
1.	Log in to your Azure Portal.
2.	Click on + Create a new resource.
3.	Search IoT Central and click on IoT Central Application. Then click on Create. 
4.	Fill in the details for the IoT App.
  - 1. Give your app a name such as lab1sensor.
  - 2. Select your subscription.
  - 3. Create a new resource group for the whole lab. In this case, I have named it Lab1.

  Resource groups are logical groupings of Azure services, allowing you to manage all the services for a particular application or project together. At the end of this workshop, this Resource Group will be deleted, deleting all the services created.
  - 4. Select Standard 1 for the Pricing plan.
  - 5. In this case we are going to create the app from scratch, so we chose a custom application in Template.
  - 6. Select your location.
  - 7. Click on Create.
5.	After that, your IoT Central app will start the deployment. Once it is finished, just click on Go to Resource.
6.	To access the IoT Application Dashboard just press on the IoT Central Application URL hyperlink.

### Create a Device Template
Azure IoT Central can work with multiple types of devices, and multiple devices per device type. Device types are defined using templates - these specify the capabilities of the device including the telemetry that can be received from the device and commands that can be sent to it.
The environment sensor captures temperature, humidity, air pressure, soil moisture, and light conditions. You will need to define a template that has these values on it, so they can be received from the Pi.
1.	From the left panel select Device Template. Then click on + New.
2.	Select the IoT Device template.
3.	Select the Next: Customize button.
4.	Select the Next: Review button.
5.	Select the Create button.
6.	Name the template SensorMonitor.

Once the template is created, you need to add capabilities to it. These are defined using capability models, which define the capabilities of all devices that will use this template. Capability models are made up of three parts:
-	Interfaces - these are reusable collections of capabilities and are grouped into three categories:
  - 1.	Telemetry - actual values detected and sent by the device, for example in a thermostat it could be the current detected temperature
  - 2.	Properties - settings on the device, for example in a thermostat it could be the desired temperature. These can be set by the device, or via Azure IoT Central and synced to the device.
  - 3.	Commands - calls that can be made on the device, optionally passing data. For example, in a thermostat, it could be called by a mobile app to send a request to change the desired temperature.
-	Cloud properties - these are properties set in Azure IoT Central against a device, but not synced to the device. For example, a device could have a cloud property for the account name of the owner, the devices’ location, or the date it was last serviced.
-	Views - these are dashboards for a device that can contain charts, data values, and other information allowing you to visualize telemetry or send commands.
The environment sensor needs a capability model created, with an interface defined for the telemetry values being sent, a command to indicate that the plant needs watering, and a view to visualize these values.
1.	Select the Custom capability model
Add an interface
2.	Add a new interface to the capability model by selecting the top-level Environment sensor item in the menu and selecting +Add interface
3.	Select Custom
4.	This interface needs 5 telemetry values added to it for the temperature, humidity, soil moisture, and light level. Telemetry values have the following properties:
-	Display name - this defines what is shown on a view to display the value
-	Name - this map to the values being sent from the device
-	Capability type - this defines what type of value this is, and includes some standard types such as temperature or pressure.
-	Schema - this defines the data type for the value being received, such as an integer or a floating-point number
-	Unit - this defines the unit, for now, telemetry types, for example, °C for temperatures.
-	Select the + Add capability button to add new capabilities, and add the following five values:

Display Name	Name	Capability Type	Semantic Type	Schema	Unit
Temperature	temperature	Telemetry	Temperature	Double	°C
Humidity (%)	humidity	Telemetry	Humidity	Double	%
Soil Moisture (%)	soil_moisture	Telemetry	None	Double	%
Light Level (%)	light_level	Telemetry	None	Double	%

|     Display Name         |     Name             |     Capability Type    |     Semantic Type    |     Schema    |     Unit    |
|--------------------------|----------------------|------------------------|----------------------|---------------|-------------|
|     Temperature          |     temperature      |     Telemetry          |     Temperature      |     Double    |     °C      |
|     Humidity (%)         |     humidity         |     Telemetry          |     Humidity         |     Double    |     %       |
|     Soil Moisture (%)    |     soil_moisture    |     Telemetry          |     None             |     Double    |     %       |
|     Light Level (%)      |     light_level      |     Telemetry          |     None             |     Double    |     %       |

### Add a view
1.	Select Views from the menu.
2.	Select Visualizing the device
3.	Set the view name to Overview. We will use this view to show the charts of the values recorded.
4.	Drag Temperature from the Telemetry section onto the dashboard. This will add a graph showing the temperature recorded over the past 30 minutes to the dashboard. You can configure this in multiple ways using the control buttons on the top of the panel:
- Change the visualization to be several different chart types or the last known value
- Change the size of the panel on the dashboard
- Configure the chart including legend, axis labels, and the time range
- Configure the chart or last know value to your liking.
5.	Repeat this for the other telemetry values. If you want to plot multiple telemetry values on the same chart use the checkboxes to select multiple values and drag them together. You can add telemetry values multiple times to get multiple views over the data.
6.	You can also customize the view with labels, markdowns, or images if desired.
7.	Select the Save button from the top menu
8.	You can create another view showing just the last value received if you want.
Here is an example of how it can look like.

### Publish the device template
Before the device template can be assigned to a device, it needs to be published. Once published, any interfaces defined on it cannot be changed, instead, a new version of the device template needs to be created.
1.	Select the Publish button from the top-most menu.
2.  Click on Publish.

### Create a device
1.	Go to Devices > SensorMonitor.
2.	Select + New.
3.	Set the Device Name to Raspberry pi and the Device Id to raspberry_pi. Then click on Create.

A new device should appear in the devices list.

### Get the device connection details
Each device has a set of connection details that will be used on the actual device to connect to Azure IoT Central and send telemetry.
1.	Click on the Raspberry pi device you have just created.
2.	Click on the Connect button located at the top right corner.
3.	Take note of the ID Scope, Device Id, and Primary key. You will need these values to send the data from the raspberry pi.

## STEP3: INSTALLING PYTHON 3
By default, Raspbian (Stretch version April 2018 and earlier) uses Python 2. However, versions 2 and 3 come installed by default. We just have to make 1 minor change so that the Pi uses Python 3 whenever we type python into a terminal. In a terminal window, enter the following command:
```
python --version
``` 
Raspbian Lite, the Python package manager, pip, does not come pre-installed. As a result, you will need to install it with the commands:
```
sudo apt-get update
sudo apt-get install python3-pip
```
Press y when prompted.
Note that to use pip for Python 3, you will need to use the command pip3.

### Configure a virtual environment
Python comes in various versions, and Python apps can use external code in packages installed via a tool called pip. This can lead to problems if different apps need different package versions or different Python versions. To make it easier to avoid issues with package or Python versions, it is best practice to use virtual environments, self-contained folder trees that contain a Python installation for a particular version of Python, plus several additional packages. Ensure that the Python 3 virtual environment tooling is installed by running the following commands in the terminal
```
sudo apt-get update
```
```
sudo apt-get install python3-venv
```
Create a new file inside the EnvironmentMonitor folder called app.py

1.	Name the new file app.py and press return
2.	Create a new virtual environment called .venv using Python 3 by running the following command in the terminal
python3 -m venv .venv
3.	A dialog will pop up asking if you want to activate this virtual environment. Select Yes.

### Install the required python packages
Python has a package manager called pip that allows you to install code from other developers in packages called pip packages. You can read more about pip and see the available packages at pypi.org. Packages can either be installed into the virtual environment one at a time using the pip command, or multiple packages can be listed in a file called requirements.txt and installed together. The advantage of using a requirements.txt file is that this can be checked into source code control so that other developers can configure their environment the same way by installing the same packages from this file.
1.	Create a new file inside the EnvironmentMonitorIoT folder called requirements.txt
2.	Add the following to this file
```
azure-iot-device
python-dotenv
RPi.bme280
grove.py
smbus2
```
From the terminal, run the following command to install these packages:
```
pip3 install -r requirements.txt
```
The packages installed are:
|      Package            |      Description                                                                                                  |     Capability Type    |     Semantic Type    |     Schema    |     Unit    |
|-------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------|----------------------|---------------|-------------|
|     azure-iot-device    |     Allows communication with Azure IoT services including   Visual Studio Code                                   |     Telemetry          |     Temperature      |     Double    |     °C      |
|     python-dotenv       |     Allows loading of environment variables   from .env files                                                     |     Telemetry          |     Humidity         |     Double    |     %       |
|     RPi.bme280          |     Provides access to the BME280 temperature/pressure/humidity   sensor                                          |     Telemetry          |     None             |     Double    |     %       |
|     grove.py            |     Provides access to the grove sensors including the Grove   capacitive moisture sensor and the Light sensor    |     Telemetry          |     None             |     Double    |     %       |






