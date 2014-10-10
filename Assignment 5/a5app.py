# a5app.py
# Walker M. White (wmw2)
# October 13, 2012
"""Primary module for assignment 5.

This module launches a GUI for transforming an image using affine transforms.
In order to work properly,

(a) The directory that this file (a5app.py) is in should also contain
    a5.py         # student-authored file
    transform.kv  # Main application layout
    images (folder containing 'gollum.jpg', 'letter.png' 'walker.png')
    a5lib  (folder containing files listed in (b) below) 


(b) the directory a5lib should contain:

   __init__.py   # Empty file needed for reasons (re: import) you don't need to know
   dialogs.py    # Dialog pop-up behavior
   dialogs.kv    # Dialog pop-up layout
   geometry.py   # Support for affine transforms
   panels.py     # Tab panel behavior
   panels.kv     # Tab panel layout
   uix (folder containing 'letter.png', tab_up.png', 'tab_down.png')
   
Of the files mentioned above, only a5.py should be modified.  The application is
fairly robust, and will still work (somewhat) if a5.py is missing
or is incomplete."""
import kivy
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.config import Config
from kivy.factory import Factory

# Local application code
import a5lib
from a5lib.dialogs import *
from a5lib.panels import *
import a5lib.geometry
import math

class StatPanel(BoxLayout):
    """Instances are a panel displaying information about the transformed Quad.
    
        tl is a Kivy property for the Label with the top left position
        
        tr is a Kivy property for the Label with the top right position

        bl is a Kivy property for the Label with the bottom left position
        
        br is a Kivy property for the Label with the bottom right position

        ma is a Kivy property for the Label with matrix a-value

        mb is a Kivy property for the Label with matrix b-value

        mc is a Kivy property for the Label with matrix c-value
        
        md is a Kivy property for the Label with matrix d-value

        off is a Kivy property for the Label with the offset vector

    These values are updated whenever the application transform changes."""
    tl = ObjectProperty(None)
    tr = ObjectProperty(None)
    bl = ObjectProperty(None)
    br = ObjectProperty(None)
    ma = ObjectProperty(None)
    mb = ObjectProperty(None)
    mc = ObjectProperty(None)
    md = ObjectProperty(None)
    off = ObjectProperty(None)
    
    def transform(self,transform):
        """Recompute the stats from the given transform.
        
        Precondition: transform is a Transform or None."""
        if (transform is None):
            return
        
        self.active = False

        # Make a 2x2 square
        bl = (-1,-1)
        br = ( 1,-1)
        tr = ( 1, 1)
        tl = (-1, 1)
        bl = transform.transform(bl)
        br = transform.transform(br)
        tr = transform.transform(tr)
        tl = transform.transform(tl)
        
        self.tl.text = '('+str(round(tl[0],3))+', '+str(round(tl[1],3))+')'
        self.tr.text = '('+str(round(tr[0],3))+', '+str(round(tr[1],3))+')'
        self.bl.text = '('+str(round(bl[0],3))+', '+str(round(bl[1],3))+')'
        self.br.text = '('+str(round(br[0],3))+', '+str(round(br[1],3))+')'
        
        matrix = transform.matrix
        offset = transform.vector
        
        try:
            if matrix is None:
                self.ma.text = '1.0'
                self.mb.text = '0.0'
                self.mc.text = '0.0'
                self.md.text = '1.0'
            else:
                self.ma.text = str(round(matrix.a,3))
                self.mb.text = str(round(matrix.b,3))
                self.mc.text = str(round(matrix.c,3))
                self.md.text = str(round(matrix.d,3))
        except:
            self.ma.text = 'ERR'
            self.mb.text = 'ERR'
            self.mc.text = 'ERR'
            self.md.text = 'ERR'

        try:
            if offset is None:
                self.off.text = '(0.0, 0.0)'
            else:
                self.off.text = '('+str(round(offset.x,3))+', '+str(round(offset.y,3))+')'
        except:
            self.off.text = 'Vector ERROR'

        self.active = True


