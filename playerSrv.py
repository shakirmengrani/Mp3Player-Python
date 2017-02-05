import pygame, threading, datetime, os, sys, json
from pygame.locals import *
import mqtt_client

SOUNDENDED = 231
pygame.mixer.music.set_endevent(SOUNDENDED)
 
class player():
 def __init__(self):
  pygame.init()
  pygame.mixer.init()
  self.index = 0
  self.files = []
  self.m = mqtt_client.mqtt_client(self.on_message)
  self.window = pygame.display
  self.window.set_mode((200,200))
  self.queue()
  self.intends = {
    "actions": ["play", "listen", "stop", "silent", "quit", "pause", "unpause", "next", "change", "previous"],
    "events": {
      "play" : self.play,
      "pause" : pygame.mixer.music.pause,
      "unpause" : pygame.mixer.music.unpause,
      "stop" : pygame.mixer.music.stop,
      "next" : self.queueNext,
      "previous" : self.queuePrev,
      "pos" : self.clicked
    }
  }
  
 def processEvent(self , event):
  if (event.type == SOUNDENDED):
   self.queueNext()
   return None
  else:
   return event

 def clicked(self):
  try: 
   pygame.mixer.music.set_pos(20)
  except:
   self.queueNext()
   print("No more pos")
   pass

 def on_message(self, mqttc, obj, msg):
  #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
  if (str(msg.payload) in self.intends["events"]):
   self.intends["events"][str(msg.payload)]()
  else:
   print "operation not found"
 
 def play(self):
  pygame.mixer.music.load(self.files[self.index])
  pygame.mixer.music.play(0)

 def start(self):
  self.m.start()
  while True:
   for event in pygame.event.get():
    self.processEvent(event)
    if (event.type == pygame.QUIT):
     pygame.quit()
     self.m.mqttc.disconnect()
     sys.exit()

 def queueNext(self):
  if (self.index < len(self.files)):
   self.index = self.index + 1
  pygame.mixer.music.load(self.files[self.index])
  pygame.mixer.music.play(0)
 
 def queuePrev(self):  
  if (self.index > 0):
   self.index = self.index - 1
  pygame.mixer.music.load(self.files[self.index])
  pygame.mixer.music.play(0)

 def queue(self):
  [indexes for indexes in os.walk(os.getcwd())]
  for file in indexes[2]:
   if (str(file).split(".")[-1] == "mp3"):
    self.files.append(os.path.join(os.getcwd(),file))

 def isBusy():
  if not pygame.mixer.get_init():
   return False
  return pygame.mixer.music.get_busy()

p = player()
p.start()