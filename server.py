from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import yaml
from struct import *
import random
from twisted.internet.task import LoopingCall

class Modbus_Device_Simulator():

    def __init__(self, config_file='config.yaml', config_section='server'):
        if (config_section==None):
            config_section = 'server'
        with open('config.yaml') as f:
            modbusConfig = yaml.safe_load(f)

        self.port = modbusConfig[config_section]['port']
        self.registers_float = modbusConfig[config_section]['float_registers']
        self.registers_int32 = modbusConfig[config_section]['int32_registers']
        self.context = None
        self.identity = None

    def create_slave_context(self):
        register_size = len(self.registers_float)*2 + len(self.registers_int32)*2
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [17]*100),
            co=ModbusSequentialDataBlock(0, [17]*100),
            hr=ModbusSequentialDataBlock(0, [0]*register_size),
            ir=ModbusSequentialDataBlock(0, [17]*100))
        if self.context == None:
            self.context = [ModbusServerContext(slaves=store, single=True)]
        else:
            self.context.append(ModbusServerContext(slaves=store, single=True))

    def create_slave_identity(self, vendor_name = 'pymodbus', product_code = 'pyMb', vendor_url = 'http://github.com/bashwork/pymodbus/', product_name = 'pymodbus device simulation',
        model_name = 'pymodbus_server', major_minor_revision = '1.0'):
        identity = ModbusDeviceIdentification()
        identity.VendorName = vendor_name
        identity.ProductCode = product_code
        identity.VendorUrl = vendor_url
        identity.ProductName = product_name
        identity.ModelName = model_name
        identity.MajorMinorRevision = major_minor_revision
        if self.identity == None:
            self.identity = [identity]
        else:
            self.identity.append(identity)

    def set_up_looping_calls(self, time = 5):
        loop = LoopingCall(f=self.update_with_random_values)
        loop.start(time, now=True)

    def create_server(self, context_id = 0):
        StartTcpServer(self.context[context_id], identity=self.identity[context_id], address=("0.0.0.0", 5020+context_id))

    def write_float(self, context_in, address, value, slave_id=0x0):

        context = context_in[0]
        register = 3 # for holding regsiter
        slave_id = slave_id

        i1, i2 = unpack('>HH',pack('f',value))
        values = [i1, i2]
        context[slave_id].setValues(register, address, values)

    def write_int32(self, context_in, address, value, slave_id=0x0):

        context = context_in[0]
        register = 3 # for holding regsiter
        slave_id = slave_id
        i1, i2 = unpack('>HH',pack('i',value))
        values = [i1, i2]
        context[slave_id].setValues(register, address, values)

    def update_with_random_values(self):
        for the_key, reg_address in self.registers_float.items():
            new_val = random.uniform(0.0,500.0)
            self.write_float(self.context, reg_address, new_val)
            # self.write_float(self.context, reg_address, 120)

        for the_key, reg_address in self.registers_int32.items():
            if the_key == "heartbeat": 
                possible_values = [0x55AA, 0xAA55, 0]
                new_val = possible_values[random.randint(0,2)]
            elif the_key == "islanding_state":
                new_val = bool(random.getrandbits(1))
            elif the_key == "island_type":
                new_val = bool(random.getrandbits(1))
            elif the_key == "bess_availability":
                new_val = bool(random.getrandbits(1))
            elif the_key == "pge_state":
                new_val = bool(random.getrandbits(1))
            elif the_key == "pcc_breaker_state":
                new_val = bool(random.getrandbits(1))
            elif the_key == "bess_pv_breaker_state":
                new_val = bool(random.getrandbits(1))
            elif the_key == "ac_frequency":
                new_val = 60
            elif the_key == "fault_condition":
                new_val = random.randint(0,10)
            else:
                new_val = random.randint(501,1000)
            self.write_int32(self.context,reg_address,new_val)
            # self.write_int32(self.context, reg_address, 5)

if __name__ == '__main__':
    modbus_dev = Modbus_Device_Simulator(config_file='server_config.yaml')
    modbus_dev.create_slave_context()
    modbus_dev.create_slave_identity()
    # modbus_dev.update_with_random_values()
    modbus_dev.set_up_looping_calls(time = 2)
    print("starting the server.. ")
    modbus_dev.create_server()
