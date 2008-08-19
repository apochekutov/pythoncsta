import rose
from acsespec import *
from pyasn1.type import univ, namedtype, tag, constraint, namedval, char
sec = '600aa10806062b0c00813401'
input =  sec.decode('hex')

from pyasn1.codec.ber import encoder,decoder

security = decoder.decode(input,asn1Spec=rose.rose)[0]

app = ApplicationContextName().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatConstructed,1))
app.setComponentByName('', univ.ObjectIdentifier('1.3.12.0.180.1'))
# app.setComponentByName('', univ.ObjectIdentifier('1.3.12.0.218.200'))
security = AARQ_apdu().setComponentByName('application-context-name', app)

print security

print sec
print encoder.encode(security).encode('hex')
print sec == encoder.encode(security).encode('hex')
print decoder.decode(encoder.encode(security),asn1Spec=rose.rose)[0]

