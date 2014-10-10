# cturtle.py
# Walker M. White (wmw2)
# September 9, 2012
"""Cornell implementation of the Tk Turtle

This module is preferable to the default turtle module for several
reasons.  First, it makes it easier to support simultaneous
turtle windows.  Second, it provides support for our custom
color models.  Finally, the attributes and methods have been
streamlined to make them easier to understand."""
from colormodel import *
import turtle

# Helper function to check numeric input
def _is_number(n):
    return type(n) == int or type(n) == float

# Private class.  Not publicly available. Emulates the Screen singleton.
class _Window(turtle.TurtleScreen):

    _root = None
    _canvas = None
    _title = turtle._CFG["title"]

    # Copy of turtle.Screen, as non-singleton
    def __init__(self,x=100,y=100,width=800,height=800):
        self._root = turtle._Root()
        self._root.title(self._title)
        self._root.ondestroy(self._destroy)
        canvwidth = turtle._CFG["canvwidth"]
        canvheight = turtle._CFG["canvheight"]
        self._root.setupcanvas(width, height, canvwidth, canvheight)
        self._canvas = self._root._getcanvas()
        turtle.TurtleScreen.__init__(self, self._canvas)
        self._setup(width, height, x, y)

    # Copy of turtle.Screen, as non-singleton
    def _setup(self, width=turtle._CFG["width"], height=turtle._CFG["height"],
              startx=turtle._CFG["leftright"], starty=turtle._CFG["topbottom"]):
        """ Set the size and position of the main window."""
        if not hasattr(self._root, "set_geometry"):
            return
        sw = self._root.win_width()
        sh = self._root.win_height()
        if isinstance(width, float) and 0 <= width <= 1:
            width = sw*width
        if startx is None:
            startx = (sw - width) / 2
        if isinstance(height, float) and 0 <= height <= 1:
            height = sh*height
        if starty is None:
            starty = (sh - height) / 2
        self._root.set_geometry(width, height, startx, starty)
        self.update()

    # Copy of turtle.Screen, as non-singleton
    def _destroy(self):
        root = self._root
        turtle.Turtle._pen = None
        turtle.Turtle._screen = None
        self._root = None
        self._canvas = None
        turtle.TurtleScreen._RUNNING = True
        root.destroy()


