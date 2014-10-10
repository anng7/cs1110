# unittest.py
# Walker M. White (wmw2)
# August 24, 2012
"""Unit test support functions

This module provides "user friendly" assert functions"""
import traceback
import math

def assert_equals(expected,received):
    """Quit the program if expected and received differ, printing minimal debug info
    
    Example printouts:
        Expected 4 but instead got 5
        line 1 of <stdin>
        Quitting with Error
    
        Expected 'Hi there' but instead got 'i there'
        Line 32 of /Users/me/classes/cs1110/scratch/a1/a1test.py: assertEquals("Hi there", myvar)
        Quitting with Error"""
    
    if (expected != received):
        stack = traceback.extract_stack()
        frame = stack[-2]
        print "Expected " + `expected` + " but instead got " + `received`
        if (frame[3] is None):
            suffix = ""
        else:
            suffix = ": "+frame[3]
        print "Line "+`frame[1]`+" of "+ frame[0] + suffix
        print "Quitting with Error"
        quit()


def assert_true(received):
    """Quits the program if received is not true, printing minimal debug info
    
    Example printouts:
        Expected True but instead got False
        line 1 of <stdin>
        Quitting with Error
    
        Expected True but instead got False
        Line 32 of /Users/me/classes/cs1110/scratch/a1/a1test.py: assertTrue(myvar)
        Quitting with Error"""
    
    if (not received):
        stack = traceback.extract_stack()
        frame = stack[-2]
        print "Expected True but instead got False"
        if (frame[3] is None):
            suffix = ""
        else:
            suffix = ": "+frame[3]
        print "Line "+`frame[1]`+" of "+ frame[0] + suffix
        print "Quitting with Error"
        quit()

def assert_floats_equal(expected,received):
    """Quit the program if the floats expected and received differ, printing minimal debug info
    
    This function is different from assert_equals in that it takes into
    consideration that floats have a limited number of significant digits.
    The floats are clamped before comparing them.
    
    Example printouts:
        Expected 4.5 but instead got 5.315
        line 1 of <stdin>
        Quitting with Error
    
        Expected 0.4 but instead got 0.3
        Line 32 of /Users/me/classes/cs1110/scratch/a1/a1test.py: assertEquals(0.4, 0.1+0.2)
        Quitting with Error"""
    
    exp = clamp_float(expected)
    rec = clamp_float(received)
    if (exp != rec):
        stack = traceback.extract_stack()
        frame = stack[-2]
        print "Expected " + `exp` + " but instead got " + `rec`
        if (frame[3] is None):
            suffix = ""
        else:
            suffix = ": "+frame[3]
        print "Line "+`frame[1]`+" of "+ frame[0] + suffix
        print "Quitting with Error"
        quit()


def isfloat(s):
    """Returns: True if s is the string representation of a number"""
    try:
        x = float(s)
        return True
    except:
        return False

def clamp_float(a):
    """Returns: The float a, rounded to its most signifcant digits.
    
    Floats have roughtly 15 significant digits (which may be before
    or after the decimal point).  This function rounds the float at
    the position of the last significant digit."""
    DIGITS = 15 # double precision
    if (a > 0):
        before = int(math.floor(math.log(a,10))+1)
    elif (a < 0):
        before = int(math.floor(math.log(-a,10))+1)
    else:
        return 0
    sig = DIGITS-before
    return round(a,sig)
