topic = "RemotePiControl" #topic name
port = YOUR_MQTT_PORT_NUMBER #port to be used by mqtt; IoT Team: use port 31883
broker = "YOUR BROKER IP/HOSTNAME" #broker DNS name or IP address; IoT Team: use localhost, supervisor IP address, or supervisor DNS name 
client = "YOUR CLIENT IP/HOSTNAME" #client DNS name or IP address; IoT Team: use IOBoard IP address or IOBoard DNS name
cacert = "/SOME/PATH/TO/YOUR_CAFILE.crt" #path to cafile, leave as is if not using keys
certfile = "/SOME/PATH/TO/YOUR_CERTFILE.crt" #path to certfile, leave as is if not using keys
keyfile = "/SOME/PATH/TO/YOUR_KEYFILE.key" #path to keyfile, leave as is if not using keys
timezone = 'US/Arizona' #timezone for timestamps, consult pytz list of timezones for acceptable timezones
