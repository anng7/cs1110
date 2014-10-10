# a3_app.py
# Walker M. White (wmw2)
# September 2, 2012
"""Main module for color model application

This module is an example of a Kivy application. It must be in the same
folder as colormodel.kv.  You must not change the name of that file"""
import kivy
from kivy.app           import App
from kivy.lang          import Builder
from kivy.uix.widget    import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties    import NumericProperty, ReferenceListProperty, ListProperty, ObjectProperty
from kivy.vector        import Vector
from kivy.factory       import Factory
from kivy.graphics      import Color
from kivy.graphics      import Ellipse
from kivy.config        import Config

import colormodel
import a3

class Separator(Widget):
    """Instances are used to space out widgets from one another"""
    pass


class ColorPanel(BoxLayout):
    """Instances display a color and its complement"""
    foreground = ListProperty([1,0,0,1])
    background = ListProperty([0,1,1,1])
    text  = ObjectProperty("")


class ColorSlider(BoxLayout):
    """Instances implement a slider widget"""
    color = ListProperty([1,1,1,1])
    slider = ObjectProperty(None)
    text  = ObjectProperty("")
    group_id  = ObjectProperty("")
    max_value = NumericProperty(1000)
    min_value = NumericProperty(0)
    initial = NumericProperty(10)
    
    @property
    def value(self):
        """Delegate to slider value."""
        return self.slider.value
    
    @value.setter
    def value(self, value):
        self.slider.value = value
    
    @value.deleter
    def value(self):
        del self.slider.value    
    
    def bind(self,**kw):
        """Bind to slider state; pass others to super"""
        if (kw.has_key("slide")):
            self.slider.bind(value=kw["slide"])
            del kw["slide"]
        super(ColorSlider,self).bind(**kw) 


class TopPanel(BoxLayout):
    """Instances implement the top panel (sliders and color panels)"""
    main = ObjectProperty(None)
    comp = ObjectProperty(None)
    rSlider = ObjectProperty(None)
    gSlider = ObjectProperty(None)
    bSlider = ObjectProperty(None)
    cSlider = ObjectProperty(None)
    mSlider = ObjectProperty(None)
    ySlider = ObjectProperty(None)
    kSlider = ObjectProperty(None)
    hSlider = ObjectProperty(None)
    sSlider = ObjectProperty(None)
    vSlider = ObjectProperty(None)
    
    def update(self, rgb, cmyk, hsv):
        """Refresh the color and text display in the color panels"""
        compRGB = a3.complement_rgb(rgb)
        if (compRGB is None):
            compRGB = rgb
        
        rgb_str = str(rgb)
        cmyk_str = '' if cmyk is None else str(cmyk) 
        hsv_str = '' if hsv is None else str(hsv)
        
        self.main.text = ("Color\nRGB:    " + rgb_str +
                          "\nCMYK: " + cmyk_str +
                          "\nHSV:    " + hsv_str + "\n \n" +
                          "R,G,B sliders in: 0..255\n" +
                          "C,M,Y,K sliders: 0 to 100%\n" +
                          "H slider: 0 <= H < 360 degrees\n" +
                          "S,V sliders: 0 <= S,V <= 1")
        self.main.background = rgb.glColor()
        self.main.foreground = compRGB.glColor()
        self.comp.text = ("Color\nRGB:    " + rgb_str +
                          "\nCMYK: " + cmyk_str +
                          "\nHSV:    " + hsv_str + "\n \n" +
                          "R,G,B sliders in: 0..255\n" +
                          "C,M,Y,K sliders: 0 to 100%\n" +
                          "H slider: 0 <= H < 360 degrees\n" +
                          "S,V sliders: 0 <= S,V <= 1" )
        self.comp.background = compRGB.glColor()
        self.comp.foreground = rgb.glColor()
        
        # set the sliders
        self.rSlider.value = rgb.red*100
        self.gSlider.value = rgb.green*100
        self.bSlider.value = rgb.blue*100
        self.cSlider.value = 0 if cmyk is None else cmyk.cyan*100 
        self.mSlider.value = 0 if cmyk is None else cmyk.magenta*100
        self.ySlider.value = 0 if cmyk is None else cmyk.yellow*100
        self.kSlider.value = 0 if cmyk is None else cmyk.black*100
        self.hSlider.value = 0 if hsv is None else hsv.hue*100
        self.sSlider.value = 0 if hsv is None else hsv.saturation*100
        self.vSlider.value = 0 if hsv is None else hsv.value*100


