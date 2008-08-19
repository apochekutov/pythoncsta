
from pyasn1.type import univ, namedtype, tag, constraint, namedval, char

from acsespec import *



class CSTASecurityData(univ.Sequence):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('messageSequenceNumber',univ.Integer())
    )

class CSTAPrivateDataData(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.NamedType('string',univ.OctetString()),
    namedtype.NamedType('integer',univ.Integer())
    )


class CSTAPrivateData(univ.Sequence):
  componentType = namedtype.NamedTypes(
    namedtype.NamedType('manufacturer',univ.ObjectIdentifier()),
    namedtype.NamedType('data',CSTAPrivateDataData())
    )
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatConstructed,29))
class CSTAPrivateData_list(univ.SequenceOf):
  componentType=CSTAPrivateData()
  
class CSTACommonArguments(univ.Sequence):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('security',CSTASecurityData().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.OptionalNamedType('privateData',CSTAPrivateData_list().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,1)))
    )
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatConstructed,30))

class SystemStatus(univ.Enumerated):
  pass


class SystemStatusResult(univ.Sequence):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('opcode',univ.Integer()),
    namedtype.OptionalNamedType('priv',CSTAPrivateData()),
    namedtype.OptionalNamedType('null',univ.Null())
    )

class NumberDigits(char.IA5String):
  pass

class DeviceNumber(univ.Integer):
  pass

class DeviceID(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('dialingNumber',NumberDigits().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.NamedType('deviceNumber',DeviceNumber().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1)))
    )

class DynamicID(univ.OctetString):
  tagSet = univ.OctetString.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,3))

class ConDeviceID(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('staticID',DeviceID()),
    namedtype.NamedType('dynamicID',DynamicID())
    )

class ConnectionID(univ.Sequence):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('call',univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2))),
    namedtype.OptionalNamedType('device',ConDeviceID())
    )
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatConstructed,11))

class MonitorCrossRefID(univ.OctetString):
  tagSet = univ.OctetString.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,21))

class PublicTON(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,3))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,4))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,5))),
    
    )

class OtherPlan(univ.OctetString):
  pass

class PrivateTON(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,3))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,4))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,5))),
    namedtype.NamedType('unknown',char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,6))),
    
    )

class InternalNum(NumberDigits):
  tagSet = univ.OctetString.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext,tag.tagFormatSimple,4))

class ExtendedDeviceID(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('deviceIdentifier',DeviceID()),
    namedtype.OptionalNamedType('implicitPublic',NumberDigits().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2))),
    namedtype.OptionalNamedType('explicitPublic',PublicTON().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,3))),
    namedtype.OptionalNamedType('implicitPrivate',InternalNum()),
    namedtype.OptionalNamedType('explicitPrivate',PrivateTON().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,5))),
    namedtype.OptionalNamedType('other',OtherPlan().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,6)))
    )

class NoOfCallsInQueue(univ.Integer):
  pass

class ConnectionIDList(univ.SequenceOf):
  tagSet = univ.SequenceOf.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,12))
  componentType=ConnectionID()

class CallInfoDetail(univ.Sequence):
  componentType = namedtype.NamedTypes(
    namedtype.NamedType('endpoint',ConnectionID()),
    namedtype.OptionalNamedType('staticEndpoint',DeviceID())
  )

class CallInfo(univ.SequenceOf):
  tagSet = univ.SequenceOf.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,13))
  componentType=CallInfoDetail()


class ConnectionList(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('connections',ConnectionIDList()),
    namedtype.OptionalNamedType('callInformation',CallInfo())
    )
  
class CallingDeviceID(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('deviceIdentifier',ExtendedDeviceID()),
    namedtype.OptionalNamedType('notKnown',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,7))),
    namedtype.OptionalNamedType('notRequired',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,8)))
    )
  tagSet = univ.Choice.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,1))

class CalledDeviceID(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('deviceIdentifier',ExtendedDeviceID()),
    namedtype.OptionalNamedType('notKnown',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,7))),
    namedtype.OptionalNamedType('notRequired',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,8)))
    )
  tagSet = univ.Choice.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,2))

class SubjectDeviceID(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('deviceIdentifier',ExtendedDeviceID()),
    namedtype.OptionalNamedType('notKnown',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,7))),
    namedtype.OptionalNamedType('notRequired',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,8)))
    )
  tagSet = univ.Choice.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,3))

class RedirectionDeviceID(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('deviceIdentifier',ExtendedDeviceID()),
    namedtype.OptionalNamedType('notKnown',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,7))),
    namedtype.OptionalNamedType('notRequired',univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,8)))
    )
  tagSet = univ.Choice.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,4))

  
class CSTAObject(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('device',DeviceID()),
    namedtype.NamedType('call',ConnectionID())
    )
class MonitorObject(CSTAObject):
  pass

class LocalConnectionState(univ.Enumerated):
  tagSet = univ.Enumerated.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,14))


class Boolean(univ.Integer):
  tagSet = univ.Enumerated.tagSet.tagImplicitly(tag.Tag(tag.tagClassUniversal,tag.tagFormatSimple,1))

class EventInfoParts(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('call',ConnectionID()),
    namedtype.OptionalNamedType('controller',SubjectDeviceID()),
    namedtype.OptionalNamedType('callingDevice',CallingDeviceID()),
    namedtype.OptionalNamedType('calledDevice',CalledDeviceID()),
    namedtype.OptionalNamedType('lastRedirectionDevice',RedirectionDeviceID()),
    namedtype.OptionalNamedType('numberedQueued',NoOfCallsInQueue()),
    namedtype.OptionalNamedType('conferenceconnections',ConnectionList()),
    namedtype.OptionalNamedType('localConnectInfo',LocalConnectionState()),
    namedtype.OptionalNamedType('cause',univ.Enumerated()),
    namedtype.OptionalNamedType('switch',Boolean()),
    namedtype.OptionalNamedType('test',univ.Sequence()),
    namedtype.OptionalNamedType('test',univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0)))
    )

