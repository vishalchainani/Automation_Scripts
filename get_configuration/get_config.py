from jnpr.junos import Device
from lxml import etree
import yaml
from jnpr.junos.exception import *


with open('devices.yaml' , 'r') as device_file:
	device_list=yaml.load(device_file)

user_name=device_list["username"]
passwd=device_list["password"]

for node in str(device_list["devices"][0]).split(" "):
	dev=Device(host=node, user=user_name, password=passwd)
	print ("Connecting to the device " + node)
	try:
		dev.open()
	except ConnectTimeoutError:
			print "Unable to connect to the device " + node
			continue
	except ConnectAuthError:
			print "Username or password is incorrect for " + node
			continue
	except ConnectRefusedError:
			print "Either " + node + " name is incorrect or " + node + " doesn't have NETCONF configured"
			continue
	except ConnectUnknownHostError:
			print "Cannot resolve device name " +node
			continue
	host_name=dev.facts["hostname"]
	with open(host_name+'.txt', 'w') as config_file:
		print ("Fetching the configuration from " + host_name)
		config_file.write(etree.tostring(dev.rpc.get_configuration({'format':'text'})))
	dev.close()
