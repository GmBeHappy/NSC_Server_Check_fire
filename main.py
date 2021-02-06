import paho.mqtt.client as mqtt
import numpy as np

broker = 'broker.netpie.io'
port = 1883
topic = "IR/#"
client_id = '2c1fc392-c8fa-48cd-a3a3-73d00bae7911'
username = 'mJoqEwaWvphcXYkED4AokANJo7zpXvHt'
password = 'rh5w58ImDcJwuKU3O8s9vwxSXx_6kJTT'

threshold = 50
alarm = False


check_state = 0
ls = []

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe(topic)

# Message receiving callback
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    #print(msg.payload)
    global check_state , ls
    if(msg.payload=="start"):
        check_state = 1
    if(msg.payload=="end"):
        check_state = 0
    if(check_state == 1 and len(ls) < 64):
        ls.append(msg.payload)
    elif(check_state == 0 and len(ls) == 64):
        ls.pop(0)
        print(ls)
        ls.sort() 
        print('Max value : ' + ls[-1])
        if(float(ls[-1]) > threshold):
            print("Fireeeee!!!")
            client.publish('isFire',payload='fire',qos=0)
            alarm = True
        else:
            client.publish('isFire',payload='no fire',qos=0)
        ls.clear()


client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)

# Establish a connection
client.connect(broker, port, 60)

client.loop_forever()