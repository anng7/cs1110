# a3test.py
# Quinn Beightol (qeb2)
# 10/11/2012
""" Unit Test for Assignment A3"""
import colormodel
import cunittest
import a3

def test_complement():
    """Test function complement"""
    cunittest.assert_equals(colormodel.RGB(255-250, 255-0, 255-71), a3.complement_rgb(colormodel.RGB(250, 0, 71)))


def test_truncate5():
    """Test function truncate5"""
    cunittest.assert_equals("130.5",  a3.truncate5(130.59))
    cunittest.assert_equals("130.5",  a3.truncate5(130.54))
    cunittest.assert_equals("100.0",  a3.truncate5(100))
    cunittest.assert_equals("99.56",  a3.truncate5(99.566))
    cunittest.assert_equals("99.99",  a3.truncate5(99.99))
    cunittest.assert_equals("99.99",  a3.truncate5(99.995))
    cunittest.assert_equals("21.99",  a3.truncate5(21.99575))
    cunittest.assert_equals("21.99",  a3.truncate5(21.994))
    cunittest.assert_equals("10.01",  a3.truncate5(10.013567))
    cunittest.assert_equals("10.00",  a3.truncate5(10.000000005))
    cunittest.assert_equals("9.999",  a3.truncate5(9.9999))
    cunittest.assert_equals("9.999",  a3.truncate5(9.9993))
    cunittest.assert_equals("1.354",  a3.truncate5(1.3546))
    cunittest.assert_equals("1.354",  a3.truncate5(1.3544))
    cunittest.assert_equals("0.045",  a3.truncate5(.0456))
    cunittest.assert_equals("0.045",  a3.truncate5(.0453))
    cunittest.assert_equals("0.005",  a3.truncate5(.0056))
    cunittest.assert_equals("0.001",  a3.truncate5(.0013))
    cunittest.assert_equals("0.000",  a3.truncate5(.0004))
    cunittest.assert_equals("0.000",  a3.truncate5(.0009999))


def test_round5():
    """Test function round5"""
    cunittest.assert_equals("130.6",  a3.round5(130.59))
    cunittest.assert_equals("130.5",  a3.round5(130.54))
    cunittest.assert_equals("100.0",  a3.round5(100))
    cunittest.assert_equals("99.57",  a3.round5(99.566))
    cunittest.assert_equals("99.99",  a3.round5(99.99))
    cunittest.assert_equals("100.0",  a3.round5(99.9951))
    cunittest.assert_equals("22.00",  a3.round5(21.99575))
    cunittest.assert_equals("21.99",  a3.round5(21.994))
    cunittest.assert_equals("10.01",  a3.round5(10.013567))
    cunittest.assert_equals("10.00",  a3.round5(10.000000005))
    cunittest.assert_equals("10.00",  a3.round5(9.9999))
    cunittest.assert_equals("9.999",  a3.round5(9.9993))
    cunittest.assert_equals("1.355",  a3.round5(1.3546))
    cunittest.assert_equals("1.354",  a3.round5(1.3544))
    cunittest.assert_equals("0.046",  a3.round5(.0456))
    cunittest.assert_equals("0.045",  a3.round5(.0453))
    cunittest.assert_equals("0.006",  a3.round5(.0056))
    cunittest.assert_equals("0.001",  a3.round5(.0013))
    cunittest.assert_equals("0.000",  a3.round5(.0004))
    cunittest.assert_equals("0.001",  a3.round5(.0009999))


def test_to_strings():
    """Test toString methods"""
    #Test rgb_to_string:()
    cunittest.assert_equals("(30, 240, 230)",
                            a3.rgb_to_string(colormodel.RGB(30, 240, 230)));
    
    #Test cmyk_to_string()
    cunittest.assert_equals("(10.00, 11.00, 20.00, 12.00)",
                            a3.cmyk_to_string(colormodel.CMYK(10, 11, 20, 12)));
    #Test that cmyk_to_string() uses round5(), not `truncate5()`:
    cunittest.assert_equals("(10.01, 11.00, 20.01, 12.00)",
                            a3.cmyk_to_string(colormodel.CMYK(10.005, 11.0045,
                                                              20.009, 12.001)));

    #Test hsv_to_string()
    cunittest.assert_equals("(100.0, 1.000, 1.000)",
                            a3.hsv_to_string(colormodel.HSV(100, 1, 1)));
    #Test that hsv_to_string uses round5(), not `truncate5()`:
    cunittest.assert_equals("(100.0, 0.500, 0.499)",
                            a3.hsv_to_string(colormodel.HSV(99.999, .4996, .4994)));


