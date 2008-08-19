#!/usr/bin/python

import socket
import select
import types
import time
import pgdb
import messclient
import sys
import phonesystem
indebug = 0
outdebug = 0
testing=0
server = None
if testing:
  server = messclient.messclient(myname='Phone',myuser="TestPhone")
  group= "testphone"
else:
  server = messclient.messclient(myname='Phone',myuser="Phone")
  group = "phone"

messclient.status="Phone System Startup"
server.join(group)
server.join(group+"ping")

mydb = None
if not testing:
  mydb = pgdb.connect(database="express",host="dbaseserver",user="sts")
else:
  mydb = pgdb.connect(database="express",host="testserver",user="sts")
if mydb:
  cur = mydb.cursor()
  cur.execute("commit;")





def processMess(so,m):
    global count
    if type(m) != type({}):
      return None
    if m.has_key('turret') and m.has_key('user'):
      so.usernames[m['turret']] = m['user']
    if not m.has_key("op"):
      return None
    print m
    if m["op"] == "MakeCall":
      so.MakeCall(m['calling'],m['called'])
    if m["op"] == "DTMF":
      so.DTMF(m['connectionid'],m['charactersToSend'])
    if m["op"] == "Query":
      pass
    
          

HOST = '192.168.0.10'
PORT = 2555

so = phonesystem.PhoneSystem((HOST,PORT),group,server,mydb)


socopen = 1
last=time.time()
while socopen:
  sin,sout,serr = select.select([so.connect,server.server],[],[so.connect,server.server],so.timeout()+0.1)
  for income in sin:
    if income==server.server:
      mess = server.read()
      if mess:
        processMess(so,mess)
    data=""
    if income == so.connect:
      try:
        data = so.readmess()
      except StandardError,e:
        print e
        socopen = 0
      so.handleCsta(data)
  if not sin and not sout and not serr or so.timeout()==0:
    so.SendStatus()

    
