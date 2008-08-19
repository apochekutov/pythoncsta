import socket
from time import strftime
import json
import sys
import os

status = ''

class messclient:
  server = 0
  alldata = ''
  nest = 0
  quote = 0
  name = "Python"
  user = "SYSTEM"

  def __init__(self,myname='Python',myuser='SYSTEM'):
    self.name = myname
    self.user = myuser
    self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.server.connect(('message',50000))
    self.server.setblocking(0)

  def join(self,groupname):
    mess = {}
    mess["to"] = "service"
    mess["command"] = "join"
    mess["group"] = groupname
    self.send(mess)

  def read(self):
    m = self.realread()
    if m:
     try:
      if m['type'] == 'ping':
           reply = {}
           reply["to"] = m["sender"]
           reply["type"] = "pong"
           reply["replyfrom"] = self.name
           self.send(reply)
      if m['type'] == 'status':
           reply = {}
           reply["to"] = m["sender"]
           reply["type"] = "statusreply"
           reply["computer"] = os.uname()[1]
           reply["program"] = sys.argv[0]
           reply["screen"] = status
           self.send(reply)
     except:
      pass
         
    return m

  def send(self,mess):
    mess["user"] = self.user
    mess["realto"] = mess["to"]
    mess["date"] = strftime("%Y-%m-%dT%H:%M:%S")
    self.server.send(json.write(mess))

  
  def realread(self):
    """ Most of this is to do with reading messages char by char and fining the end of each message
       not really ideal! but its the safest method!
    """
    try:
       data = self.server.recv(1)
       self.alldata += data
       if data:
         if not self.quote:
           if data in ["{","["]:
             self.nest+=1
           elif data=="\\":
             d = server.recv(1)
             self.alldata += d
           elif data in ["}","]"]:
              self.nest-=1
         if data == "\"":
           if self.quote:
             self.nest-=1
           else:
             self.nest+=1
           self.quote = not self.quote
         if self.nest == 0:
           if len(self.alldata.strip()):
            try:
             d = json.read(self.alldata.strip())
             self.alldata = ''
             return d
            except Exception,e:
             pass
    except Exception,e:
      pass

    
    
    
    