def test_rgb_to_cmyk():
    """Test rgb_to_cmyk"""
    #Test rgb_to_cmyk() when C = M = Y = 0:
    rgb = colormodel.RGB(255, 255, 255);
    cmyk = a3.rgb_to_cmyk(rgb);
    cunittest.assert_equals("0.000", a3.round5(cmyk.cyan))
    cunittest.assert_equals("0.000", a3.round5(cmyk.magenta))
    cunittest.assert_equals("0.000", a3.round5(cmyk.yellow))
    cunittest.assert_equals("0.000", a3.round5(cmyk.black))
    
    #Test rgb_to_cmyk() when C' = M' = Y' = 1:
    rgb = colormodel.RGB(0, 0, 0);
    cmyk = a3.rgb_to_cmyk(rgb);
    cunittest.assert_equals("0.000", a3.round5(cmyk.cyan))
    cunittest.assert_equals("0.000", a3.round5(cmyk.magenta))
    cunittest.assert_equals("0.000", a3.round5(cmyk.yellow))
    cunittest.assert_equals("100.0", a3.round5(cmyk.black))
    
    #Test rgb_to_cmyk() when C' = K (=> C = 0):
    rgb = colormodel.RGB(217, 43, 164);
    cmyk = a3.rgb_to_cmyk(rgb);
    cunittest.assert_equals("0.000", a3.round5(cmyk.cyan))
    cunittest.assert_equals("80.18", a3.round5(cmyk.magenta))
    cunittest.assert_equals("24.42", a3.round5(cmyk.yellow))
    cunittest.assert_equals("14.90", a3.round5(cmyk.black))
    
    #Test rgb_to_cmyk() when M' = K (=> M = 0):
    rgb = colormodel.RGB(1, 100, 1);
    cmyk = a3.rgb_to_cmyk(rgb);
    cunittest.assert_equals("99.00", a3.round5(cmyk.cyan))
    cunittest.assert_equals("0.000", a3.round5(cmyk.magenta))
    cunittest.assert_equals("99.00", a3.round5(cmyk.yellow))
    cunittest.assert_equals("60.78", a3.round5(cmyk.black))
    
    #Test rgb_to_cmyk() when Y' = K (=> Y = 0):
    rgb = colormodel.RGB(101, 40, 141);
    cmyk = a3.rgb_to_cmyk(rgb);
    cunittest.assert_equals("28.37", a3.round5(cmyk.cyan))
    cunittest.assert_equals("71.63", a3.round5(cmyk.magenta))
    cunittest.assert_equals("0.000", a3.round5(cmyk.yellow))
    cunittest.assert_equals("44.71", a3.round5(cmyk.black))


def test_cmyk_to_rgb():
    """Test translation function cmyk_to_rgb"""
    #Test cmyk_to_rgb() when K = 1:
    cmyk = colormodel.CMYK(10, 11, 12, 100)
    rgb = a3.cmyk_to_rgb(cmyk)
    cunittest.assert_equals(0, rgb.red)
    cunittest.assert_equals(0, rgb.green)
    cunittest.assert_equals(0, rgb.blue)
    
    #Test cmyk_to_rgb() when C, M, or Y = 0:
    cmyk = colormodel.CMYK(0, 11, 12, 0)
    rgb = a3.cmyk_to_rgb(cmyk)
    cunittest.assert_equals(255, rgb.red)
    cunittest.assert_equals(227, rgb.green)
    cunittest.assert_equals(224, rgb.blue)
    
    cmyk = colormodel.CMYK(10, 0, 12, 0)
    rgb = a3.cmyk_to_rgb(cmyk)
    cunittest.assert_equals(230, rgb.red)
    cunittest.assert_equals(255, rgb.green)
    cunittest.assert_equals(224, rgb.blue)
    
    cmyk = colormodel.CMYK(10, 11, 0, 0)
    rgb = a3.cmyk_to_rgb(cmyk)
    cunittest.assert_equals(230, rgb.red)
    cunittest.assert_equals(227, rgb.green)
    cunittest.assert_equals(255, rgb.blue)
    
    #General Test Case
    cmyk = colormodel.CMYK(4, 20, 7, 18.63)
    rgb = a3.cmyk_to_rgb(cmyk)
    cunittest.assert_equals(199, rgb.red)
    cunittest.assert_equals(166, rgb.green)
    cunittest.assert_equals(193, rgb.blue)
    