class Window(object):
    """Instances are GUI windows that support turtle graphics
    
    You should construct a Window object before constructing a
    Turtle or Pen.  You will only need one Window object for the
    entire assignment."""
    _frame = None # Wrapper to private object
    _turtles = [] # Active turtles
    _gpens = []   # Active pens
    
    # Mutable properties
    
    @property
    def x(self):
        """x coordinate for top left corner of window
        
        **Invariant**: x must be an int"""
        return self._x
    
    @x.setter
    def x(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        self._x = value
        self._reshape()
    
    @property
    def y(self):
        """y coordinate for top left corner of window
        
        **Invariant**: y must be an int"""
        return self._frame._y
    
    @y.setter
    def y(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        self._y = value
        self._reshape()
    
    @property
    def width(self):
        """width of the window in pixels
        
        **Invariant**: width must be an int"""
        return self._width
    
    @width.setter
    def width(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value > 0), "value %s is negative" % `value`
        self._width = value
        self._reshape()
    
    @property
    def height(self):
        """height of the window in pixels
        
        **Invariant**: height must be an int"""
        return self._height
    
    @height.setter
    def height(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value > 0), "value %s is negative" % `value`
        self._height = value
        self._reshape()
    
    @property
    def title(self):
        """title displayed at top of window bar
        
        **Invariant**: title must be a string"""
        return self._frame._title
    
    @title.setter
    def title(self,value):
        assert (type(value) == str), "value %s is not a string" % `value`
        self._frame._root.title(value)
        self._frame._title = value
    
    # Immutable properties

    @property
    def turtles(self):
        """list of all turtles attached to this Window
        
        *This attribute may not be altered directly*"""
        return self._turtles[:]

    @property
    def pens(self):
        """list of all pens attached to this Window
        
        *This attribute may not be altered directly*"""
        return self._gpens[:]

    @property
    def shapes(self):
        """list containing all supported turtle shapes
        
        *This attribute may not be altered di*"""
        return self._frame.getshapes()
    
    # Built-in Methods
    
    def __init__(self,x=100,y=100,width=800,height=800):
        """**Constructor**: creates a new Window to support turtle graphics
        
            :param x: initial x coordinate (default 100)
            **Precondition**: int
            
            :param y: initial y coordinate (default 100)
            **Precondition**: int
        
            :param width: initial window width (default 800)
            **Precondition**: int
        
            :param height: initial window height (default 800)
            **Precondition**: int
        
        All parameters are optional."""
        self._frame = _Window(x,y,width,height)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        try:
            self._frame.addshape('pencil.gif')
        except:
            pass

    def __del__(self):
        try:
            self._frame._destroy()
        except:
            pass
        self._turtles = []
        self._gpens = []
        del self._frame

    # Methods
    
    # Copy of turtle.Screen, as non-singleton
    def _reshape(self):
        self._frame._setup(width=self._width,height=self._height,
                           startx=self._x,starty=self._y)

    # Add a turtle to this Window
    def _addTurtle(self,turt):
        self._turtles.append(turt)

    # Add a pen to this Window
    def _addPen(self,pen):
        self._gpens.append(pen)

    # Remove a turtle from this Window
    def _removeTurtle(self,turt):
        if turt in self._turtles:
            self._turtles.remove(turt)

    # Remove a pen from this Window
    def _removePen(self,pen):
        if pen in self._gpens:
            self._gpens.remove(pen)
    
    def clear(self):
        """Erase the contents of this Window
        
        All Turtles and Pens are eliminated from the Window.
        Any attempt to use a previously created Turtle or Pen
        will fail."""
        self._frame.clear()
        self._turtles = []
        self._gpens = []

    def bye(self):
        """Shut the graphics Window"""
        self._frame._destroy()
        self._turtles = []
        self._gpens = []
        del self._frame


# Helper function to support colormodel in turtles
def _is_turtle_color(c):
    return (type(c) == RGB or
            type(c) == HSV or
            type(c) == str or
            type(c) == tuple)


# Helper function to support colormodel in turtles
def _to_turtle_color(c):
    return c.turtleColor() if (type(c) == RGB or type(c) == HSV) else c

class Turtle(object):
    """Instance is a graphics turtle.
    
    Graphics turtle is a pen that is controlled by direction
    and movement.  The turtle is a cursor that that you control
    by moving it left, right, forward, or backward.  As it moves,
    it draws a line of the same color as the Turtle."""
    
    _screen = None
    _turtle = None

    # Mutable properties
    
    @property
    def heading(self):
        """The heading of this turtle in degrees.
        
        Heading is measured counter clockwise from due east.
        
        **Invariant**: Value must be a float"""
        return float(self._turtle.heading())
    
    @heading.setter
    def heading(self,value):
        assert (_is_number(value)), "value %s is not a valid number" % `value`
        self._turtle.setheading(value)

    @property
    def speed(self):
        """The animation speed of this turtle.
        
        The speed is an integer from 0 to 10. Speed = 0 means that no animation
        takes place. The methods forward/back makes turtle jump and likewise
        left/right make the turtle turn instantly.

        Speeds from 1 to 10 enforce increasingly faster animation of line
        drawing and turtle turning. 1 is the slowest speed while 10 is the
        fastest (non-instantaneous) speed.

        **Invariant**: Value must be an integer value in the range 0..10."""
        return self._turtle.speed()
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 or value <= 10), "value %s is outside the range 0..10" % `value`
        self._turtle.speed(value)

    @property
    def color(self):
        """The color of this turtle.
        
        All subsequent draw commands (forward/back) draw using this color.
        If the color changes, it only affects future draw commands, not
        past ones.
        
        **Invariant**: Value must be either a string with a color name, a
        3 element tuple of floats between 0 and 1 (inclusive), or an object
        in an additive color model (e.g. RGB or HSV)."""
        return self._color
    
    @color.setter
    def color(self,value):
        assert (_is_turtle_color(value)), "value %s is not a valid color input" % `value`
        self._turtle.color(_to_turtle_color(value))
        self._color = self._turtle.color()[0]
    
    @property
    def visible(self):
        """Indicates whether the turtle's icon is visible.
        
        Drawing commands will still work while the turtle icon is hidden.
        There will just be no indication of the turtle's current location
        on the screen.
        
        **Invariant**: Value must be a bool"""
        return self._turtle.isvisible()
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        if value and not self._turtle.isvisible():
            self._turtle.showturtle()
        elif not value and self._turtle.isvisible():
            self._turtle.hideturtle()
    
    @property
    def drawmode(self):
        """Indicates whether the turtle is in draw mode.
        
        All drawing calls are active if an only if this mode is True
        
        **Invariant**: Value must be a bool"""
        return self._turtle.isdown()
    
    @drawmode.setter
    def drawmode(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        if value and not self._turtle.isdown():
            self._turtle.pendown()
        elif not value and self._turtle.isdown():
            self._turtle.penup()

    
    # Immutable properties
    
    @property
    def x(self):
        """The x-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.xcor()
    
    @property
    def y(self):
        """The y-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.ycor()

    # Built-in Methods

    def __init__(self,screen,position=(0, 0), color='red', heading=180, speed=0):
        """**Constructor**: Create a new turtle to draw on the given screen.

            :param screen: window object that turtle will draw on.
            **Precondition**: object of type Window.
            
            :param position: initial turtle position (origin is screen center)
            **Precondition**: 2D tuple of floats or ints.
            
            :param color: initial turtle color (default red)
            **Precondition**: either a string with a color name, a 3 element
            tuple of floats between 0 and 1 (inclusive), or an object in an
            additive color model (e.g. RGB or HSV).
            
            :param heading: initial turtle directions (default 180)
            **Precondition**: a float or int

            :param speed: initial turtle speed (default 0)
            **Precondition**: a int between 0 and 10, inclusive
        
        The argument ``screen`` is not optional."""

        assert type(screen) == Window
        self._turtle = turtle.RawTurtle(screen._frame)
        self._turtle.hideturtle()

        self._screen = screen
        screen._addTurtle(self)
        self._turtle.shape('turtle')
        self._turtle.penup()
        self.color = color
        self._turtle.setposition(position)
        self._turtle.setheading(heading)
        self._turtle.speed(speed)
        self._turtle.pendown()
        self._turtle.showturtle()
    
    def __repr__(self):
        """Returns: Unambiguous string representation of this turtle. """
        return super(Turtle,self).__repr__()

    # A printable representation of the turtle, giving its position, color, and heading
    def __str__(self):
        """Returns: Readable string representation of this turtle. """
        return 'Turtle[position={}, color={}, heading={}]'.format((self.x,self.y), self.color, self.heading)
    
    def __del__(self):
        """Deletes this turtle object. """
        self.clear()
        self._screen._removeTurtle(self)
        del self._turtle
    
    # Methods
    
    def forward(self,distance):
        """Move the turtle forward.
        
            :param distance: distance to move in pixels
            **Precondition**: a float or int
        
        Draws a line if drawmode is True."""
        self._turtle.forward(distance)

    def backward(self,distance):
        """Move the turtle backward.
        
            :param distance: distance to move in pixels
            **Precondition**: a float or int
        
        Draws a line if drawmode is True."""
        self._turtle.backward(distance)

    def right(self,degrees):
        """Turn the turtle to the right.
        
            :param degrees: amount to turn right in degrees
            **Precondition**: a float or int
        
        Nothing is drawn."""
        self._turtle.right(degrees)

    def left(self,degrees):
        """Turn the turtle to the left.
        
            :param degrees: amount to turn left in degrees
            **Precondition**: a float or int
        
        Nothing is drawn."""
        self._turtle.left(degrees)

    def move(self,x,y):
        """Moves the turtle to given position without drawing.
        
            :param x: new x position for turtle
            **Precondition**: a float or int
        
            :param y: new y position for turtle
            **Precondition**: a float or int
        
        This method does not draw, regardless of the drawmode."""
        assert (_is_number(x)), "parameter x:%s is not a valid number" % `x`
        assert (_is_number(y)), "parameter y:%s is not a valid number" % `y`
        d = self._turtle.isdown()
        if d:
            self._turtle.penup()
        self._turtle.setposition(x,y)
        if d:
            self._turtle.pendown()

    def clear(self):
        """Delete the turtle's drawings from the window, but do not move
        the turtle or alter its attributes."""
        self._turtle.clear()

    def reset(self):
        """Delete the turtle's drawings from the window, re-center the turtle
        and reset all attributes to their default values."""
        self._turtle.clear()
        self._turtle.setposition((0,0))        
        self._turtle.shape('turtle')
        self.color = 'red'
        self.heading = 180
        self.speed = 0


class Pen(object):
    """Instance is a graphics pen.
    
    A graphics pen is like a turtle except that it does not have
    a heading, and there is no drawmode attribute.
    Instead, the pen relies on explicit drawing commands such
    as drawLine or drawCircle.
    
    Another difference with the pen is that it can draw solid
    shapes.  The pen has an attribute called ``fill``.  When this
    attribute is set to True, it will fill the insides of any
    polygon traced by its drawLine method.  However, the fill
    will not be completed until fill is set to False, or
    the move method is invoked."""
    
    _screen = None
    _turtle = None

    # Mutable properties

    @property
    def speed(self):
        """The animation speed of this pen.
        
        The speed is an integer from 0 to 10. Speed = 0 means that
        no animation takes place. The drawLine and drawCircle
        methods happen instantly with no animation.

        Speeds from 1 to 10 enforce increasingly faster animation of line
        drawing. 1 is the slowest speed while 10 is the fastest
        (non-instantaneous) speed.

        **Invariant**: Value must be an integer value in the range 0..10."""
        return self._turtle.speed()
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 or value <= 10), "value %s is outside the range 0..10" % `value`
        self._turtle.speed(value)
    
    @property
    def fill(self):
        """The fill status of this pen.
        
        If the fill status is True, then the pen will fill the insides
        of any polygon or circle subsequently traced by its drawLine
        or drawCircle method. Ifthe attribute changes, it only affects
        future draw commands, not past ones. Switching this attribute
        between True and False allows the pen to draw both solid and
        hollow shapes.
        
        **Invariant**: Value must be an bool."""
        return self._turtle.fill()
    
    @fill.setter
    def fill(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        self._turtle.fill(value)
        # Make the pen state relative to fill.
        if value and not self._turtle.isdown():
            self._turtle.pendown()
        elif not value and self._turtle.isdown():
            self._turtle.penup()

    # silent property requested by beta tester
    @property
    def color(self):
        assert False, 'Pen does not have a color; use pencolor or fillcolor'

    @color.setter
    def color(self,value):
        assert False, 'Pen does not have a color; use pencolor or fillcolor'

    @property
    def pencolor(self):
        """The pen color of this pen.
        
        The pen color is used for drawing lines and circles.  All subsequent
        draw commands draw using this color. If the color changes, it only
        affects future draw commands, not past ones.

        This color is only used for lines and the border of circles.
        It is not the color used for filling in solid areas (if the
        ``fill`` attribute is True).  See the attribute
        ``fillcolor`` for solid shapes.
        
        **Invariant**: Value must be either a string with a color name, a
        3 element tuple of floats between 0 and 1 (inclusive), or an object
        in an additive color model (e.g. RGB or HSV)."""
        return self._pencolor
    
    @pencolor.setter
    def pencolor(self,value):
        assert (_is_turtle_color(value)), "value %s is not a valid color input" % `value`
        self._turtle.color(_to_turtle_color(value),self._fillcolor)
        self._pencolor = self._turtle.color()[0]

    @property
    def fillcolor(self):
        """The fill color of this turtle.
        
        The fill color is used for filling in solid shapes. If the
        ``fill`` attribute is True, all subsequent draw
        commands fill their insides using this color.  If the color
        changes, it only affects future draw commands, not past ones.
        
        This color is only used for filling in the insides of solid
        shapes.  It is not the color used for the shape border.
        See the attribute ``pencolor`` for the border color.
        
        **Invariant**: Value must be either a string with a color name, a
        3 element tuple of floats between 0 and 1 (inclusive), or an object
        in an additive color model (e.g. RGB or HSV)."""
        return self._fillcolor

    @fillcolor.setter
    def fillcolor(self,value):
        assert (_is_turtle_color(value)), "value %s is not a valid color input" % `value`
        self._turtle.color(self._pencolor,_to_turtle_color(value))
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[1]
    
    @property
    def visible(self):
        """Indicates whether the pen's icon is visible.
        
        Drawing commands will still work while the pen icon is hidden.
        There will just be no indication of the pen's current location
        on the screen.
        
        **Invariant**: Value must be a bool"""
        return self._turtle.isvisible()
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        if value and not self._turtle.isvisible():
            self._turtle.showturtle()
        elif not value and self._turtle.isvisible():
            self._turtle.hideturtle()

    # Immutable properties
    
    @property
    def x(self):
        """The x-coordinate of this pen.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.xcor()
    
    @property
    def y(self):
        """The y-coordinate of this pen.
        
        To change the y coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.ycor()

    # Built-in Methods
    
    def __init__(self,screen,position=(0, 0), color='red', speed=0):
        """**Constructor**: Create a new pen to draw on the given screen.

            :param screen: window object that pen will draw on.
            **Precondition**: object of type Window.
            
            :param position: initial pen position (origin is screen center)
            **Precondition**: 2D tuple of floats or ints.
            
            :param color: initial pen and fill color (default red)
            **Precondition**: either a string with a color name, a 3 element
            tuple of floats between 0 and 1 (inclusive), or an object in an
            additive color model (e.g. RGB or HSV).
            
            :param speed: initial turtle speed (default 0)
            **Precondition**: a int between 0 and 10, inclusive
        
        The argument ``screen`` is not optional."""
        assert type(screen) == Window
        self._turtle = turtle.RawTurtle(screen._frame)
        self._turtle.hideturtle()
        
        self._screen = screen
        screen._addPen(self)
        try:
            self._turtle.shape('pencil.gif')
        except:
            self._turtle.shape('classic')
        self._turtle.penup()
        self._turtle.setposition(position)
        self._turtle.color(color)
        self._turtle.speed(speed)
        self._turtle.showturtle()
        
        # Record current color
        #"pair" seems unused
        #pair = self._turtle.color() 
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[0]
    
    def __repr__(self):
        """Returns: Unambiguous string representation of this pen. """
        return super(Turtle,self).__repr__()
        
    def __str__(self):
        """Returns: Readable string representation of this pen. """
        return 'Pen(position={}, pencolor={}, fillcolor={})'.format(self._turtle.position(), self.pencolor, self.fillcolor)
    
    def __del__(self):
        """Deletes this pen object. """
        self._screen._removePen(self)
        del self._turtle

    # Methods

    def clear(self):
        """Delete the pen's drawings from the window, but do not move
        the pen or alter its attributes."""
        self._turtle.clear()

    def reset(self):
        """Delete the pen's drawings from the window, re-center the pen
        and reset all attributes to their default values."""
        self._turtle.clear()
        self._turtle.setposition((0,0))        
        try:
            self._turtle.shape('pencil.gif')
        except:
            self._turtle.shape('classic')
        self._turtle.color('red')
        self.speed = 0
        
        #pair = self._turtle.color()
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[0]
 

    def move(self,x,y):
        """Moves the pen to given position without drawing.
        
            :param x: new x position for pen
            **Precondition**: a float or int
        
            :param y: new y position for pen
            **Precondition**: a float or int
        
        If the ``fill`` attribute is currently True, this
        method will complete the fill before moving to the
        new region. The space between the original position
        and (x,y) will not be connected."""
        assert (_is_number(x)), "parameter x:%s is not a valid number" % `x`
        assert (_is_number(y)), "parameter y:%s is not a valid number" % `y`
        fstate = self._turtle.fill()
        if fstate: # invariant; pen only down if filling
            self._turtle.fill(False)
            self._turtle.penup()
        self._turtle.setposition(x,y)
        if fstate: # invariant; pen only down if filling
            self._turtle.pendown()
            self._turtle.fill(True)
        
    # Drawing Methods
    def drawLine(self, dx, dy):
        """Draw a line segment (dx,dy) from the current pen position
        
            :param dx: change in the x position
            **Precondition**: a float or int
        
            :param dy: change in the y position
            **Precondition**: a float or int
        
        The line segment will run from (x,y) to (x+dx,y+dy), where
        (x,y) is the current pen position.  When done, the pen will
        be at position (x+dx,y+dy)"""
        assert (_is_number(dx)), "parameter x:%s is not a valid number" % `dx`
        assert (_is_number(dy)), "parameter y:%s is not a valid number" % `dy`
        if not self.fill: # invariant; pen only down if filling
            self._turtle.pendown()
        x = self._turtle.xcor()
        y = self._turtle.ycor()
        self._turtle.setposition(x+dx, y+dy)
        if not self.fill: # invariant; pen only down if filling
            self._turtle.penup()
    
    def drawTo(self, x, y):
        """Draw a line from the current pen position to (x,y)
        
            :param x: finishing x position for line
            **Precondition**: a float or int
        
            :param y: finishing y position for line
            **Precondition**: a float or int
        
        When done, the pen will be at (x, y)."""
        assert (_is_number(x)), "parameter x:%s is not a valid number" % `x`
        assert (_is_number(y)), "parameter y:%s is not a valid number" % `y`
        if not self.fill: # invariant; pen only down if filling
            self._turtle.pendown()
        self._turtle.setposition(x, y)
        if not self.fill: # invariant; pen only down if filling
            self._turtle.penup()


    def drawCircle(self, r):
        """Draw a circle of radius r centered on the pen.
        
            :param r: radius of the circle
            **Precondition**: a float or int

        The center of the circle is the current pen coordinates.
        When done, the position of the pen will remain unchanged"""
        assert (_is_number(r)), "parameter r:%s is not a valid number" % `r`
        x = self._turtle.xcor()
        y = self._turtle.ycor()
        self._turtle.setposition(x, y-r)
        if not self.fill: # invariant; pen only down if filling
            self._turtle.pendown()
        self._turtle.circle(r)
        if not self.fill: # invariant; pen only down if filling
            self._turtle.penup()
        self._turtle.setposition(x, y)
