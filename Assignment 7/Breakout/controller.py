# controller.py
# Jonathan Lee (jwl274) and Quinn Beightol (qeb2)
# 12/1/12
#Extension for Breakout ----
#Implemented Sound Files that play whenever the ball hits
#the paddle or the ball hits a brick (sound files rotate for when ball hits a
# brick) Has ability to change sound on or off.

#Improved User Control over Bounces. If ball hits the left eigth or right
#eighth of the paddle, the _vx and _vy directions are negated

#Continue End Functionality. If player loses, player is given
#the option to continue (lives reset to 3) or to quit (window closes)

#Pause Feature. Pause GLabel object at lower right hand corner.
#Pauses game if touched down. Unpauses if touched down on again.

#Score. Score board on top right hand corner. Increments by
#one whenever a brick is broken.

#Kicker. Every 7th time that the ball hits the paddle, ._vx is increased by
#1.5 and ._vy is increased by 1.5. Also, the color of the ball changes
#(the ball starts out black, but after the first kicker, the ball's color cycles
#through the brick colors-- the ball never goes back to black)
"""Controller module for Breakout

This module contains a class and global constants for the game Breakout.
Unlike the other files in this assignment, you are 100% free to change
anything in this file. You can change any of the constants in this file
(so long as they are still named constants), and add or remove classes."""
import colormodel
import random
import sys
from graphics import *

# CONSTANTS

# Width of the game display (all coordinates are in pixels)
GAME_WIDTH  = 480
# Height of the game display
GAME_HEIGHT = 620

# Width of the paddle
PADDLE_WIDTH = 58
# Height of the paddle
PADDLE_HEIGHT = 11
# Distance of the (bottom of the) paddle up from the bottom
PADDLE_OFFSET = 30

# Horizontal separation between bricks
BRICK_SEP_H = 5
# Vertical separation between bricks
BRICK_SEP_V = 4
# Height of a brick
BRICK_HEIGHT = 8
# Offset of the top brick row from the top
BRICK_Y_OFFSET = 70

# Number of bricks per row
BRICKS_IN_ROW = 10
# Number of rows of bricks, in range 1..10.
BRICK_ROWS = 10
# Width of a brick
BRICK_WIDTH = GAME_WIDTH / BRICKS_IN_ROW - BRICK_SEP_H

# Diameter of the ball in pixels
BALL_DIAMETER = 18

# Number of attempts in a game
NUMBER_TURNS = 3

# Basic game states
# Game has not started yet
STATE_INACTIVE = 0
# Game is active, but waiting for next ball
STATE_PAUSED   = 1
# Ball is in play and being animated
STATE_ACTIVE   = 2
# Game is over, deactivate all actions
STATE_COMPLETE = 3
#Game is paused, ball and paddle are frozen
STATE_FREEZE = 4

# ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY
#List of colors for creating rows of bricks
BRICK_COLOR = [colormodel.RED,colormodel.ORANGE,colormodel.YELLOW,colormodel.GREEN,colormodel.CYAN]

#Basic Paddle States
#Touch is down and paddle can be moved
PADDLE_MOVE = 1
#Touch is up and paddle cannot be moved
PADDLE_STOP = 0

#Basic Sound States
#Sound is On, Sounds made when ball collides with bricks or paddle
SOUND_ON = 0
#Sound is off, No sounds made when ball collides with bricks or paddle
SOUND_OFF=1

#Sound Files
#bounce.wav for when ball collides with paddle
bounceSound=Sound('bounce.wav')
#cup1.wav for when ball collides with bricks
bounceSound2=Sound('cup1.wav')
#saucer1.wav for when ball collides with bricks
bounceSound3=Sound('saucer1.wav')
#saucer2.wav for when ball collides with bricks
bounceSound4=Sound('saucer2.wav')
#plate1.wav for when ball collides with bricks
bounceSound5=Sound('plate1.wav')


