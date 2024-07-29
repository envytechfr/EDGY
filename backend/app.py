from flask import Flask, request, jsonify
from flask_cors import CORS
from protocols.modbus import ModbusClient, ModbusServer
from protocols.mqtt import MQTTClient, MQTTBroker
from protocols.snmp import SNMPClient, SNMPTrapReceiver
from protocols.bacnet import BACnetClient
import json

app = Flask(__name__)
CORS(app)

# Global configuration storage
configurations = {
    'modbus_clients': [],
    'modbus_servers': [],
    'mqtt_clients': [],
    'mqtt_brokers': [],
    'snmp_clients': [],
    'snmp_trap_receivers': [],
    'bacnet_clients': []
}

# Login route (for simplicity, without tokens)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'password':
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

# Configure and route data for each protocol
@app.route('/api/configure', methods=['POST'])
def configure():
    data = request.get_json()
    protocol = data['protocol']
    config = data['config']

    if protocol == 'modbus':
        if config['type'] == 'client':
            client = ModbusClient(config)
            configurations['modbus_clients'].append(client)
        elif config['type'] == 'server':
            server = ModbusServer(config)
            configurations['modbus_servers'].append(server)
            server.start()
    elif protocol == 'mqtt':
        if config['type'] == 'client':
            client = MQTTClient(config)
            configurations['mqtt_clients'].append(client)
            client.start()
        elif config['type'] == 'broker':
            broker = MQTTBroker(config)
            configurations['mqtt_brokers'].append(broker)
            broker.start()
    elif protocol == 'snmp':
        if config['type'] == 'client':
            client = SNMPClient(config)
            configurations['snmp_clients'].append(client)
        elif config['type'] == 'trap_receiver':
            trap_receiver = SNMPTrapReceiver(config)
            configurations['snmp_trap_receivers'].append(trap_receiver)
            trap_receiver.start()
    elif protocol == 'bacnet':
        client = BACnetClient(config)
        configurations['bacnet_clients'].append(client)
    
    return jsonify({'message': 'Configuration saved'}), 200

@app.route('/api/data', methods=['POST'])
def route_data():
    data = request.get_json()
    source_protocol = data['source_protocol']
    source_config = data['source_config']
    destination_protocol = data['destination_protocol']
    destination_config = data['destination_config']
    data_to_route = data['data']

    # Fetch data from source
    if source_protocol == 'modbus':
        client = ModbusClient(source_config)
        fetched_data = client.read_data(data_to_route['address'], data_to_route['count'])
    elif source_protocol == 'mqtt':
        client = MQTTClient(source_config)
        fetched_data = client.get_message(data_to_route['topic'])
    elif source_protocol == 'snmp':
        client = SNMPClient(source_config)
        fetched_data = client.get_data(data_to_route['oid'])
    elif source_protocol == 'bacnet':
        client = BACnetClient(source_config)
        fetched_data = client.read_data(data_to_route['address'])

    # Route data to destination
    if destination_protocol == 'modbus':
        client = ModbusClient(destination_config)
        client.write_data(destination_config['address'], fetched_data)
    elif destination_protocol == 'mqtt':
        client = MQTTClient(destination_config)
        client.publish(destination_config['topic'], fetched_data)
    elif destination_protocol == 'snmp':
        client = SNMPClient(destination_config)
        client.set_data(destination_config['oid'], fetched_data)
    elif destination_protocol == 'bacnet':
        client = BACnetClient(destination_config)
        client.write_data(destination_config['address'], fetched_data)
    
    return jsonify({'message': 'Data routed successfully', 'fetched_data': fetched_data}), 200

# Network configuration route
@app.route('/api/configure_network', methods=['POST'])
def configure_network():
    data = request.get_json()
    if data['connection_type'] == 'LAN':
        with open('/etc/network/interfaces', 'w') as file:
            file.write(f"auto eth0\niface eth0 inet static\naddress {data['ip_address']}\nnetmask {data['netmask']}\ngateway {data['gateway']}")
    elif data['connection_type'] == 'WiFi':
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as file:
            file.write(f"network={{\nssid=\"{data['ssid']}\"\npsk=\"{data['password']}\"\n}}")
    return jsonify({'message': 'Network configuration updated'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
