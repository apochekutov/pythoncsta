from rose import *
from pyasn1.type import univ
import settings
import time
import pgdb
import messclient

eventtypes = {
  1: 'CallCleared',
  2: 'Conference',
  3: 'Cleared',
  4: 'Delivered',
  5: 'Diverted',
  6: 'Established',
  7: 'Failed',
  8: 'Hold',
  9: 'Reached',
  10: 'Originated',
  11: 'Queued',
  12: 'Retrieved',
  13: 'Initiated',
  14: 'Transferred',
  101: 'CallInfo',
  102: 'DoNotDistirb',
  103: 'Forwarding',
  104: 'MessageWaiting',
  201: 'AgentLoggedOn',
  202: 'AgentLoggedOff',
  203: 'AgentNotReady',
  204: 'AgentReady',
  205: 'AgentWorkNotReady',
  206: 'AgentWorkReady',
  301: 'BackInService',
  302: 'OutOfService',
  401: 'PrivateEvent'
  }

def getPhoneNum(devid):
  ret = devid.getComponent()
  if ret.isSameTypeWith(ExtendedDeviceID()):
    ret = ret.getComponent()
  if ret.isSameTypeWith(DeviceID()):
    ret = ret.getComponent()
  if ret.isSameTypeWith(univ.Null()) or str(ret) == '':
    return None
  return ret

def isLocal(phonenum):
  if phonenum in settings.localext:
    return 1
  else:
    return 0

def toConnectionID(conhash):
  conid = ConnectionID()
  conid.setComponentByName('call',conhash['call'].decode('hex'))
  ch = ConDeviceID()
  if conhash.has_key('staticID'):
    conid.setComponentByName('dstaticID',DeviceID(conhash['staticID'].decode('hex')))
  else:
    ch.setComponentByName('dynamicID',DynamicID(conhash['dynamicID'].decode('hex')))
  conid.setComponentByName('device',ch)
  return conid

def fromConnectionID(conid):
  conhash = {}
  conhash['call'] = str(conid.getComponentByName('call')).encode('hex')
  t = conid.getComponentByName('device')
  if t.getComponent().isSameTypeWith(DeviceID()):
    conhash['staticID'] = str(t.getComponent()).encode('hex')
  else:
    conhash['dynamicID'] = str(t.getComponent()).encode('hex')
  return conhash
  