class ViewPanel(Widget):
    """Instances are a panel displaying (transformed) Quad containing an image.
    
        corners is a Kivy property with the corners of the image
        
        image_file is a Kivy property with the file name for the image

    These corners are updated whenever the application transform changes.
    The image_file is updated when a new file is loaded."""
    corners = ListProperty([0]*8) # Have to initialize to size 8
    image_file = StringProperty('')
    
    def transform(self,transform):
        """Recompute the corners from the given transform.
        
        Precondition: transform is a Transform or None."""
        if (transform is None):
            return
    
        self.active = False

        # Calculate origin at center
        hx = self.size[0]/2.0
        hy = self.size[1]/2.0
        
        # Center as a vector
        origin = (self.pos[0]+hx,self.pos[1]+hy)
        
        # Make a 2x2 square
        bl = (-1,-1)
        br = ( 1,-1)
        tr = ( 1, 1)
        tl = (-1, 1)
        bl = transform.transform(bl)
        br = transform.transform(br)
        tr = transform.transform(tr)
        tl = transform.transform(tl)
        
        # Scale and shift by dimensions
        bl = (bl[0]*hx/2.0+origin[0],bl[1]*hy/2.0+origin[1])
        br = (br[0]*hx/2.0+origin[0],br[1]*hy/2.0+origin[1])
        tl = (tl[0]*hx/2.0+origin[0],tl[1]*hy/2.0+origin[1])
        tr = (tr[0]*hx/2.0+origin[0],tr[1]*hy/2.0+origin[1])

        self.corners = [bl[0],bl[1],br[0],br[1],tr[0],tr[1],tl[0],tl[1]]
        self.active = True


# This class is very unstable, and reflects the primitiveness of TabbedPanel
# It will likely need to be refactored in later additions.
class DynamicTabbedPanel(TabbedPanel):
    """Instances are a TabbedPanel where tabs can be added, removed, and reordered.
    
        transform is a Kivy property storing the currently active Transform
        object.
        
    In addition, the tab contents of the class are always a TransformPanel.
    This class has a notion of "active Transform", which is the composition
    of all the transforms from the tabs including and above the currently
    selected one."""
    transform = ObjectProperty(None)
    
    def __init__(self,**kwargs):
        """Constructor: Creates a DynamicTabbedPanel and passes the keyword
        arguments to the superclass."""
        super(DynamicTabbedPanel,self).__init__(**kwargs)
    
    def register(self):
        """Register this GUI object with the application.
        
        Necessary to hook up callbacks and perform any initialization that
        has to happen post-layout."""
        self.default_tab_text = ''
        panel = TransformPanel()
        panel.bind(transform=self.recalculate)
        self.default_tab_content = panel
        self.default_tab.background_down = 'a5lib/uix/tab_down.png'
        self.default_tab.background_normal = 'a5lib/uix/tab_up.png'
        self.transform = a5lib.geometry.Transform.Identity()
    
    def swap(self,x,y):
        """Swap the tab contents at positions x and y.
        
        Precondition: x and y refer to a valid tab position."""
        rng = len(self.tab_list)
        assert (0 <= x and x < rng and 0 <= y and y < rng)
        tab1 = self.tab_list[x]
        tab2 = self.tab_list[y]
        tmp_header = tab1.text
        tmp_content = tab1.content
        tab1.text = tab2.text
        tab1.content = tab2.content
        tab2.text = tmp_header
        tab2.content = tmp_content
        
        # It appears that switch_to is broken and does not actually move to a tab.
        # It just changes the content; the tabs have to be moved manually.
        if self.current_tab is tab1:
            tab1.state = 'normal'
            tab2.state = 'down'
            self.switch_to(tab2)
        elif self.current_tab is tab2:
            tab2.state = 'normal'
            tab1.state = 'down'
            self.switch_to(tab1)

    def shuffle_tab(self,pos,forward):
        """Shuffle the tab contents at pos forward or backward.
        
        Precondition: pos refers to a valid tab position; forward is a bool."""
        if forward and pos < len(self.tab_list)-1:
            self.swap(pos,pos+1)
        if not forward and pos > 0:
            self.swap(pos,pos-1)

    def shuffle_current_tab(self,forward):
        """Shuffle the current tab forward or backward.
        
        Precondition: forward is a bool."""
        pos = self.tab_list.index(self.current_tab)
        self.shuffle_tab(pos,forward)
        self.recalculate(None,None)

    def add_tab(self):
        """Adds a new tab to this TabbedPanel.
        
        The new tab will contain a TransformPanel and attach this panel
        as a listener to its transform property.  It will be added after
        the current tab, and the panel will switch to that tab.
        
        This implementation has a hard-limit of 6 tabs; the implementation
        will show an error dialog if this method tries to exceed that
        number of tabs."""
        if (len(self.tab_list) > 6):
            dialog = ErrorDialog('No more than 6 transforms allowed')
            dialog.size_hint = (0.7,0.6)
            dialog.pos_hint = {'x':0.15,'y':0.2}
            return
        
        pos = self.tab_list.index(self.current_tab)
        content = TransformPanel()
        content.bind(transform=self.recalculate)
        panel = TabbedPanelHeader(text='',content=content)
        panel.background_color = (0.8,0.8,0.5)
        panel.background_down = 'a5lib/uix/tab_down.png'
        panel.background_normal = 'a5lib/uix/tab_up.png'
        self.add_widget(panel)
        for x in range(pos):
            self.shuffle_tab(x,True)
        tab1 = self.tab_list[pos+1]
        tab2 = self.tab_list[pos]
        
        tab1.state = 'normal'
        tab2.state = 'down'
        self.switch_to(self.tab_list[pos])
        # Tab is identity; no recalculation needed.

    def del_tab(self):
        """Deletes the current tab from this TabbedPanel.

        When the tab is deleted, the panel chooses the tab above it
        as the selected one. If the only remaining tab is deleted,
        it removes the content and replaces it with a panel for an
        Identity transform."""
        if (len(self.tab_list) == 1):
            self.default_tab_content.unbind(transform=self.recalculate)
            panel = TransformPanel()
            panel.bind(transform=self.recalculate)
            self.default_tab_content = panel
            self.switch_to(self.tab_list[0]) # Hack to refresh content
            self.recalculate(panel,panel.transform)
            return
        
        pos = self.tab_list.index(self.current_tab)
        if (pos == len(self.tab_list)-1):
            self.shuffle_tab(pos,False)
            pos = pos-1
        
        tab = self.tab_list[pos]
        self.remove_widget(tab)
        tab.content.unbind(transform=self.recalculate)
        tab = self.tab_list[pos]
        self.switch_to(tab)
        tab.state = 'down'
        # Need to recalculate the active transform.
        self.recalculate(tab.content,tab.content.transform)
    
    def switch_to(self,header):
        """Overrides the base switch_to of TabbedPanel.
        
        Forces a recalculation of the active transform whenever we switch tabs."""
        super(DynamicTabbedPanel,self).switch_to(header)
        self.recalculate(None,None)
    
    def recalculate(self,obj,value):
        """Recalculates the active transform.
        
        The active transform is the composition of every transform from
        the current tab to the first one (the default tab).  Remember that
        the tab list in a TabbedPanel is actually in reverse order, so the
        default tab comes last."""
        if self.default_tab_content is None:
            return

        trans = self.default_tab_content.transform
        pos = self.tab_list.index(self.current_tab)
        cnt = len(self.tab_list)-2

        # Compose.
        # If compose is not implemented, this uses the selected tab.
        while cnt >= pos:
            trans = self.tab_list[cnt].content.transform.compose(trans)
            cnt = cnt-1
        self.transform = trans


