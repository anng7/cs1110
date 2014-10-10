# panels.py
# Walker M. White (wmw2)
# October 13, 2012
"""Special purpose panels for defining transforms.

This code has been factored out of a5app for purposes of readability."""
import kivy
from kivy.uix.label import Label
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.factory import Factory

import geometry
import math

# Import Kivy language file with layout information
from kivy.lang import Builder 
Builder.load_file('a5lib/panels.kv') 


class CCheckBox(CheckBox):
    """Instances are appropriately colored checkboxes"""
    pass


class IdentityPanel(BoxLayout):
    """Instances are panels for defining an Identity transform.
    
    There are no parameters to define."""
    pass


class TranslatePanel(BoxLayout):
    """Instances are panels for defining an Translation transform.
    
        dx is a Kivy property for the TextInput with the x offset
        
        dy is a Kivy property for the TextInput with the y offset
    
    When either dx or dy change, Kivy invokes the method update. This
    method updates the transform property in the observer field."""
    dx = ObjectProperty(None)
    dy = ObjectProperty(None)
    observer = None
    
    def __init__(self,observer,**kw):
        """Constructor: Makes a TranslatePanel with the given observer.
        
        Precondition: observer has an attribute called transform that
        stores a Transform object.  **kw is a list of keyword arguments
        for BoxLayout."""
        super(TranslatePanel,self).__init__(**kw)
        self.observer = observer

    def update(self):
        """Creates a translation transform and stores it in the observer.
        
        Called when either dx or dy is updated."""
        text_dx = self.dx.text
        text_dy = self.dy.text
        try:
            dx = round(float(text_dx),3)
        except:
            dx = 0.0
        self.dx.text = str(dx)

        try:
            dy = round(float(text_dy),3)            
        except:
            dy = 0.0
        self.dy.text = str(dy)
        
        self.observer.transform = geometry.Transform.Translation(dx,dy)


class ScalePanel(BoxLayout):
    """Instances are panels for defining an Scaling transform.
    
        sx is a Kivy property for the TextInput with the x magnification
        
        sy is a Kivy property for the TextInput with the y magnification
    
    When either sx or sy change, Kivy invokes the method update. This
    method updates the transform property in the observer field."""
    sx = ObjectProperty(None)
    sy = ObjectProperty(None)
    observer = None
    
    def __init__(self,observer,**kw):
        """Constructor: Makes a ScalePanel with the given observer.
        
        Precondition: observer has an attribute called transform that
        stores a Transform object.  **kw is a list of keyword arguments
        for BoxLayout."""
        super(ScalePanel,self).__init__(**kw)
        self.observer = observer
    
    def update(self):
        """Creates a scaling transform and stores it in the observer.
        
        Called when either sx or sy is updated."""
        text_sx = self.sx.text
        text_sy = self.sy.text
        try:
            sx = round(float(text_sx),3)
        except:
            sx = 1.0
        self.sx.text = str(sx)

        try:
            sy = round(float(text_sy),3)            
        except:
            sy = 1.0
        self.sy.text = str(sy)
        
        self.observer.transform = geometry.Transform.Scale(sx,sy)


class RotatePanel(BoxLayout):
    """Instances are panels for defining an Rotation transform.
    
        angle is a Kivy property for the TextInput with the angle
        
        degrees is a Kivy property for a checkbox indicating degrees
    
        radians is a Kivy property for a checkbox indicating degrees

    When angle, degrees, or radians change, Kivy invokes the method update.
    This method updates the transform property in the observer field."""
    angle = ObjectProperty(None)
    degrees = ObjectProperty(None)
    radians = ObjectProperty(None)
    observer = None
    
    def __init__(self,observer,**kw):
        """Constructor: Makes a RotatePanel with the given observer.
        
        Precondition: observer has an attribute called transform that
        stores a Transform object.  **kw is a list of keyword arguments
        for BoxLayout."""
        super(RotatePanel,self).__init__(**kw)
        self.observer = observer

    def update(self,button):
        """Creates a rotation transform and stores it in the observer.
        
        Called when angle, degrees, or radians is updated.
        
        The argument button is a bool indicating whether the change
        was just with the TextInput (False) or in one of the
        checkboxes (True)."""
        text = self.angle.text
        try:
            angle = float(text)
        except:
            self.angle.text = '0.0'
            angle = 0.0
        
        if self.degrees.active:
            if button:
                angle = round(angle,3)
                self.angle.text = str(round(180.0*angle/math.pi,3))
            else:
                angle = round(math.pi*angle/180.0,6)
        elif self.radians.active:
            if button:
                angle = round(math.pi*angle/180.0,6)
            else:
                angle = round(angle,6)
            self.angle.text = str(angle)
        
        self.observer.transform = geometry.Transform.Rotation(angle)


class ShearPanel(BoxLayout):
    """Instances are panels for defining an Shear transform.
    
        x_axis is a Kivy property for a checkbox indicating a shear in the x-direction
    
        y_axis is a Kivy property for a checkbox indicating a shear in the y-direction

        amount is a Kivy property for the TextInput with the amount

    When x_axis, y_axis, or amount change, Kivy invokes the method update.
    This method updates the transform property in the observer field."""
    x_axis = ObjectProperty(None)
    y_axis = ObjectProperty(None)
    amount = ObjectProperty(None)
    observer = None
    
    def __init__(self,observer,**kw):
        """Constructor: Makes a ShearPanel with the given observer.
        
        Precondition: observer has an attribute called transform that
        stores a Transform object.  **kw is a list of keyword arguments
        for BoxLayout."""
        super(ShearPanel,self).__init__(**kw)
        self.observer = observer

    def update(self):
        """Creates a shear transform and stores it in the observer.
        
        Called when x_axis, y_axis, or amount is updated."""
        text = self.amount.text
        try:
            amount = float(text)
        except:
            amount = 0.0
        self.amount.text = str(amount)

        if self.x_axis.active:
            self.observer.transform = geometry.Transform.ShearX(amount)
        else:
            self.observer.transform = geometry.Transform.ShearY(amount)