class BotPanel(BoxLayout):
    """Instances implement the top panel (text boxes and buttons)"""
    rgbButton  = ObjectProperty(None)
    cmykButton = ObjectProperty(None)
    hsvButton  = ObjectProperty(None)
    rField = ObjectProperty(None)
    gField = ObjectProperty(None)
    bField = ObjectProperty(None)
    cField = ObjectProperty(None)
    mField = ObjectProperty(None)
    yField = ObjectProperty(None)
    kField = ObjectProperty(None)
    hField = ObjectProperty(None)
    sField = ObjectProperty(None)
    vField = ObjectProperty(None)
    
    def _toInt(self,s):
        """Returns: if s is not an int, 0 else max(0, min(255, s)."""
        try:
            i = int(s)
            return i
        except ValueError:
             return 0
    
    def _toFloat(self,s):
        """Returns: if s is not a float, 0 else max(0.0, min(1.0, s)."""
        try:
            d = float(s)
            return max(0.0,min(1.0,d))
        except ValueError:
            return 0.0
      
    def _toFloat100(self,s):
        """Returns: if s is not a float, 0.0 else max(0.0, min(100.0, s)."""
        try:
            d = float(s)
            return max(0.0, min(100.0, d));
        except ValueError:
            return 0.0
      
    def _toFloat360(self,s):
        """Returns: if s is not a float, 0 else max(0.0, min(359.9, s)."""
        try:
            d = float(s)
            return max(0.0, min(359.9, d));
        except ValueError:
            return 0.0
        
    def clear(self):
        self.rField.text = ""
        self.gField.text = ""
        self.bField.text = ""
        self.cField.text = ""
        self.mField.text = ""
        self.yField.text = ""
        self.kField.text = ""


