inp1 = 'a1720201010201337e6aa1687d660606' \
      '2b0c89368374045c0103e80000000000' \
      '0003e900000000000000000000000000' \
      '00000000000000000000000000000000' \
      '00000000000000000000000000000000' \
      '00000000000000000000000000000000' \
      '00000000000000000000000000000000' \
      '00000000' \

inp = 'a22e020203e830280201347d2306062b' \
      '0c8936837404190301000013888ec90b' \
      '61b59ffe4d8bd6ef1fb0fd798926d400' 

inp = 'a1720201020201337e6aa1687d66' \
      '06062b0c89368374045c0103e8000000' \
      '00000003e90000000000000000000000' \
      '00000000000000000000000000000000' \
      '00000000000000000000000000000000' \
      '00000000000000000000000000000000' \
      '00000000000000000000000000000000' \
      '000000000000' 
      

input = inp1.decode('hex')

from rose import *

from pyasn1.codec.ber import decoder,encoder

print decoder.decode(input,asn1Spec=rose)[0]

stat = ROS()
result = ReturnResult()
result.setComponentByName('opcode',univ.Integer(52));
result.setComponentByName('invokeid',1000);
result.setComponentByName('args',univ.Null());
stat.setComponentByName('returnResult',result);
print encoder.encode(stat).encode('hex')