class EventInfo:
  connectionid = None
  transconnection = None
  connectionid= None
  state= None
  cause= None
  extradest = None
  dest = None
  list = None
  calling = None
  called = None
  lastdiverted = None
  direction = None
  que = None
  switch = None
  state = None
  localext = []
  parties = []
  callstate = None
  hidekeys = ['hidekeys','callstate']
    

  def __init__(self,eventinfo,typeid,moniterrefid,callstate):
    self.callstate = callstate
    self.connectionid = None
    self.transconnection = None
    self.connectionid= None
    self.state= None
    self.cause= None
    self.extradest = None
    self.dest = None
    self.list = None
    self.calling = None
    self.called = None
    self.lastdiverted = None
    self.que = None
    self.switch = None
    self.state = None
    self.localext = []
    self.typeid = typeid
    self.parties = []
    for i in eventinfo:
      if i.isSameTypeWith(ConnectionID()):
        if self.connectionid:
          self.transconnection = fromConnectionID(i)
        else:
          self.connectionid=fromConnectionID(i)
      if i.isSameTypeWith(LocalConnectionState()):
        self.state=i
      if i.isSameTypeWith(univ.Enumerated()):
        self.cause=i
      if i.isSameTypeWith(SubjectDeviceID()):
        if self.dest:
          self.extradest = getPhoneNum(i)
          self.parties.append(self.extradest)
        else:
          self.dest = getPhoneNum(i)
          self.parties.append(self.dest)
      if i.isSameTypeWith(ConnectionList()):
          self.list = []
          counter = 0
          if i.getComponent().isSameTypeWith(CallInfo()):
            for j in i.getComponent():
              for k in j:
                if k.isSameTypeWith(ConnectionID()):
                  self.list.append(fromConnectionID(k))
                else:
                  if counter == 0:
                    self.calling = getPhoneNum(k)
                    self.parties.append(self.calling)
                    counter =+ 1
                  elif counter == 1:
                    self.called = getPhoneNum(k)
                    self.parties.append(self.called)
                    counter =+ 1
                  else:
                    phonenum = getPhoneNum(k)
                    if isLocal(phonenum):
                      self.localext.append(phonenum)
                    self.parties.append(phonenum)
          elif i.getComponent().isSameTypeWith(ConnectionIDList()):
            for j in i.getComponent():
              self.list.append(fromConnectionID(j))
      if i.isSameTypeWith(CallingDeviceID()):
          self.calling = getPhoneNum(i)
          self.parties.append(self.calling)
      if i.isSameTypeWith(CalledDeviceID()):
          self.called = getPhoneNum(i)
          self.parties.append(self.called)
      if i.isSameTypeWith(RedirectionDeviceID()):
          self.lastdiverted = getPhoneNum(i)
          if self.lastdiverted:
            self.parties.append(self.lastdiverted)
      if i.isSameTypeWith(univ.Integer()):
          self.que = i
      if i.isSameTypeWith(Boolean()):
          self.switch = i
      if i.isSameTypeWith(LocalConnectionState()):
        self.state = i
    if isLocal(self.dest):
       self.localext.append(self.dest)
    if isLocal(self.calling):
       self.localext.append(self.calling)
    self.localext = list(set(self.localext))
    self.parties = list(set(self.parties))
    if self.calling or self.called:
      if isLocal(self.dest):
        if isLocal(self.calling) or isLocal(self.called):
          self.direction = "Internal"
        else:
          self.direction = "Incomming"
      else:
        self.direction = "Outgoing"
    self.eventtype = eventtypes[typeid]
    if self.eventtype == 'Cleared':
      self.body = "Cleared %s (%s)" % (str(self.dest),str(self.state))
      self.removeCallState()
    elif self.eventtype == 'Transferred':
      self.removeCallState()
      self.connectionid = self.list[0]
      if self.localext.count(self.dest):
        self.localext.remove(self.dest)
      self.updateCallState()
    elif self.eventtype == 'Delivered':
      if self.direction == "Internal":
        self.body = "Delivered Internal Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      if self.direction == "Incomming":
        self.body = "Delivered Incomming Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      if self.direction == "Outgoing":
        self.body = "Delevered Outgoing Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      self.updateCallState()
    elif typeid == 6:
      if self.direction == "Internal":
        self.body = "Establised Internal Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      if self.direction == "Incomming":
        self.body = "Establised Incomming Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      if self.direction == "Outgoing":
        self.body = "Establised Outgoing Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      self.updateCallState()
    elif typeid == 9:
      if self.direction == "Internal":
        self.body = "Reached Internal Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      if self.direction == "Incomming":
        self.body = "Reached Incomming Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
      if self.direction == "Outgoing":
        self.body = "Reached Outgoing Call %s to %s (%s Dialed)" % (str(self.calling),str(self.dest),str(self.called))
    elif typeid == 10:
      if self.direction == "Internal":
        self.body = "Starting Internal Call From %s to %s" % (str(self.dest),str(self.called))
      if self.direction == "Incomming":
        self.body = "Starting Incomming Call From %s to %s"  % (str(self.dest),str(self.called))
      if self.direction == "Outgoing":
        self.body = "Starting Outgoing Call From %s to %s" % (str(self.dest),str(self.called))
    elif self.eventtype=='Hold':
      if self.callstate.calls.has_key(self.connectionid['call']):
        self.calling = self.callstate.calls[self.connectionid['call']]['calling']
        self.called = self.callstate.calls[self.connectionid['call']]['called']
    elif self.eventtype=='Retrieved':
      if self.callstate.calls.has_key(self.connectionid['call']):
        self.calling = self.callstate.calls[self.connectionid['call']]['calling']
        self.called = self.callstate.calls[self.connectionid['call']]['called']

  def updateCallState(self):
    if len(self.localext) == 0:
      return
    if not self.callstate.calls.has_key(self.connectionid['call']):
      self.callstate.calls[self.connectionid['call']] = {}
      self.callstate.calls[self.connectionid['call']]['localext'] = []
      self.callstate.calls[self.connectionid['call']]['started'] = time.time()
      self.callstate.calls[self.connectionid['call']]['callstate'] = self.eventtype
      messclient.status="%d Calls in Progress" % (len(self.callstate.calls))
    for i in self.localext:
      if self.callstate.calls[self.connectionid['call']]['localext'].count(i)==0:
        self.callstate.calls[self.connectionid['call']]['localext'].append(i)
    self.callstate.calls[self.connectionid['call']]['called'] = self.called
    self.callstate.calls[self.connectionid['call']]['calling'] = self.calling
    if self.eventtype == "Established" or self.eventtype=='Delivered':
      self.callstate.calls[self.connectionid['call']]['dest'] = self.dest

    if self.eventtype == "Established" or self.eventtype=='Transferred':
      if not self.callstate.calls[self.connectionid['call']].has_key('answered'):
        self.callstate.calls[self.connectionid['call']]['answered'] = time.time()
       
      

  def removeCallState(self):
      if self.callstate.calls.has_key(self.connectionid['call']):
        for i in self.localext:
          if self.callstate.calls[self.connectionid['call']]['localext'].count(i):
            self.callstate.calls[self.connectionid['call']]['localext'].remove(i)
        if len(self.callstate.calls[self.connectionid['call']]['localext'])==0:
          writelog(self.callstate,self.dest,self.connectionid['call'])
          del self.callstate.calls[self.connectionid['call']]
          messclient.status="%d Calls in Progress" % (len(self.callstate.calls))

  def __repr__(self):
    return repr(self.__dict__)
  
  def toStringHash(self):
    di = {}
    for key,val in self.__dict__.items():
      if type(val) == type([]):
        di[key] = map(str,val)
      elif type(val) == type({}):
        di[key] = maphash(str,val)
      elif key in self.hidekeys:
        pass
      elif val is None:
        pass
      else:
        di[key] = str(val)
    return di

