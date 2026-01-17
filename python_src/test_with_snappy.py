"""
This is a slightly larger testsuite requires the snappy module.

>>> PK = get_DT_tables()[0]
>>> len(PK)
3869541
>>> PK['K6a3']
'fafbdfeac.010001'
>>> PK['K8n1']
'hahbdFaGCHE.00010101'
>>> PK['16a52086']
'papbefiadkmcngojhpl.0000110111110010'
>>> PK['16n992421']
'papdeghaNbcLMOPIFJK.0000101100001111'
>>> PK['18ah_4028506']
'rarpqekhibncfrdoglmaj.000110110100100011'
>>> PK['18nh_07319980']
'rarePNkoHQlABcrgJdIFm.001011101011110000'
>>> PK['18ns_86']
'rarnDqMjOKaPlGeBhFRcI.000001010011110011'

Here's the tests from the README:

>>> import snappy
>>> import plausible_knots
>>> len(snappy.PlausibleKnots)
3869541
>>> K = snappy.PlausibleKnots[100000]; K
17nh_1645806(0,0)
>>> K.volume()
24.3340174921580
>>> M = snappy.PlausibleKnots['19nh_045358315']
>>> M.identify()
[19nh_045358315(0,0)]

"""

from .database import get_DT_tables
import sys
import doctest
import snappy

this_module = sys.modules[__name__]

def run_tests():
    result = doctest.testmod(this_module)
    print('plausible_knots: ' + repr(result))
    return result[0]

if __name__ == '__main__':
    sys.exit(run_tests())
