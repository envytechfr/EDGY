import paho.mqtt.client as mqtt
import threading

class MQTTClient:
    def __init__(self, config):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(config['broker'], config['port'], 60)
        self.topics = config['topics']
        self.messages = []
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        for topic in self.topics:
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        self.messages.append((msg.topic, msg.payload.decode()))

    def get_message(self, topic):
        for t, m in self.messages:
            if t == topic:
                return m
        return None

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def stop(self):
        self.client.loop_stop()

class MQTTBroker:
    def __init__(self, config):
        self.config = config

    def start(self):
        broker_thread = threading.Thread(target=self._start_broker)
        broker_thread.start()

    def _start_broker(self):
        import subprocess
        subprocess.run(["mosquitto", "-c", self.config['config_file']])

    def stop(self):
        import subprocess
        subprocess.run(["pkill", "mosquitto"])
