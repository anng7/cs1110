# a1test.py
# Quinn Beightol (qeb2), Mengyun Xia (mx48)
# September 16, 2012
"""Unit test for module a1

When run as an application, this module invokes several 
procedures that test the various functions in the module 
a1."""

import cunittest
from a1 import *

def testA():
    """Tests the functions before_space() and after_space()"""
    
    cunittest.assert_equals("0.814663951",before_space("0.814663951 Euros"))
    cunittest.assert_equals("Euros",after_space("0.814663951 Euros"))


def testB():
    """Tests first_inside_quotes(), get_lhs(), and get_rhs()"""
    
    #Test first_inside_quotes():
    cunittest.assert_equals("cake",first_inside_quotes("The \"cake\" is a lie"))
    cunittest.assert_equals("cake",
                            first_inside_quotes("The \"cake\" is a \"lie\""))

    #Test get_lhs():
    cunittest.assert_equals("42 Euros",get_lhs(
        '{lhs: "42 Euros",rhs: "171.43569717129 Polish zloty",error: "",icc: true}'))
    cunittest.assert_equals("0.7734 Canadian dollars",
                            get_lhs('{lhs: "0.7734 Canadian dollars",rhs: "0.78231730165439 U.S. dollars",error: "",icc: true}'))
    cunittest.assert_equals("",get_lhs('{lhs: "",rhs: "",error: "4",icc: false}'))
    
    #Test get_rhs():
    cunittest.assert_equals("171.43569717129 Polish zloty",
                            get_rhs('{lhs: "42 Euros",rhs: "171.43569717129 Polish zloty",error: "",icc: true}'))
    cunittest.assert_equals("0.78231730165439 U.S. dollars",
                            get_rhs('{lhs: "0.7734 Canadian dollars",rhs: "0.78231730165439 U.S. dollars",error: "",icc: true}'))
    cunittest.assert_equals("",get_rhs('{lhs: "",rhs: "",error: "4",icc: false}'))


def testC():
    """Tests currency_response()"""
    
    cunittest.assert_equals(
        '{lhs: "1 U.S. dollar",rhs: "4.60600254 Argentine pesos",error: "",icc: true}',
        currency_response(1.0,"USD","ARS"))
    cunittest.assert_equals('{lhs: "",rhs: "",error: "4",icc: false}',
                            currency_response(1.0,"USA","ARS"))
    cunittest.assert_equals('{lhs: "",rhs: "",error: "4",icc: false}',
                            currency_response(1.0,"USD","TRI"))


def testD():
    """Tests iscurrency() and exchange()"""
    
    #Test iscurrency():
    cunittest.assert_true(iscurrency('USD'))
    cunittest.assert_true(iscurrency('BOB'))
    cunittest.assert_true(iscurrency('pen'))
    cunittest.assert_true(not iscurrency('Sexual favors'))          #damn it...
    cunittest.assert_true(not iscurrency('NIN'))

    #Test exchange():
    cunittest.assert_floats_equal(0.25593749975655,exchange(24,'NPR','AUD'))
    cunittest.assert_floats_equal(0,exchange(0,'UZS','VND'))


if __name__ == '__main__':
    testA()
    testB()
    testC()
    testD()
    print "Module a1 is working correctly"
    