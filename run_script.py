from modbus_server import Modbus_Server
import time
from struct import *

#from pymodbus.constants import Endian
#from pymodbus.payload import BinaryPayloadDecoder




obj = Modbus_Server("config.yaml")
print("check it")
obj.write_float(0,32.0)
#obj.initialize_modbus()
#signal_strength = obj.decode_register(0,'32float')
#print(signal_strength)
#print(type(signal_strength))

#output = obj.get_data()
#print(output)
