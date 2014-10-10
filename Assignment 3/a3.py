# a3.py
# Quinn Beightol (qeb2)
# 10/11/2012
""" Functions for Assignment A3"""
import colormodel
import math

def complement_rgb(rgb):
    """Returns: the complement of color rgb.
    
    Precondition: rgb is an RGB object"""
    assert (type(rgb) == colormodel.RGB), 'Value '+ `rgb`+' is not a RGB object'
    return colormodel.RGB(255 - rgb.red, 255 - rgb.green, 255 - rgb.blue)


def truncate5(value):
    """Returns: value, as a string, using exactly 5 characters.

    The truncated value will have one of the forms:
        ddd.d        Example:  360.1
        dd.dd        Example:  29.53
        d.ddd        Examples: 4.003,  0.001,  and 0.000
    
    Precondition: value is a number (int or float), 0 <= value <= 999."""

    assert (type(value) == int or type(value) == float), ('Value '+ `value`+
                                                          ' is not a number')
    assert (0 <= value  and value <= 999), ('Value '+ `value`+
                                            ' is outside of the range 0..999')
    
    # To get the desired output, do the following
    #    1. Make sure value is a float.  If it is not, convert it to one.
    #    1. If value < 0.001, set value to 0.
    #        This prevents value appearing in scientific notation, e.g. 1.5E-6.
    #    2. Convert value to a string s, in the usual way. Note that s is guaranteed to
    #        have at least three chars: a decimal point and a digit on either side of it.
    #        Therefore, the simplest thing to do as s is being constructed is to make
    #        sure s has at least 5 chars by appending "00" after the decimal point.
    #    3. Return the first five characters of s.
    
    if type(value) <> float:
        value = float(value)
    
    if value < .001:
        value = 0.
    
    s = `value` + '00' 
    
    return s[:5]


def round5(value):
    """ Returns: value, but expand or round to be (if necessary) exactly 5 characters.
    
    Examples:
        Round 1.3546  to  1.355.
        Round 1.3544  to  1.354.
        Round 21.9954 to  22.00.
        Round 21.994  to  21.99.
        Round 130.59  to  130.6.
        Round 130.54  to  130.5.
        Round 1         to  1.000.
    
    Precondition: value is a number (int or float), 0 <= value <= 360."""
    assert (type(value) == int or type(value) == float), ('Value '+ `value`+
                                                          ' is not a number')
    assert (0 <= value  and value <= 360), ('Value '+ `value`+
                                            ' is outside of the range 0..360.')

    # Note. You want to round and then call truncate5. DO NOT convert value
    # to a string and then back to a float in order to call truncate5.
    # Points will be deducted for this.
    #
    # MAKE SURE THAT VALUE IS A FLOAT BEFORE USING THE BUILT-IN round() FUNCTION
    # If it is not a float convert it to one with the float() function.
    #
    # Obviously, you want to use the built-in function round().  However, 
    # remember that the rounding takes place at a different place depending on
    # how big value is. Look at the examples in the specification.
    
    # ASSERT PRECONDITIONS
    
    if type(value) <> float:
        value = float(value)
    
    if value < 10:
        value = round(value,3)
    elif value < 100:
        value = round(value,2)
    else:
        value = round(value,1)
    
    return truncate5(value)


def rgb_to_string(rgb):
    """Returns: String representation of rgb in the form "(R, G, B)".
    
    Precondition: rgb is an RGB object"""
    
    assert (type(rgb) == colormodel.RGB), ('Value '+ `rgb`+
                                           ' is not an RGB object')
    
    return '(' + `rgb.red` +', ' + `rgb.green` + ', ' + `rgb.blue` + ')'


def cmyk_to_string(cmyk):
    """Returns: String representation of cmyk in the form "(C, M, Y, K)".
    
    In the output, each of C, M, Y, and K should be exactly 5 characters long.
    
    Precondition: cmyk is an CMYK object."""
    
    assert (type(cmyk) == colormodel.CMYK), ('Value '+ `cmyk`+
                                             ' is not a CMYK object')
    
    return ('(' + round5(cmyk.cyan) + ', ' + round5(cmyk.magenta) + ', ' +
            round5(cmyk.yellow) + ', ' + round5(cmyk.black) +')')


