

from pyasn1.type import univ, namedtype, tag, constraint, namedval, char
class ProtocolVersion(univ.BitString):
  pass

class ApplicationContextName(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('',univ.ObjectIdentifier())
    )

class APtitle(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('AP-title-form1',univ.OctetString()),
    namedtype.NamedType('AP-title-form2',univ.ObjectIdentifier())
    )

  
class APInvocationIdentifier(univ.Integer):
  pass

class AEInvocationIdentifier(univ.Integer):
  pass

class Encoding(univ.Choice):
   componentType=namedtype.NamedTypes(
     namedtype.NamedType('single-ASN1-type',univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
     namedtype.NamedType('octet-aligned',univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
     namedtype.NamedType('arbitrary',univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2)))
     )

class External(univ.Sequence):
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassUniversal,tag.tagFormatConstructed,8))
  componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType('direct-reference',univ.ObjectIdentifier()),
    namedtype.OptionalNamedType('indirect-reference',univ.Integer()),
    namedtype.OptionalNamedType('data-value-descriptor',univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassUniversal,tag.tagFormatSimple,7))),
    namedtype.NamedType('encoding',Encoding()),
    )


class AEQualifier(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('AE-qualifier-form1',univ.OctetString()),
    namedtype.NamedType('AE-qualifier-form2',univ.Integer()),
    )

class ASCE_requirements(univ.BitString):
  pass

class Mechanism_name(univ.ObjectIdentifier):
  pass
class Authentication_value(univ.Choice):
  pass
class Application_context_name_list(univ.SequenceOf):
  componentType=ApplicationContextName()
class Implemation_Data(char.GraphicString):
  pass
class Association_information(univ.SequenceOf): 
  componentType=External()
class Associate_result(univ.Integer):
  pass
class Associate_source_diagnostic(univ.Choice):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('asce-service-user',univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
    namedtype.NamedType('asce-service-provider',univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,2)))
    )

class AARQ_apdu(univ.Sequence):
  componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType('protocol-version',univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.OptionalNamedType('application-context-name',ApplicationContextName().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,1))),
    namedtype.OptionalNamedType('called-AP-title',APtitle().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple, 2))),
    namedtype.OptionalNamedType('called-AE-qualifier',AEQualifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,3))),
    namedtype.OptionalNamedType('called-AP-invocation-identifier',APInvocationIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,4))),
    namedtype.OptionalNamedType('called-AE-invocation-identifier',AEInvocationIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,5))),
    namedtype.OptionalNamedType('calling-AP-title',APtitle().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple, 6))),
    namedtype.OptionalNamedType('calling-AE-qualifier',AEQualifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,7))),
    namedtype.OptionalNamedType('calling-AP-invocation-identifier',APInvocationIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,8))),
    namedtype.OptionalNamedType('calling-AE-invocation-identifier',AEInvocationIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,9))),
    namedtype.OptionalNamedType('sender-acse-requirements',ASCE_requirements().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,10))),
    namedtype.OptionalNamedType('mechanism-name',Mechanism_name().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,11))),
    namedtype.OptionalNamedType('calling-authentication-value',Authentication_value().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,12))),
    namedtype.OptionalNamedType('application-context-name-list',Application_context_name_list().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,13))),
    namedtype.OptionalNamedType('implementation-information',Implemation_Data().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,29))),
    namedtype.OptionalNamedType('user-information',Association_information().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,30)))
    )
    
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatConstructed,0))

class AARE_apdu(univ.Sequence):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('protocol-version',univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.NamedType('application-context-name',ApplicationContextName().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,1))),
    namedtype.NamedType('result',Associate_result().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple, 2))),
    namedtype.NamedType('result-source-diagnostic',Associate_source_diagnostic().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed, 3))),
    namedtype.OptionalNamedType('called-AP-title',APtitle().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple, 4))),
    namedtype.OptionalNamedType('called-AE-qualifier',AEQualifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,5))),
    namedtype.OptionalNamedType('called-AP-invocation-identifier',APInvocationIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,6))),
    namedtype.OptionalNamedType('called-AE-invocation-identifier',AEInvocationIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,7))),
    namedtype.OptionalNamedType('sender-acse-requirements',ASCE_requirements().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,8))),
    namedtype.OptionalNamedType('mechanism-name',Mechanism_name().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,9))),
    namedtype.OptionalNamedType('calling-authentication-value',Authentication_value().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,10))),
    namedtype.OptionalNamedType('application-context-name-list',Application_context_name_list().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,11))),
    namedtype.OptionalNamedType('implementation-information',Implemation_Data().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,29))),
    namedtype.OptionalNamedType('user-information',Association_information().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,30)))
    )
    
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatConstructed,1))

class ABRT_diagnostic(univ.Enumerated):
  pass

class ABRT_source(univ.Integer):
  pass

class ABRT_apdu(univ.Sequence):
  componentType=namedtype.NamedTypes(
    namedtype.NamedType('abort-source',ABRT_source().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))),
    namedtype.OptionalNamedType('abort-diagnostic',ABRT_diagnostic().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1))),
    namedtype.OptionalNamedType('user-information',Association_information().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,30)))
    )
    
  tagSet = univ.Sequence.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication,tag.tagFormatConstructed,4))