class EventInfo(univ.SequenceOf):
  componentType = EventInfoParts()

  
class ArgumentSeqParts(univ.Choice):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('crossRefIdentifier',MonitorCrossRefID()),
    namedtype.OptionalNamedType('eventType',univ.Integer()),
    namedtype.OptionalNamedType('systemStatus',SystemStatus()),
    namedtype.OptionalNamedType('moniterObject',MonitorObject()),
    namedtype.OptionalNamedType('extensions',CSTACommonArguments()),
    namedtype.OptionalNamedType('eventInfo',EventInfo()),
    namedtype.OptionalNamedType('cstaprivatedata',CSTAPrivateData())
    )

class ArgumentSeq(univ.SequenceOf):
  componentType=ArgumentSeqParts()

class EventTypeID(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType("cSTAform",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    )


def argumentseq(op=-1):
  jack = namedtype.NamedTypes(
    namedtype.OptionalNamedType('crossRefIdentifier',MonitorCrossRefID()),
    namedtype.OptionalNamedType('eventType',univ.Integer()),
    namedtype.OptionalNamedType('systemStatus',SystemStatus()),
    namedtype.OptionalNamedType('moniterObject',MonitorObject()),
    namedtype.OptionalNamedType('extensions',CSTACommonArguments()),
    namedtype.OptionalNamedType('eventInfo',EventInfo()),
    namedtype.OptionalNamedType('cstaprivatedata',CSTAPrivateData())
    )
  if(op==21):
    jack=namedtype.NamedTypes(
      namedtype.OptionalNamedType('crossRefIdentifier',MonitorCrossRefID()),
      namedtype.OptionalNamedType('systemStatus',SystemStatus()),
      namedtype.OptionalNamedType('eventType',EventTypeID()),
      namedtype.OptionalNamedType('extensions',CSTACommonArguments()),
      namedtype.OptionalNamedType('eventInfo',EventInfo()),
      namedtype.OptionalNamedType('cstaprivatedata',CSTAPrivateData())
      )
  return univ.SequenceOf(componentType=univ.Choice(componentType=jack))

  



  


class ErrorArgs(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType("null",univ.Null()),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2))),
    )



def args(op=-1):
  ret = univ.Choice(componentType=namedtype.NamedTypes(
      namedtype.OptionalNamedType("null",univ.Null()),
      namedtype.OptionalNamedType("ArgSeq",argumentseq(op)),
      namedtype.OptionalNamedType("systemStatus",CSTACommonArguments()),
      namedtype.OptionalNamedType("enum",univ.Enumerated())
      ))
  return ret

  

class MonitorFilter(univ.Sequence):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType("call",univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.OptionalNamedType("feature",univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
    namedtype.OptionalNamedType("agent",univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2))),
    namedtype.OptionalNamedType("maintenance",univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,3))),
    namedtype.OptionalNamedType("private",univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,4)))
    )
class MonitorStartResult(univ.Sequence):
  componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('crossRefIdentifier',MonitorCrossRefID()),
    namedtype.OptionalNamedType('monitorFilter',MonitorFilter())
    )

class ResultSeq(univ.SequenceOf):
  componentType = univ.Choice(componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType('opcode',univ.Integer()),
    namedtype.OptionalNamedType('priv',CSTAPrivateData()),
    namedtype.OptionalNamedType('monitorFilter',MonitorStartResult()),
    namedtype.OptionalNamedType('null',univ.Null()),
    namedtype.NamedType('initiatedCall',ConnectionID())
    ))
  
class Result(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType("null",univ.Null()),
    namedtype.OptionalNamedType("ResultSeq",ResultSeq()),
    )
class RejectArgs(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType("null",univ.Null()),
    namedtype.OptionalNamedType("systemStatus",univ.Integer()),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2))),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,3))),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,4))),
    namedtype.OptionalNamedType("systemStatus",univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,5)))
    )

class Invoke(univ.Sequence):
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,1))

def invoke(op=-1):
  ret=Invoke(componentType=namedtype.NamedTypes(
      namedtype.NamedType('invokeid',univ.Integer()),
      namedtype.OptionalNamedType('opcode',univ.Integer()),
      namedtype.OptionalNamedType('args',args(op))
      ))
  return ret
    

class ReturnResult(univ.Sequence):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('invokeid',univ.Integer()),
    namedtype.OptionalNamedType('opcode',univ.Integer()),
    namedtype.NamedType('args',Result())
    )
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,2))
  
class ReturnError(univ.Sequence):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('invokeid',univ.Integer()),
    namedtype.OptionalNamedType('opcode',univ.Integer()),
    namedtype.NamedType('args',ErrorArgs())
    )
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,3))
class Reject(univ.SequenceOf):
  componentType=RejectArgs()
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,4))


def Rose(op=-1):
  ros = univ.Choice(componentType = namedtype.NamedTypes(
    namedtype.NamedType("invoke",invoke(op)),
    namedtype.NamedType("returnResult",ReturnResult()),
    namedtype.NamedType("returnError",ReturnError()),
    namedtype.NamedType("reject",Reject()),
    namedtype.NamedType("AARQ-apdu",AARQ_apdu()),
    namedtype.NamedType("AARE-apdu",AARE_apdu()),
    namedtype.NamedType("ABRT-apdu",ABRT_apdu()),
    ))
  return ros



rose = Rose()