def maphash(func,hash):
  newhash = {}
  for key,val in hash.items():
    newhash[key] = func(val)
  return newhash
    
  
    
def writelog(callstate, des, call):
          if callstate.mydb:
            query = "insert into phonelog (type,turret,phonenum,ddn,started,answered,ended,username) values (%s,%d,%s,%s,%s,%s,%s,%s);"
            ext = str(des)
            calling = callstate.calls[call]['calling']
            called = callstate.calls[call]['called']
            dest = None
            if callstate.calls[call].has_key('dest'):
              dest = callstate.calls[call]['dest']
            started = pgdb.TimestampFromTicks(callstate.calls[call]['started'])
            direction = None
            if isLocal(called) or isLocal(dest):
              if des == 0:
               ext = dest
              if isLocal(calling):
                direction = "Internal"
              else:
                direction = "Incomming"
            else:
              if des == 0:
               ext = calling
              direction = "Outgoing"
            answered = None
            if not callstate.calls[call].has_key('answered'):
              if direction == 'Outgoing':
                direction = 'Failed'
              elif direction == 'Internal':
                direction = 'IntLost'
              else:
                direction = 'Lost'
            else:
              answered = pgdb.TimestampFromTicks(callstate.calls[call]['answered'])
            username = None
            if callstate.usernames.has_key(ext):
              username = callstate.usernames[ext]
            ended = pgdb.TimestampFromTicks(time.time())
            cur = callstate.mydb.cursor();
            if direction == "Internal":
              cur.execute(query, ("T",int(str(dest)),str(calling),str(called),started,answered,ended,username))
            elif direction == "Incomming":
              cur.execute( query, ("N",int(str(ext)),str(calling),str(called),started,answered,ended,username))
            elif direction == "Lost":
              cur.execute( query, ("L",int(str(ext)),str(calling),str(called),started,answered,ended,username))
            elif direction == "Outgoing":
              cur.execute(query, ("O",int(str(ext)),str(called),str(calling),started,answered,ended,username))
            elif direction == "Failed":
              cur.execute(query, ("F",int(str(ext)),str(called),str(calling),started,answered,ended,username))
            elif direction == "IntLost":
              cur.execute(query, ("X",int(str(ext)),str(calling),str(called),started,answered,ended,username))