def test_rgb_to_hsv():
    """Test translation function rgb_to_hsv"""
    #Test rgb_to_hsv when MAX = MIN and MAX = 0:
    rgb = colormodel.RGB(0, 0, 0)
    hsv = a3.rgb_to_hsv(rgb)
    cunittest.assert_equals("0.000", a3.round5(hsv.hue))
    cunittest.assert_equals("0.000", a3.round5(hsv.saturation))
    cunittest.assert_equals("0.000", a3.round5(hsv.value))
    
    #Test rgb_to_hsv when MAX = MIN and MAX <> 0:
    rgb = colormodel.RGB(100, 100, 100)
    hsv = a3.rgb_to_hsv(rgb)
    cunittest.assert_equals("0.000", a3.round5(hsv.hue))
    cunittest.assert_equals("0.000", a3.round5(hsv.saturation))
    cunittest.assert_equals("0.392", a3.round5(hsv.value))
    
    #Test rgb_to_hsv when MAX = R and G >=B:
    rgb = colormodel.RGB(161, 42, 42)
    hsv = a3.rgb_to_hsv(rgb)
    cunittest.assert_equals("0.000", a3.round5(hsv.hue))
    cunittest.assert_equals("0.739", a3.round5(hsv.saturation))
    cunittest.assert_equals("0.631", a3.round5(hsv.value))
    
    rgb = colormodel.RGB(161, 72, 42)
    hsv = a3.rgb_to_hsv(rgb)
    cunittest.assert_equals("15.13", a3.round5(hsv.hue))
    cunittest.assert_equals("0.739", a3.round5(hsv.saturation))
    cunittest.assert_equals("0.631", a3.round5(hsv.value))
    
    #Test rgb_to_hsv when MAX = R and G < B:
    rgb = colormodel.RGB(161, 42, 72)
    hsv = a3.rgb_to_hsv(rgb)
    cunittest.assert_equals("344.9", a3.round5(hsv.hue))
    cunittest.assert_equals("0.739", a3.round5(hsv.saturation))
    cunittest.assert_equals("0.631", a3.round5(hsv.value))
    
    #Test rgb_to_hsv when MAX = G:
    rgb = colormodel.RGB(17, 101, 19)
    hsv = a3.rgb_to_hsv(rgb)
    cunittest.assert_equals("121.4", a3.round5(hsv.hue))
    cunittest.assert_equals("0.832", a3.round5(hsv.saturation))
    cunittest.assert_equals("0.396", a3.round5(hsv.value))
    
    #Test rgb_to_hsv when MAX = B:
    rgb = colormodel.RGB(21, 100, 255)
    hsv = a3.rgb_to_hsv(rgb)
    cunittest.assert_equals("219.7", a3.round5(hsv.hue))
    cunittest.assert_equals("0.918", a3.round5(hsv.saturation))
    cunittest.assert_equals("1.000", a3.round5(hsv.value))


def test_hsv_to_rgb():
    """Test translation function hsv_to_rgb"""
    #Test hsv_to_rgb() when H is in the interval [0,60):
    hsv = colormodel.HSV(42, .6, .7)
    rgb = a3.hsv_to_rgb(hsv)
    cunittest.assert_equals(179, rgb.red)
    cunittest.assert_equals(146, rgb.green)
    cunittest.assert_equals(71, rgb.blue)
    
    #Test hsv_to_rgb() when H is in the interval [60,120):
    hsv = colormodel.HSV(94, .5, .5)
    rgb = a3.hsv_to_rgb(hsv)
    cunittest.assert_equals(91, rgb.red)
    cunittest.assert_equals(128, rgb.green)
    cunittest.assert_equals(64, rgb.blue)
    
    #Test hsv_to_rgb() when H is in the interval [120,180):
    #Also tests that hsv_to_rgb() properly handles values at the borders of
    #each interval of H
    hsv = colormodel.HSV(120, .5, .5)
    rgb = a3.hsv_to_rgb(hsv)
    cunittest.assert_equals(64, rgb.red)
    cunittest.assert_equals(128, rgb.green)
    cunittest.assert_equals(64, rgb.blue)
    
    #Test hsv_to_rgb() when H is in the interval [180,240):
    hsv = colormodel.HSV(216, .6, .3)
    rgb = a3.hsv_to_rgb(hsv)
    cunittest.assert_equals(31, rgb.red)
    cunittest.assert_equals(49, rgb.green)
    cunittest.assert_equals(77, rgb.blue)
    
    #Test hsv_to_rgb() when H is in the interval [240,300):
    hsv = colormodel.HSV(256, .2, .8)
    rgb = a3.hsv_to_rgb(hsv)
    cunittest.assert_equals(174, rgb.red)
    cunittest.assert_equals(163, rgb.green)
    cunittest.assert_equals(204, rgb.blue)
    
    #Test hsv_to_rgb() when H is in the interval [300,360):
    hsv = colormodel.HSV(343, .7, .3)
    rgb = a3.hsv_to_rgb(hsv)
    cunittest.assert_equals(77, rgb.red)
    cunittest.assert_equals(23, rgb.green)
    cunittest.assert_equals(38, rgb.blue)


# Application Code
if __name__ == "__main__":
    test_complement()
    test_truncate5()
    test_round5()
    test_to_strings()
    test_rgb_to_cmyk()
    test_cmyk_to_rgb()
    test_rgb_to_hsv()
    test_hsv_to_rgb()
    print "Module a3 is working correctly"
