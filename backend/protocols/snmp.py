from pysnmp.hlapi import *
import threading

class SNMPClient:
    def __init__(self, config):
        self.target = config['target']
        self.port = config['port']
        self.community = config['community']
        self.version = config['version']

    def get_data(self, oid):
        iterator = getCmd(SnmpEngine(),
                          CommunityData(self.community, mpModel=self.version),
                          UdpTransportTarget((self.target, self.port)),
                          ContextData(),
                          ObjectType(ObjectIdentity(oid)))

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            print(errorIndication)
            return None
        elif errorStatus:
            print(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
            return None
        else:
            for varBind in varBinds:
                return varBind.prettyPrint().split('=')[1].strip()

    def set_data(self, oid, value):
        iterator = setCmd(SnmpEngine(),
                          CommunityData(self.community, mpModel=self.version),
                          UdpTransportTarget((self.target, self.port)),
                          ContextData(),
                          ObjectType(ObjectIdentity(oid), value))

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            print(errorIndication)
            return False
        elif errorStatus:
            print(f'{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
            return False
        else:
            return True

class SNMPTrapReceiver:
    def __init__(self, config):
        self.port = config['port']
        self.community = config['community']
        self.engine = SnmpEngine()

    def start(self):
        trap_thread = threading.Thread(target=self._start_trap_receiver)
        trap_thread.start()

    def _start_trap_receiver(self):
        from pysnmp.entity import engine, config
        from pysnmp.carrier.asyncio.dgram import udp
        from pysnmp.entity.rfc3413 import ntfrcv

        config.addV1System(self.engine, 'my-area', self.community)
        config.addTransport(
            self.engine,
            udp.domainName,
            udp.UdpTransport().openServerMode(('0.0.0.0', self.port))
        )

        def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
                  varBinds, cbCtx):
            print(f'Received new Trap message: {varBinds}')

        ntfrcv.NotificationReceiver(self.engine, cbFun)
        self.engine.transportDispatcher.jobStarted(1)

        try:
            self.engine.transportDispatcher.runDispatcher()
        except:
            self.engine.transportDispatcher.closeDispatcher()
            raise
