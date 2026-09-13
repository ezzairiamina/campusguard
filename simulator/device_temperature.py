import time 
import random 
import json 
import ssl
import paho.mqtt.client as mqtt

BROKER_HOST = "5648f4b7dea146cf9ff1f97dfd9d98d0.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
USERNAME = "campusguard_device"
PASSWORD = "Amina@123)($$%/(FDTHV"


DEVICE_ID = "temp_sensor_batiment_A"
TOPIC = f"campusguard/{DEVICE_ID}/data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{DEVICE_ID}] Connecté au broker avec succès.")
    else:
        print(f"[{DEVICE_ID}] Échec de connexion, code : {rc}")

def generate_temperature():
    # Température réaliste autour de 22°C avec un peu de bruit
    return round(random.gauss(22, 1.5), 2)

def main():
    client = mqtt.Client(client_id=DEVICE_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    client.on_connect = on_connect

    client.connect(BROKER_HOST, BROKER_PORT)
    client.loop_start()

    try:
        while True:
            payload = {
                "device_id": DEVICE_ID,
                "type": "temperature",
                "value": generate_temperature(),
                "timestamp": time.time(),
            }
            client.publish(TOPIC, json.dumps(payload))
            print(f"[{DEVICE_ID}] Envoyé : {payload}")
            time.sleep(5)
    except KeyboardInterrupt:
        print(f"[{DEVICE_ID}] Arrêt du simulateur.")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()