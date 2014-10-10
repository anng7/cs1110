# dialogs.py
# Walker M. White (wmw2)
# October 13, 2012
"""Special purpose dialogs popups for our application.

This code has been factored out of a5app for purposes of readability."""
import kivy
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.factory import Factory

import os.path

# Import Kivy language file with layout information
from kivy.lang import Builder 
Builder.load_file('a5lib/dialogs.kv') 


class ErrorDialog(Popup):
    """Instances are an error popup with a confirmation button"""
    def __init__(self,message,**kw):
        """Constructor: Make an error dialog with the given error message
        
        Precondition: message is a string"""
        super(ErrorDialog,self).__init__(title='ERROR',
                                         content=ErrorMessage(self))
        self.content.label = message
        self.open()


class ErrorMessage(BoxLayout):
    """Instances are the internal contents of an ErrorDialog"""
    label  = StringProperty('')    # ErrorMessage
    button = ObjectProperty(None)  # Reference to OK button
    
    def __init__(self,popup,**kw):
        """Constructor: Fill the ErrorDialog with these contents
        
        Precondition: popup is the parent popup window"""
        super(ErrorMessage,self).__init__(**kw)
        self.popup = ObjectProperty(popup)
    
    def acknowledge(self):
        """Acknowledge the error and dismiss the parent popup window"""
        self.popup.dismiss()


class ImageDialog(Popup):
    """Instances are a file chooser popup for images"""
    observer = None
    
    def __init__(self,observer,**kw):
        """Constructor: Make an ImageDialog with the given observer
        
        Precondition: observer is an object with method
        on_file_open, which registers the choice of this dialog"""
        super(ImageDialog,self).__init__(title='Choose an Image',
                                         content=ImageChooser(self))
        self.observer = observer
        self.open()
        
    def do_select(self,selection):
        """Handle the file selection for this chooser
        
        Precondition: selection is a string with the absolute file path"""
        # I live in fear that the Asian students have non ASCII folder names
        # The file chooser will fail on those
        # To mitigated damage, convert to relative path names
        self.dismiss()
        if (len(selection) > 0):
            choice = os.path.relpath(selection[0])
            try:
                choice = choice.encode('ascii')
                self.observer.on_file_open(choice)
            except:
                dialog = ErrorDialog('Non-ASCII characters encountered in path name:\n\n'+choice)
                dialog.size_hint = self.size_hint
                dialog.pos_hint = self.pos_hint


class ImageChooser(BoxLayout):
    """Instances are the internal contents of an ImageDialog"""
    chooser = ObjectProperty(None)        # Reference to FileChooser
    open_button = ObjectProperty(None)    # Reference to Open Button
    cancel_button = ObjectProperty(None)  # Reference to Cancel Button
    
    def __init__(self,popup,**kw):
        """Constructor: Fill the ImageDialog with these contents
        
        Precondition: popup is the parent popup window"""
        super(ImageChooser,self).__init__(**kw)
        self.popup = ObjectProperty(popup)