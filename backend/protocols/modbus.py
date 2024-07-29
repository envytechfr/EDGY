from pymodbus.client.sync import ModbusTcpClient
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

class ModbusClient:
    def __init__(self, config):
        self.client = ModbusTcpClient(config['ip'], config['port'])
    
    def read_data(self, address, count):
        self.client.connect()
        result = self.client.read_holding_registers(address, count)
        self.client.close()
        return result.registers if not result.isError() else []

    def write_data(self, address, values):
        self.client.connect()
        self.client.write_registers(address, values)
        self.client.close()

class ModbusServer:
    def __init__(self, config):
        self.store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0]*100),
            co=ModbusSequentialDataBlock(0, [0]*100),
            hr=ModbusSequentialDataBlock(0, [0]*100),
            ir=ModbusSequentialDataBlock(0, [0]*100))
        self.context = ModbusServerContext(slaves=self.store, single=True)
        self.address = (config['ip'], config['port'])
    
    def start(self):
        StartTcpServer(context=self.context, address=self.address)