class ColorWidget(BoxLayout):
    """Instances represent the top level widget"""
    active = True
    rgb = colormodel.RGB(0, 255, 0)
    cmyk = None
    hsv = None
    
    top = ObjectProperty(None)
    bot = ObjectProperty(None)
        
    def register(self):
        """Initialize color values and force refresh"""
        self.rgb = colormodel.RGB(0, 255, 0)
        self.cmyk = a3.rgb_to_cmyk(self.rgb)
        assert (self.cmyk == None or type(self.cmyk) == colormodel.CMYK), 'rgb_to_cmyk does not return a CMYK object'
        self.hsv = a3.rgb_to_hsv(self.rgb)
        assert (self.hsv == None or type(self.hsv) == colormodel.HSV), 'rgb_to_hsv does not return a HSV object'
        self.update()
    
    def update(self):
        """Force refresh of top panel on update"""
        self.active = False
        self.top.update(self.rgb,self.cmyk,self.hsv)
        self.active = True

    def on_rgb_press(self,r,g,b):
        """Call back to rgb button"""
        self.bot.clear()
        self.rgb = colormodel.RGB(r, g, b)
        self.hsv = a3.rgb_to_hsv(self.rgb)
        assert (self.hsv == None or type(self.hsv) == colormodel.HSV), 'rgb_to_hsv does not return a HSV object'
        self.cmyk = a3.rgb_to_cmyk(self.rgb)
        assert (self.cmyk == None or type(self.cmyk) == colormodel.CMYK), 'rgb_to_cmyk does not return a CMYK object'
        self.update()
    
    def on_rgb_slide(self,r,g,b):
        """Call back to rgb sliders"""
        if not self.active:
            return
        red = int(round(r / 100.0))
        green = int(round(g / 100.0))
        blue = int(round(b / 100.0))
        self.rgb = colormodel.RGB(red, green, blue)
        self.hsv = a3.rgb_to_hsv(self.rgb)
        assert (self.hsv == None or type(self.hsv) == colormodel.HSV), 'rgb_to_hsv does not return a HSV object'
        self.cmyk = a3.rgb_to_cmyk(self.rgb)
        assert (self.cmyk == None or type(self.cmyk) == colormodel.CMYK), 'rgb_to_cmyk does not return a CMYK object'
        self.update()
    
    def on_cmyk_press(self,c,m,y,k):
        """Call back to cmyk button"""
        self.bot.clear()
        self.cmyk = colormodel.CMYK(c, m, y, k)
        temp = a3.cmyk_to_rgb(self.cmyk)
        assert (temp == None or type(temp) == colormodel.RGB), 'cmyk_to_rgb does not return a RGB object'
        self.rgb = self.rgb if temp is None else temp
        self.hsv = a3.rgb_to_hsv(self.rgb)
        assert (self.hsv == None or type(self.hsv) == colormodel.HSV), 'rgb_to_hsv does not return a HSV object'
        self.update()
    
    def on_cmyk_slide(self,c,m,y,k):
        """Call back to cmyk sliders"""
        if not self.active:
            return
        cyan = c / 100.0
        magenta = m / 100.0
        yellow = y / 100.0
        black = k / 100.0
        self.cmyk = colormodel.CMYK(cyan, magenta, yellow, black)
        temp = a3.cmyk_to_rgb(self.cmyk)
        assert (temp == None or type(temp) == colormodel.RGB), 'cmyk_to_rgb does not return a RGB object'
        self.rgb = self.rgb if temp is None else temp
        self.hsv = a3.rgb_to_hsv(self.rgb)
        assert (self.hsv == None or type(self.hsv) == colormodel.HSV), 'rgb_to_hsv does not return a HSV object'
        self.update()
    
    def on_hsv_press(self,h,s,v):
        """Call back to hsv button"""
        self.bot.clear()
        self.hsv = colormodel.HSV(h, s, v)
        temp = a3.hsv_to_rgb(self.hsv)
        assert (temp == None or type(temp) == colormodel.RGB), 'hsv_to_rgb does not return a RGB object'
        self.rgb = self.rgb if temp is None else temp
        self.cmyk = a3.rgb_to_cmyk(self.rgb);
        assert (self.cmyk == None or type(self.cmyk) == colormodel.CMYK), 'rgb_to_cmyk does not return a CMYK object'
        self.update()
        
    def on_hsv_slide(self,h,s,v):
        """Call back to hsv sliders"""
        if not self.active:
            return
        hue = h / 100.0
        sat = s / 100.0
        val = v / 100.0
        self.hsv = colormodel.HSV(hue, sat, val)
        temp = a3.hsv_to_rgb(self.hsv)
        assert (temp == None or type(temp) == colormodel.RGB), 'hsv_to_rgb does not return a RGB object'
        self.rgb = self.rgb if temp is None else temp
        self.cmyk = a3.rgb_to_cmyk(self.rgb);
        assert (self.cmyk == None or type(self.cmyk) == colormodel.CMYK), 'rgb_to_cmyk does not return a CMYK object'
        self.update()


class ColorModelApp(App):
    """Instances represnet the color model application"""
    def build(self):
        """Read kivy file and perform layout"""
        Config.set('graphics', 'width', '1150')
        Config.set('graphics', 'height', '300')
        return ColorWidget()
    
    def on_start(self):
        """Start up the app and initialize values"""
        super(ColorModelApp,self).on_start()
        self.root.register()


Factory.register("Separator", Separator)
Factory.register("ColorPanel", ColorPanel)
Factory.register("ColorSlider", ColorSlider)
Factory.register("TopPanel", TopPanel)
Factory.register("BotPanel", BotPanel)

# Application Code
if __name__ in ('__android__', '__main__'):
    ColorModelApp().run()