class MainPanel(BoxLayout):
    """Instances are the main application panel.
    
    This panel arranges the major elements and hooks up the callbacks."""
    statpanel = ObjectProperty(None)
    parapanel = ObjectProperty(None)
    origpanel = ObjectProperty(None)
    tranpanel = ObjectProperty(None)

    def update(self,obj,value):
        """Updates both the image and statistics when the transform changes
        
        The arguments are given by the default Kivy callback mechanism, and
        hence are there to keep the program from crashing.  However, the
        values are ignored."""
        self.tranpanel.transform(self.parapanel.transform)
        self.statpanel.transform(self.parapanel.transform)

    def on_file_open(self,choice):
        """Callback function for image chooser.
        
        Used to load a new image file into the view panels.
        
        Precondition: choice is a name of an image file."""
        self.origpanel.image_file = choice
        self.tranpanel.image_file = choice
    
    def on_load_press(self):
        """Display an ImageDialog and set this object as the observer."""
        dialog = ImageDialog(self)
        dialog.size_hint = (0.75,0.75)
        dialog.pos_hint = {'x':0.125,'y':0.125}
   
    def register(self):
        """Register this GUI object with the application.
        
        Necessary to hook up callbacks and perform any initialization that
        has to happen post-layout."""
        self.parapanel.bind(transform=self.update)
        self.tranpanel.bind(pos=self.update)
        self.parapanel.register()
        self.update(None,None)

class TransformApp(App):
    def build(self):
        """Read kivy file and perform layout"""
        Config.set('graphics', 'width', '680')
        Config.set('graphics', 'height', '680')
        return MainPanel()

    def on_start(self):
        """Start up the app and initialize values"""
        super(TransformApp,self).on_start()
        self.root.register()

# Register UI elements for .kv files.
Factory.register("DynamicTabbedPanel", DynamicTabbedPanel)
Factory.register("ViewPanel", ViewPanel)
Factory.register("StatPanel", StatPanel)

# Application Code
if __name__ == '__main__':
    TransformApp().run()