# CLASSES
class Breakout(GameController):
    """Instance is the primary controller for Breakout.

    This class extends GameController and implements the various methods
    necessary for running the game.

        Method initialize starts up the game.

        Method update animates the ball and provides the physics.

        The on_touch methods handle mouse (or finger) input.

    The class also has fields that provide state to this controller.
    The fields can all be hidden; you do not need properties. However,
    you should clearly state the field invariants, as the various
    methods will rely on them to determine game state."""
    # FIELDS.

    # Current play state of the game; needed by the on_touch methods
    # Invariant: One of STATE_INACTIVE, STATE_PAUSED, STATE_ACTIVE
    _state  = STATE_INACTIVE

    # List of currently active "bricks" in the game.
    #Invariant: A list of  objects that are instances of GRectangle (or a
    #subclass) If list is  empty, then state is STATE_INACTIVE (game over)
    _bricks = []

    # The player paddle
    # Invariant: An object that is an instance of GRectangle (or a subclass)
    # Also can be None; if None, then state is STATE_INACTIVE (game over)
    _paddle = None

    # The ball to bounce about the game board
    # Invariant: An object that is an instance of GEllipse (or a subclass)
    # Also can be None; if None, then state is STATE_INACTIVE (game over) or
    # STATE_PAUSED (waiting for next ball)
    _ball = None

    # ADD MORE FIELDS (AND THEIR INVARIANTS) AS NECESSARY
    
    #The message displayed prior to the beginning of a game
    #Invariant: An object that is an instance of GLabel (or a subclass).
    #Can also be none if no message exists to display. 
    _message = None
    
    #The score to be displayed at the top right hand corner
    #Invariant: An object that is an instance of GLabel (or a subclass).
    #Can be None when a Glabel object for _score has not yet been created
    _score = None
    
    #Current paddle state of the game; used by on touch methods
    #Determines if paddle can be moved or not.
    #Invariant: One of PADDLE_MOVE or PADDLE_STOP
    _paddle_collide = PADDLE_STOP
    
    #The object that the ball is currently colliding with, or None if there
    #isn't a collision
    #Invariant: object must be a GRectangle object representing a brick, a
    #GRectangle object representing the paddle, or None
    _colliding_object = None
    
    #Continue message to display to user when state is STATE_COMPLETE
    #and game still has bricks left remaining.
    #Invariant: An object that is an instance GLabel (or a subclass).
    #Can be none when GLabel object for _tryy has not yet been created (state is not STATE_COMPLETE)
    _tryy=None
    
    #End message to display to user when state is STATE_COMPLETE
    #and game still has bricks left remaining.
    #Invariant: An object that is an instance of GLabel (or a subclass).
    #Can be none when GLabel object for _tryn has not yet been created (state is not STATE_COMPLETE)
    _tryn=None
    
    #Number of Lives left remaining for the player.
    #_lives decreases by one whenever player loses a ball
    #Invariant: _lives is 0 <= NUMBER_TURNS
    _lives = NUMBER_TURNS
    
    #Pause Message to display during the game.
    #On touch down on pause will pause the game
    #Invariant: An object that is an instance of GLabel (or a subclass)
    #Can be none when GLabel object for _pause has not yet been created. 
    _pause = None
    
    #Number of times the ball strikes the counter.
    #Used to implement kicker for Breakout. Increases by 1 every time ball strikes paddle.
    #Invariant: _paddlecounter is an integer that specifies # of times ball hits paddle.
    _paddlecounter = 0
    
    #Number of times ball hits a brick. Increments by one every time it does.
    #Used to rotate between sound audio files.
    #Invariant: _souundcounter is an integer that specifies # of times ball hits a brick.
    _soundcounter = 0
    
    #Sound Message to display during game.
    #Shows user whether sound is currently ON or OFF.
    #Invariant: An object that is an instance of GLabel.
    #Can be none when GLabel object for _sound has not yet been created. 
    _sound= None
    
    #Current Sound States for sound. Determines whether or not sound is played during game.
    #Invariant: One of SOUND_ON or SOUND_OFF
    _soundplay = SOUND_ON
    
    #Keeps track of the color of the ball once the ball has been kicked.
    #BRICK_COLOR[(self._color_counter - 1) % 5) is the color of the ball,
    #assuming it has already been kicked (otherwise the ball is black by
    #default)
    #Invariant: An int >= 0
    _color_counter = 0
    # METHODS

    def initialize(self):
        """Initialize the game state.

        Initialize any state fields as necessary to statisfy invariants.
        When done, set the state to STATE_INACTIVE, and display a message
        saying that the user should press to play a game."""
        # IMPLEMENT ME

        self._message = GLabel(text = 'Press To Play',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
        self.view.add(self._message)
        self._state = STATE_INACTIVE
    
    def update(self, dt):
        """Animate a single frame in the game.

        This is the method that does most of the work.  It moves the ball, and
        looks for any collisions.  If there is a collision, it changes the
        velocity of the ball and removes any bricks if necessary.

        This method may need to change the state of the game.  If the ball
        goes off the screen, change the state to either STATE_PAUSED (if the
        player still has some tries left) or STATE_COMPLETE (the player has
        lost the game).  If the last brick is removed, it needs to change
        to STATE_COMPLETE (game over; the player has won).

        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored."""
        # IMPLEMENT ME
        if self._state == STATE_ACTIVE:
            self._ball.move_ball()
            self._colliding_object = self._get_colliding_object()
            self._play_sounds()
            self._ball_collision()
            self._bounce()
            self._score.text = 'Score: ' + `(BRICKS_IN_ROW * BRICK_ROWS) - len(self._bricks)`
            self._pause.text = 'Pause'
        elif self._state ==STATE_FREEZE:
            self._pause.text = 'Unpause'
            self._paddle_collide = PADDLE_STOP
            
        
    def on_touch_down(self,view,touch):
        """Respond to the mouse (or finger) being pressed (but not released)

        If state is STATE_ACTIVE or STATE_PAUSED, then this method should
        check if the user clicked inside the paddle and begin movement of the
        paddle.  Otherwise, if it is one of the other states, it moves to the
        next state as appropriate.

        Precondition: view is just the view attribute (unused because we have
        access to the view attribute).  touch is a MotionEvent (see
        documentation) with the touch information."""
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self.view.remove(self._message)
            self._state = STATE_PAUSED
            self._setup_bricks()
            self._create_paddle(GAME_WIDTH /2.0)
            self._create_pause()
            self._create_scoreboard()
            self._wait_message()
            self._create_sound()
            self._paddlecounter = 0
            self._color_counter = 0
        self._contend(touch)
        self._pausetouch(touch)
        self._sound_toggle(touch)
        
        if self._state == STATE_PAUSED or self._state ==STATE_ACTIVE:
            if self._paddle.collide_point(touch.x,touch.y):
                self._paddle_collide = PADDLE_MOVE
        
            
    def on_touch_move(self,view,touch):
        """Respond to the mouse (or finger) being moved.

        If state is STATE_ACTIVE or STATE_PAUSED, then this method should move
        the paddle. The distance moved should be the distance between the
        previous touch event and the current touch event. For all other
        states, this method is ignored.

        Precondition: view is just the view attribute (unused because we have
        access to the view attribute).  touch is a MotionEvent (see
        documentation) with the touch information."""
        # IMPLEMENT ME
        if self._state == STATE_ACTIVE or self._state == STATE_PAUSED:
            if self._paddle_collide==PADDLE_MOVE:
                touch.x = max(PADDLE_WIDTH/2,touch.x)
                touch.x = min(touch.x,GAME_WIDTH-PADDLE_WIDTH/2)
                self._paddle.center_x = touch.x
            
    def on_touch_up(self,view,touch):
        """Respond to the mouse (or finger) being released.

        If state is STATE_ACTIVE, then this method should stop moving the
        paddle. For all other states, it is ignored.

        Precondition: view is just the view attribute (unusaed because we have
        access to the view attribute).  touch is a MotionEvent (see
        documentation) with the touch information."""
        # IMPLEMENT ME
        self._paddle_collide = PADDLE_STOP

    # ADD MORE HELPER METHODS (PROPERLY SPECIFIED) AS NECESSARY
    
    def _setup_bricks(self):
        """Creates Rows of Bricks and adds them to both the view and the field _bricks
        in the form of a list. Number of rows of bricks is determined by the constant
        BRICK_ROWS. Number of bricks in a row is determined by the constant
        BRICKS_IN_ROW. Dimensions and spacing of bricks are also determined by
        constants within controller. The colors of bricks remain constant for two
        rows and run in a sequence of RED,ORANGE,YELLOW,GREEN,CYAN."""
        
        xcoord = BRICK_SEP_H / 2
        ycoord = GAME_HEIGHT - BRICK_Y_OFFSET
        brick = None
        bcolor = colormodel.RED
        for x in range(BRICK_ROWS):
            if (x/2) % 5 == 0:
                bcolor == BRICK_COLOR[0]
            elif (x/2) % 5 ==1:
                bcolor = BRICK_COLOR[1]
            elif (x/2) % 5 ==2:
                bcolor = BRICK_COLOR[2]
            elif (x/2)%5 ==3:
                bcolor = BRICK_COLOR[3]
            elif (x/2)%5 ==4:
                bcolor = BRICK_COLOR[4]
            for x in range(BRICKS_IN_ROW):
                brick = GRectangle(pos=(xcoord,ycoord),size = (BRICK_WIDTH,BRICK_HEIGHT),linecolor = bcolor,fillcolor=bcolor)
                xcoord = xcoord + BRICK_WIDTH + BRICK_SEP_H
                self.view.add(brick) # Add to view
                self._bricks.append(brick) # Add to controller
            ycoord = ycoord - BRICK_HEIGHT - BRICK_SEP_V
            xcoord = BRICK_SEP_H / 2
            
    def _create_paddle(self,xcoord):
        """Helper Function to create a paddle. Used in on touch_down
        to setup the game. Puts GRectangle object corresponding
        to paddle into field _paddle and adds _paddle to the view. 
        
        Precondition: xcoord is a int or a float."""
        
        self._paddle = GRectangle(size=(PADDLE_WIDTH,PADDLE_HEIGHT),y = PADDLE_OFFSET,center_x=xcoord)
        self.view.add(self._paddle)
        
    def _create_pause(self):
        """Helper Function to create pause text in lower right hand corner.
        Used in on touch_down to pause the game. Puts GLabel object corresponding
        to pause into field _pause and adds _pause to the view. """
        
        self._pause = GLabel(text = 'Pause',pos=(GAME_WIDTH - 50,5),font_size=9)
        self.view.add(self._pause)
        
    def _create_sound(self):
        """Helper Function to create sound text in lower left hand corner.
        Used in on touch_down to change sound states of the game. Puts GLabel object corresponding
        to sound into field _sound and adds _sound to the view. """
        
        self._sound = GLabel(text = 'Sound: On',pos=(20,5),font_size=9)
        self.view.add(self._sound)
        
    def _create_ball(self):
        """Helper Function to create ball. Removes the current message displayed
        in the view and creates a Ball using the constructor for the class Ball.
        Used in on touch_down to pause the game. Puts GEllipse object corresponding
        to ball into field _ball and adds _ball to the view.
        Function then changes the current state to STATE_ACTIVE indicating
        the game has begun and the ball is in play"""
        
        self.view.remove(self._message)
        self._ball = Ball()
        self.view.add(self._ball)
        self._state = STATE_ACTIVE
    
    def _sound_toggle(self,touch):
        """Helper function to change sound state. If user touches
        down on _sound object, state changes to either SOUND_ON
        or SOUND_OFF depending on its current state and alters
        the text of _sound's GLabel object accordingly.
        
        Precondition: touch is a MotionEvent"""
        
        if self._sound.collide_point(touch.x,touch.y) and self._soundplay == SOUND_OFF:
            self._soundplay=SOUND_ON
            self._sound.text= 'Sound: On'
        
        elif self._sound.collide_point(touch.x,touch.y) and self._soundplay == SOUND_ON:
            self._sound.text='Sound: Off'
            self._soundplay = SOUND_OFF

    def _create_scoreboard(self):
        """Helper Function to create score text in top right hand corner.
        Puts GLabel object corresponding to score into field _score and
        adds _score to the view. """
        
        self._score = GLabel(text = 'Score:' ,pos=(GAME_WIDTH-150,GAME_HEIGHT-20),font_size=10,halign='center')
        self.view.add(self._score)
    
    def _bounce(self):
        """Helper function to be used within update. If no bricks are remaining,
        _bounce sets the state to STATE_COMPLETE, removes the ball from the view and
        adds a Congratulatory You Win message to the view.
        
        Otherwise, if the ball touches the bottom, _bounce removes the ball, changes
        the state to STATE_PAUSED, subtracts one life, displays the appropriate message,
        and reserves the ball.
        
        When player has no more lives, _bounce displays a losing message, and gives the player
        option to continue or quit the game. """
        
        if len(self._bricks) == 0:
            self._state = STATE_COMPLETE
            self._message = GLabel(text = 'YOU WIN!!',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
            self.view.add(self._message)
            self.view.remove(self._ball)
        elif self._ball.y <= 0:
            self.view.remove(self._ball)
            self._state = STATE_PAUSED
            self._lives=self._lives-1
            self._paddlecounter = 0
            self._color_counter = 0
            if self._lives ==1:
                self._message = GLabel(text = 'Ball Lost ' + '1' + ' Try Remaining',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
                self.view.add(self._message)
                self._wait_message()
            elif self._lives > 0 and self._lives !=3:
                self._message = GLabel(text = 'Ball Lost ' + `self._lives` + ' Tries Remaining',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
                self.view.add(self._message)
                self._wait_message()
            else:
                self._state = STATE_COMPLETE
                self._try_again()
                self._message = GLabel(text = 'YOU LOSE!!',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
                self.view.add(self._message)
                
    def _pausetouch(self,touch):
        """Helper function to change game state. If user touches
        down on _pause object, state changes to either STATE_FREEZE
        or STATE_ACTIVE depending on its current state and alters
        the text of _pause's GLabel object accordingly.
        
        Precondition: touch is a MotionEvent"""
        if self._state == STATE_ACTIVE and self._pause.collide_point(touch.x,touch.y) and self._pause.text =='Pause':
            self._pause.text='Unpause'
            self._state = STATE_FREEZE
        
        elif self._state ==STATE_FREEZE and self._pause.text == 'Unpause' and self._pause.collide_point(touch.x,touch.y):
            self._state = STATE_ACTIVE
            self._pause.text='Pause'
            
    def _try_again(self):
        """Helper function to display Continue/End text to player when player
        has no more lives. Sets fields _tryn and _tryy to END and CONTINUE
        respectively and adds them to the view when lives run out and state
        is STATE_COMPLETE"""
        
        self._tryn=GLabel(text = 'END',pos=(GAME_WIDTH/2 +50,GAME_HEIGHT/2 -50),font_size=20,halign='center')
        self._tryy=GLabel(text = 'CONTINUE',pos=(GAME_WIDTH/2 -150,GAME_HEIGHT/2 -50),font_size=20,halign='center')
        self.view.add(self._tryn)
        self.view.add(self._tryy)
        
    def _contend(self,touch):
        """Helper function to either continue game or end it when a player has lost.
        If user touches down on _tryy object, state changes to
        STATE_PAUSE, new ball is served, and number of lives is reset.
        Otherwise, if user touches down on _tryn object, game quits. 
        
        Precondition: touch is a MotionEvent"""
        
        if self._state==STATE_COMPLETE and len(self._bricks) != 0:
            if self._tryy.collide_point(touch.x,touch.y):
            
                self._state = STATE_PAUSED
                self._lives=NUMBER_TURNS
                self.view.remove(self._tryn)
                self.view.remove(self._tryy)
                self.view.remove(self._message)
                self._wait_message()
    
            elif self._tryn.collide_point(touch.x,touch.y):
                sys.exit()
        
    def _wait_message(self):
        """Helper function that gives player 3,2,1 countdown till
        ball serve and then serves the ball.
        create_ball changes state to STATE_ACTIVE
        indicating that the ball has been served"""
        
        self.delay(self._wait_3,1)
        self.delay(self._wait_2,2)
        self.delay(self._wait_1,3)
        self.delay(self._create_ball,4)
        
    def _wait_3(self):
        """Helper function to display countdown till ball is served
        (3) Countdown till ball is served
        Removes the current field _message from view.
        Changes _message to '3' and adds that to the view."""
        
        self.view.remove(self._message)
        self._message = GLabel(text = '3',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
        self.view.add(self._message)
        
    def _wait_2(self):
        """Helper function to display countdown till ball is served
        (2) Countdown till ball is served
        Removes the current field _message from view.
        Changes _message to '2' and adds that to the view."""
        
        self.view.remove(self._message)
        self._message = GLabel(text = '2',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
        self.view.add(self._message)
        
    def _wait_1(self):
        """Helper function to display countdown till ball is served
        (1) Countdown till ball is served
        Removes the current field _message from view.
        Changes _message to '1' and adds that to the view."""
        
        self.view.remove(self._message)
        self._message = GLabel(text = '1',pos=(GAME_WIDTH/2 - 50,GAME_HEIGHT/2),font_size=20,halign='center')
        self.view.add(self._message)

    def _get_colliding_object(self):
        """Returns: GObject that has collided with the ball
        
        This method checks the four corners of the ball, one at a 
        time. If one of these points collides with either the paddle 
        or a brick, it stops the checking immediately and returns the 
        object involved in the collision. It returns None if no 
        collision occurred."""
       
        #Check bottom left corner:
        colliding_object = self._check_collision(self._ball.x, self._ball.y)
        if colliding_object <> None:
            return colliding_object
       
        #Check top left corner:
        colliding_object = self._check_collision(self._ball.x, self._ball.top)
        if colliding_object <> None:
            return colliding_object
        
        #Check bottom right corner:
        colliding_object = self._check_collision(self._ball.right, self._ball.y)
        if colliding_object <> None:
            return colliding_object
        
        #Check top right corner:
        colliding_object = self._check_collision(self._ball.right, self._ball.top)
        if colliding_object <> None:
            return colliding_object
        
        return None 
      
    def _check_collision(self, x, y):
        """Checks to see if the point (x,y) is inside of a brick or the paddle
    
        Returns the object the point is currently colliding with, or None,
        if the point is not colliding with another object
        
        Precondition: x and y are float or int within range of
        x and y coordinates determined by window/Game size"""
        
        if self._paddle.collide_point(x,y):
            return self._paddle

        c= len(self._bricks) - 1
        
        while c >= 0:
            if self._bricks[c].collide_point(x,y):                  
                return self._bricks[c]
            c -= 1
        
        return None       
    
    def _ball_collision(self):
        """Handles the redirection of the ball and the playing of sound effects
        when the ball collides with bricks or the paddle.
        
        When the ball collides with a brick or the middle of the padle, its
        y-velocity is simply multiplied by -1. When the ball colides with the
        ends of the paddle (specifially, the leftmost and rightmost eighths of
        the paddle), the balls x- and y-velocities are multiplied by -1.
        
        Also implements a kicker that changes the ball's color and multiplies
        _ball._vx  and _ball._vy by 1.5 every seventh time the ball hits the
        paddle."""
        
        if self._colliding_object == self._paddle and self._ball._vy < 0:
            self._paddlecounter = self._paddlecounter + 1
            if self._paddlecounter % 7 ==0:
                self._ball._vx = 1.5 * self._ball._vx
                self._ball._vy = 1.5 * self._ball._vy
                
                i = 0
                while i < 5:
                    if self._color_counter % 5 == i:
                        self._ball.fillcolor = BRICK_COLOR[i]
                        self._ball.linecolor = BRICK_COLOR[i]
                    i += 1
                self._color_counter += 1
            
            #Reverse the ball velocity's y-component, and, if the ball
            #collides with the left or right eigth of the paddle, the ball's
            #x-velocity:
            self._ball._vy = -self._ball._vy
            if (self._ball.x + BALL_DIAMETER/2 <
                self._paddle.x + self._paddle.width/8
                or self._ball.right - BALL_DIAMETER/2 >
                self._paddle.right - self._paddle.width/8):
                
                self._ball._vx = -self._ball._vx
        elif (self._colliding_object <> self._paddle and
                  isinstance(self._colliding_object, GRectangle)):
            self._ball._vy = -self._ball._vy
            self.view.remove(self._colliding_object)
            self._bricks.remove(self._colliding_object)
            
    def _play_sounds(self):
        """Helper function for update that plays sounds when the ball colides
        with certain objects.
        
        When the ball hits the paddle, a bouncing sound will be played,
        and when the ball hits a brick, the sound of plates/cups/etc.
        shattering will play. Otherwise, no sounds are played."""
        
        if self._soundplay == SOUND_ON:
            if self._colliding_object == self._paddle and self._ball._vy < 0:
                bounceSound.play()
            elif (self._colliding_object <> self._paddle and
                  isinstance(self._colliding_object, GRectangle)):
                self._soundcounter=self._soundcounter+1
                if self._soundcounter % 4 == 0:
                    bounceSound5.play()
                elif self._soundcounter % 4 ==1:
                    bounceSound2.play()
                elif self._soundcounter % 4 ==2:
                    bounceSound3.play()
                elif self._soundcounter % 4 ==3:
                    bounceSound4.play()  
        

 
class Ball(GEllipse):
    """Instance is a game ball.

    We extends GEllipse because a ball does not just have a position; it
    also has a velocity.  You should add a constructor to initialize the
    ball, as well as one to move it.

    Note: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above."""
    # FIELDS.  You may wish to add properties for them, but that is optional.

    # Velocity in x direction.  A number (int or float)
    _vx = 0.0
    # Velocity in y direction.  A number (int or float)
    _vy = 0.0

    # ADD MORE FIELDS (INCLUDE INVARIANTS) AS NECESSARY

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    
    
    def __init__(self):
        """**Constructor for Ball
        
        Creates Ball object with width=BALL_DIAMETER,
        height = BALL_DIAMETER, position in center of screen.
        
        Sets ._vy to -5.0 and sets ._vx to random number between -5.0 and -1.0
        or between 1.0 and 5.0 """
        
        super(Ball,self).__init__(width= BALL_DIAMETER,height=BALL_DIAMETER,pos =(GAME_WIDTH/2,GAME_HEIGHT/2))
        self._vy = -5.0
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])

    def move_ball(self):
        """ Changes the x position of the ball by ._vx and the
        y position by ._vy. If position of x <= 0, ._vx is reversed
        If position of x + BALL_DIAMETER > = GAME_WIDTH, vx is reversed.
        If y + BALL_DIAMETER >= GAME_HEIGHT ._vy is reversed."""
        
        self.pos = (self.pos[0] + self._vx, self.pos[1] + self._vy)
        if self.x <= 0:
            self._vx = - self._vx
        if self.y + BALL_DIAMETER >= GAME_HEIGHT:
            self._vy = - self._vy
        if self.x+BALL_DIAMETER >= GAME_WIDTH:
            self._vx = -self._vx

