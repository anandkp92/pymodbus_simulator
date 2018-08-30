# from get_modbus import Get_Modbus_Data
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from modbus_driver import Modbus_Driver
# from local_db import Influx_Database_class
# import time

# obj =  ModbusClient('127.0.0.1', '5020')
# print(obj)
obj = Modbus_Driver(config_file='config.yaml')
obj.initialize_modbus()

# local_db = Influx_Database_class(config_type="local")
# remote_db = Influx_Database_class(config_type="remote")

print("heartbeat: ", obj.decode_register(0, '32int'))

print("real_power_setpoint: ", obj.decode_register(2, '32float'))
print("reactive_power_setpoint: ", obj.decode_register(4, '32float'))
print("target_real_power: ", obj.decode_register(6, '32float'))
print("target_reactive_power: ", obj.decode_register(8, '32float'))
print("battery_total_capacity: ", obj.decode_register(10, '32float'))
print("battery_current_stored_energy: ", obj.decode_register(12, '32float'))
print("total_actual_real_power: ", obj.decode_register(14, '32float'))
print("total_actual_reactive_power: ", obj.decode_register(16, '32float'))
print("total_actual_apparent_power: ", obj.decode_register(18, '32float'))

print("active_power_output_limit: ", obj.decode_register(20, '32float'))
print("current_power_production: ", obj.decode_register(22, '32float'))
print("ac_current_phase_a: ", obj.decode_register(24, '32float'))
print("ac_current_phase_b: ", obj.decode_register(26, '32float'))
print("ac_current_phase_c: ", obj.decode_register(28, '32float'))
print("ac_voltage_ab: ", obj.decode_register(30, '32float'))
print("ac_voltage_bc: ", obj.decode_register(32, '32float'))
print("ac_voltage_ca: ", obj.decode_register(34, '32float'))
print("ac_frequency: ", obj.decode_register(36, '32float'))

print("islanding_state: ", obj.decode_register(38, '32int'))
print("island_type: ", obj.decode_register(40, '32int'))
print("bess_availability: ", obj.decode_register(42, '32int'))
print("fault_condition: ", obj.decode_register(44, '32int'))
print("pge_state: ", obj.decode_register(46, '32int'))
print("pcc_breaker_state: ", obj.decode_register(48, '32int'))
print("pge_voltage: ", obj.decode_register(50, '32float'))
print("pge_frequency: ", obj.decode_register(52, '32float'))
print("bess_pv_breaker_state: ", obj.decode_register(54, '32int'))

# print(obj.decode_register(0x2001, '32float'))
	# local_db.push_json_to_db(data=data)
	# time.sleep(1)

	# if i%10 == 0 and i!=0:
	# 	time_now = time.time()
	# 	local_data = local_db.read_from_db(time_now=time_now)
	# 	print("length of data in local db:", len(local_data))

	# 	remote_db.push_df_to_db(df=local_data)
	# 	remote_data = remote_db.read_from_db(time_now=time_now)
	# 	print("length after remote push = ",len(remote_data))

	# 	local_db.delete_from_db(time_now=time_now)
	# 	local_data2 = local_db.read_from_db(time_now=time_now)
	# 	print("length after deleting from local = ", len(local_data2))
	# i+=1
