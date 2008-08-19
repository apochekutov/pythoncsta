import time
import socket
from acsespec import *
from rose import *
from pyasn1.codec.ber import encoder,decoder
import cstautils
import settings


class PhoneSystem:
  id = 0
  connect = None
  hostname = ('192.168.0.10',2555)
  last = time.time()
  outdebug = 0
  indebug = 0
  group = "phone"
  server = None
  mydb = None
  calls = {}
  usernames = {}


  def __init__(self,host=('192.168.0.10',2555),sendto='phone',serv=None,db=None):
    self.hostname = host
    self.connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.startup(self.hostname)
    self.group = sendto
    self.server = serv
    self.mydb = db

  def startup(self,hostname):
    self.connect.connect(hostname)
    self.connect.setblocking(0)
    self.connect.send('B')

  def timeout(self):
    tm = 20-(time.time()-self.last)
    if tm<0:
      tm=0
    return tm

  def resetTimeout(self):
    self.last = time.time()


  def SendSec(self):
    app = ApplicationContextName().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,1))
    app.setComponentByName('', univ.ObjectIdentifier('1.3.12.0.180.1'))
    # app.setComponentByName('', univ.ObjectIdentifier('1.3.12.0.218.200'))
    security = AARQ_apdu().setComponentByName('application-context-name', app)
    self.sendMess(security)



  def MakeCall(self,calling,called):
    o = invoke(10)
    o.setComponentByName('invokeid',self.NextID())
    o.setComponentByName('opcode',10)
    arg = ArgumentSeq()
    dev = DeviceID()
    dev.setComponentByName('dialingNumber',calling)
    arg.setComponentByPosition(0,dev)
    phonenum = DeviceID()
    phonenum.setComponentByName('dialingNumber',called)
    temp = ExtendedDeviceID()
    temp.setComponentByName('deviceIdentifier',phonenum)
    call = CalledDeviceID()
    call.setComponentByName('deviceIdentifier',temp)
    arg.setComponentByPosition(1,call)
    o.setComponentByName('args',arg)
    self.sendMess(o)
  
  def DTMF(self,connectionid,charactersToSend):
      if type(connectionid) != type({}):
        return
      o = invoke(19)
      o.setComponentByName('invokeid',self.NextID())
      o.setComponentByName('opcode',19)
      arg = ArgumentSeq()
      arg.setComponentByPosition(0,cstautils.toConnectionID(connectionid))
      arg.setComponentByPosition(1,char.IA5String(charactersToSend))
      o.setComponentByName('args',arg)
      self.sendMess(o)

  def SendStatus(self):
    result = invoke(52)
    result.setComponentByName('opcode',52)
    result.setComponentByName('invokeid',self.NextID())
    result.setComponentByName('args',SystemStatus(2))
    ret = Rose(52)
    ret.setComponentByName('invoke',result)
    self.sendMess(ret)
    self.resetTimeout()
    m = {}
    m["to"] = self.group
    m["type"] = "status"
    self.server.send(m)
    for key,val in self.calls.items():
      if val["callstate"] == "Delivered":
        if time.time()-val["started"] > 5 * 60:
          cstautils.writelog(self,0,key)
          del self.calls[key]

  def StartMonitor(self,ext):
    m = invoke(71)
    m.setComponentByName('invokeid',self.NextID())
    m.setComponentByName('opcode',71)
    arg = ArgumentSeq()
    mon = CSTAObject()
    dev = DeviceID()
    dev.setComponentByName('dialingNumber',ext)
    mon.setComponentByName('device',dev)
    arg.setComponentByPosition(0,mon)
    m.setComponentByName('args',arg)
    self.sendMess(m)
    
  def StartUpMonitors(self,ran):
    for i in ran:
      self.StartMonitor(i)

  def sendMess(self,mess):
    dat = encoder.encode(mess)
    if self.outdebug:
      print "Out Hex:  %s" % (dat.encode('hex'))
      print "Out ASN1: %s" % (mess)
    self.connect.send('\0' + chr(len(dat)))
    self.connect.send(dat)

  def NextID(self):
    self.id += 1
    return self.id
    
  def readmess(self):
    try:
      data = self.connect.recv(1)
      if not data:
        return ""
      full = str(data)
      data = self.connect.recv(1)
      if not data:
        return ""
      full = full + str(data)
      length = ord(data)
      got = 0
      while length>got:
        data = self.connect.recv(ord(data))
        if not data:
          return ""
        full = full + str(data)
        got = got + len(data)
      return full
    except socket.error, e:
      return full


  def handleCsta(self,data):
    if data:
      if data == "P":
        self.SendSec()
      else:
        if self.indebug:
          print "In  Hex:  %s" % (data.encode('hex'))
        if data[0] == '\00':
          data = data[2:]
        decode = decoder.decode(data,asn1Spec=Rose())[0]
        if self.indebug:
          print "In  ASN1: %s" % (decode)
        if data[0] == '\00':
          data = data[2:]
        decode = decoder.decode(data,asn1Spec=Rose())[0]
        if self.indebug:
          print "In  ASN1: %s" % (decode)
        Obj = decode.getComponent()
        if Obj.isSameTypeWith(AARE_apdu()):
          self.handleAARE(data)
        if Obj.isSameTypeWith(ReturnResult()):
          self.handleResult(data)
        if Obj.isSameTypeWith(Invoke()):
          self.handleInvoke(Obj.getComponentByName('opcode'),data)

  def handleAARE(self,data):
    decode = decoder.decode(data,asn1Spec=Rose())[0]
    print "In  ASN1: %s" % (decode)
    self.StartUpMonitors(settings.localext)

  def handleResult(self,data):
    decode = decoder.decode(data,asn1Spec=Rose())[0]
    Obj = decode.getComponent()
    ar = Obj.getComponentByName("args")
    ar = ar.getComponentByName("ResultSeq")
    if(ar.getComponentByPosition(0) not in settings.handledopcodes):
      print "In  ASN1: %s" % (decode)

  def handleInvoke(self,opcode,data):
    if(opcode == 21):
      self.handleEvent(data)
    elif(opcode == 52):
      result = ReturnResult()
      dec = decoder.decode(data,asn1Spec=Rose(opcode))[0]
      Obj = dec.getComponent()
      result.setComponentByName('opcode',52)
      result.setComponentByName('invokeid',Obj.getComponentByName('invokeid'))
      result.setComponentByName('args',univ.Null())
      self.sendMess(soc,result)
    else:
     dec = decoder.decode(data,asn1Spec=Rose(opcode))[0]
     Obj = dec.getComponent()
     print "In  ASN1: %s" % (decode)

  def handleEvent(self,data):
            dec = decoder.decode(data,asn1Spec=Rose(21))[0]
            Obj = dec.getComponent()
            # print "In  ASN1: %s" % (dec)
            args = Obj.getComponentByName("args").getComponentByName("ArgSeq")
            for i in args:
              if i.isSameTypeWith(EventTypeID()):
                typeid = i.getComponentByName("cSTAform")
              if i.isSameTypeWith(EventInfo()):
                ev = i
              if i.isSameTypeWith(MonitorCrossRefID()):
                monitorid = i
            eventinfo = cstautils.EventInfo(ev,typeid,monitorid,self)
            mess = eventinfo.toStringHash()
            mess["to"] = self.group
            mess["type"] = "phone"
            if mess.has_key("body") == None:
              mess["body"] = "Phone Event %s" % (mess["eventtype"])
            if len(eventinfo.localext):
              self.server.send(mess)
            