class ReflectPanel(BoxLayout):
    """Instances are panels for defining an Reflection transform.
    
        x_axis is a Kivy property for a checkbox indicating a reflection
        about the the x-axis
    
        y_axis is a Kivy property for a checkbox indicating a reflection
        about the the y-axis

    When either x_axis or y_axis change, Kivy invokes the method update.
    This method updates the transform property in the observer field."""
    x_axis = ObjectProperty(None)
    y_axis = ObjectProperty(None)
    observer = None
    
    def __init__(self,observer,**kw):
        """Constructor: Makes a ReflectPanel with the given observer.
        
        Precondition: observer has an attribute called transform that
        stores a Transform object.  **kw is a list of keyword arguments
        for BoxLayout."""
        super(ReflectPanel,self).__init__(**kw)
        self.observer = observer

    def update(self):
        """Creates a reflection transform and stores it in the observer.
        
        Called when either x_axis or y_axis is updated."""
        if not self.x_axis.active and not self.y_axis.active:
            self.observer.transform = geometry.Transform.Identity()
        elif self.x_axis.active and not self.y_axis.active:
            self.observer.transform = geometry.Transform.Reflection(1,0)
        elif not self.x_axis.active and self.y_axis.active:
            self.observer.transform = geometry.Transform.Reflection(0,1)
        else:
            self.observer.transform = geometry.Transform.Rotation(math.pi)


class TransformBubble(Bubble):
    """Instances are a pop-up menu to select a transform.
    
    Something about the lastest Kivy makes this class incompatible
    with .kv files.  The constructor crashes at initialization.
    Therefore, we have to build the layout manually."""
    callback = None # Callback function for Widget that makes this bubble

    def __init__(self,**kw):
        super(TransformBubble,self).__init__(**kw)
        self.size_hint = (0.5, None)
        self.size = (0,200)
        self.pos_hint = {'right':1,'top':1}
        self.arrow_pos = 'left_top'
        self.orientation = 'vertical'
        self.rows = 6
        
        # Create and bind each button.
        button = BubbleButton(text='Identity')
        button.bind(on_press=self.select_option)
        self.add_widget(button)
        
        button = BubbleButton(text='Translate')
        button.bind(on_press=self.select_option)
        self.add_widget(button)
        
        button = BubbleButton(text='Scale')
        button.bind(on_press=self.select_option)
        self.add_widget(button)
        
        button = BubbleButton(text='Rotate')
        button.bind(on_press=self.select_option)
        self.add_widget(button)
        
        button = BubbleButton(text='Shear')
        button.bind(on_press=self.select_option)
        self.add_widget(button)
        
        button = BubbleButton(text='Reflect')
        button.bind(on_press=self.select_option)
        self.add_widget(button)
    
    def select_option(self,value):
        """Callback function when an item is selected from menu.
        
        This is a placeholder; it will be replaced on creation."""
        if value is None or self.callback is None:
            return
        self.callback(value.text)


class TransformPanel(FloatLayout):
    """Instances are a panel to define an arbitrary Transform.
    
        transform is a Kivy property containing the Transform defined by this panel.
        
    This panel contains one of the panels defined above. The exact panel can
    change dynamically depending on the choice via TransformBubble. This Panel
    provides a uniform interface to them all and stores the defined transform."""
    state = False
    bubble = None
    choice = ObjectProperty(None)
    bbzone = ObjectProperty(None)
    content = ObjectProperty(None)
    transform = ObjectProperty(geometry.Transform.Identity())
    
    def select_transform(self,text):
        """Callback function when an item is selected from TransformBubble.
        
        Used in place of select_option."""
        self.choice.text = text
        self.content.clear_widgets()
        panel = None
        if (text == 'Translate'):
            panel = TranslatePanel(self)
        elif (text == 'Scale'):
            panel = ScalePanel(self)
        elif (text == 'Rotate'):
            panel = RotatePanel(self)
        elif (text == 'Shear'):
            panel = ShearPanel(self)
        elif (text == 'Reflect'):
            panel = ReflectPanel(self)
        else:
            panel = IdentityPanel()
        
        panel.pos_hint = {'x':0,'top':1}
        panel.size_hint = (None,None)
        self.content.add_widget(panel)
        
        self.choice.state = 'normal'
        self.bbzone.remove_widget(self.bubble)
        self.transform = geometry.Transform.Identity()
        self.state = False

    def show_bubble(self):
        """Show a TransformBubble to allow a new Transform type.
        
        Sets select_transform as the appropriate callback."""
        if not self.state:
            if self.bubble is None:
                self.bubble = TransformBubble()
                self.bubble.callback = self.select_transform
            self.bbzone.add_widget(self.bubble)
            self.state = True
        else:
            self.choice.state = 'down'

# Register UI elements for .kv files.
Factory.register("TransformPanel", TransformPanel)
Factory.register("IdentityPanel", IdentityPanel)
Factory.register("CCheckBox", CCheckBox)
