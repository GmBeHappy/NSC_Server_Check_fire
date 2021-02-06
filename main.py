import paho.mqtt.client as mqtt
import numpy as np

broker = 'mqtt.gmtech.co.th'
port = 1883
topic = "IR/#"
client_id = 'server'
username = 'server'
password = 'GServer_2021'

count = 0
cc = 0
full = np.array([])
a = np.array([])

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe(topic)

# Message receiving callback
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    global count 
    global cc
    global full
    global a
    aa = []
    if(msg.payload!="N" and msg.payload!="end rec" and msg.payload!="start new rec"):
        #print(msg.payload,",",end =" ")
        count = count + 1
        aa[cc] = msg.payload
        cc = cc + 1
    elif(msg.payload=="N"):
        print(aa)
        np.append(full,aa, axis = 0)
        #print("\n")
    if(count==64):
        count = 0
        print(full)

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)

# Establish a connection
client.connect(broker, port, 60)

client.loop_forever()