def hsv_to_string(hsv):
    """Returns: String representation of hsv in the form "(H, S, V)".
    
    In the output, each of H, S, and V should be exactly 5 characters long.

    Precondition: hsv is an HSV object."""
    
    assert (type(hsv) == colormodel.HSV), ('Value '+ `hsv`+
                                           ' is not an HSV object')
    
    return ('(' + round5(hsv.hue) +', ' + round5(hsv.saturation) + ', ' +
            round5(hsv.value) + ')')


def rgb_to_cmyk(rgb):
    """Returns: color rgb in space CMYK, with the most black possible.

    Formulae from en.wikipedia.org/wiki/CMYK_color_model.

    Precondition: rgb is an RGB object"""
    
    assert (type(rgb) == colormodel.RGB), ('Value '+ `rgb`+
                                           ' is not an RGB object')
    
    R = rgb.red / 255.0
    G = rgb.green /255.0
    B = rgb.blue / 255.0
    
    C = 1 - R
    M = 1 - G
    Y = 1 - B
    
    if C == 1 and M == 1 and Y == 1:
        C = 0
        Y = 0
        M = 0
        K = 1
    else:
        K = min(C, M, Y)
        C = (C - K) / (1 - K)
        M = (M - K) / (1 - K)
        Y = (Y - K) / (1 - K)
    
    C = C * 100.0
    M = M * 100.0
    Y = Y * 100.0
    K = K * 100.0
    return colormodel.CMYK(C, M, Y, K)


def cmyk_to_rgb(cmyk):
    """Returns : color CMYK in space RGB.

    Formulae from en.wikipedia.org/wiki/CMYK_color_model.
    
    Precondition: cmyk is an CMYK object."""
    
    assert (type(cmyk) == colormodel.CMYK), ('Value '+ `cmyk`+
                                             ' is not an RGB object')
    
    C = cmyk.cyan / 100.0
    M = cmyk.magenta / 100.0
    Y = cmyk.yellow / 100.0
    K = cmyk.black / 100.0
    
    R = (1 - C) * (1 - K)
    G = (1 - M) * (1 - K)
    B = (1 - Y) * (1 - K)
    
    return colormodel.RGB(int(round(255 * R)), int(round(255 * G)),
                          int(round(255 * B)))


def rgb_to_hsv(rgb):
    """Return: color rgb in HSV color space.

    Formulae from wikipedia.org/wiki/HSV_color_space.
    
    Precondition: rgb is an RGB object"""

    assert (type(rgb) == colormodel.RGB), ('Value '+ `rgb`+
                                           ' is not an RGB object')
    
    R = rgb.red/255.0
    G = rgb.green/255.0
    B = rgb.blue/255.0
    
    colors = [R, G, B]
    colors.sort()
    MIN = colors[0]
    MAX = colors[2]
    
    if MAX == MIN:
        H = 0
    elif MAX == R:
        if G >= B:
            H = 60.0 * (G - B) / (MAX - MIN)
        else:
            H = 60.0 * (G - B) / (MAX - MIN) + 360.0
    elif MAX == G:
        H = 60.0 * (B - R) / (MAX - MIN) + 120.0
    else:
        H = 60.0 * (R - G) / (MAX - MIN) + 240.0
    
    if MAX == 0:
        S = 0
    else:
        S = 1 - MIN / MAX
    
    return colormodel.HSV(H, S, MAX)


def hsv_to_rgb(hsv):
    """Returns: color in RGB color space.
    
    Formulae from http://en.wikipedia.org/wiki/HSV_color_space.
    
    Precondition: hsv is an HSV object."""
    
    assert (type(hsv) == colormodel.HSV), ('Value '+ `hsv`+
                                           ' is not an RGB object')
    
    H = hsv.hue
    S = hsv.saturation
    V = hsv.value
    
    
    H_sub_i = math.floor(H / 60)
    f = H / 60 - H_sub_i
    p = V * (1 - S)
    q = V * (1 - f * S)
    t = V * (1 - (1 - f) * S) 
    
    if H_sub_i == 0:
        R = V
        G = t
        B = p
    elif H_sub_i == 1:
        R = q
        G = V
        B = p
    elif H_sub_i == 2:
        R = p
        G = V
        B = t
    elif H_sub_i == 3:
        R = p
        G = q
        B = V
    elif H_sub_i == 4:
        R = t
        G = p
        B = V
    else:
        R = V
        G = p
        B = q
    
    return colormodel.RGB(int(round(255 * R)), int(round(255 * G)),
                          int(round(255 * B)))

