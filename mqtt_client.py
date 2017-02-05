import paho.mqtt.client as mqtt, threading

class mqtt_client(threading.Thread):
 mqttc = mqtt.Client()
 def __init__(self, on_message=None):
  threading.Thread.__init__(self)
  if (on_message == None):
   self.mqttc.on_message = self.on_message
  else:
   self.mqttc.on_message = on_message
  self.mqttc.on_connect = self.on_connect
  self.mqttc.on_publish = self.on_publish
  self.mqttc.on_subscribe = self.on_subscribe
  # Uncomment to enable debug messages
  #mqttc.on_log = on_log
 
 def on_connect(self, mqttc, obj, flags, rc):
  print("rc: "+str(rc))
	
 def on_message(self, mqttc, obj, msg):
  print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

 def on_publish(self, mqttc, obj, mid):
  print("mid: "+str(mid))

 def publish(self,topic, payload):
  #if (str(payload) in self.intends["events"]):
  self.mqttc.publish(topic=topic, payload=payload)
  return "sent"
  #else:
  #return "operation not found"


 def on_subscribe(self, mqttc, obj, mid, granted_qos):
  print("Subscribed: "+str(mid)+" "+str(granted_qos))

 def on_log(self, mqttc, obj, level, string):
  print(string)
 
 def run(self):
  self.mqttc.connect("localhost", 1883, 60)
  self.mqttc.subscribe("player", 0)
  self.mqttc.loop_forever()