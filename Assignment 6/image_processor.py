# image_processor.py
# Quinn Beightol (qeb2)
# 11/16/2012
from image_array import ImageArray
"""Secondary Controller module for Imager Application

This module provides all of the image processing operations that
are called whenever you press a button.  All other controller
functionality (loading files, etc.) is provided in imager.py"""

import math
# GLOBAL CONSTANTS
GRAY = 0
SEPIA = 1


class ImageProcessor(object):
    """Instance is a collection of image transforms"""
    # Fields
    _current  = None # Current image being manipulated
    _original = None # Original image, may not be changed.

    # Immutable Attributes
    @property
    def original(self):
        """The original state of the image in this processor.

        *This attribute is set by the constructor and may not be altered*"""
        return self._original

    # Mutable Attributes
    @property
    def current(self):
        """The original state of the image in this processor.

        **Invariant**: Must be an ImageArray"""
        return self._current

    @current.setter
    def current(self,value):
        assert isinstance(value,ImageArray), `value`+' is not an ImageArray'
        self._current = value

    # Built-in Methods

    def __init__(self, image_array):
        """**Constructor**: Create an ImageProcessor for the given image.

            :param image: The image to process.
            **Precondition**: an ImageArray object

        Attribute `original` is a direct reference to `image_array`.
        However, attribute `current` is a copy of that ImageArray."""
        self._original = image_array
        self._current  = ImageArray.Copy(image_array)

    def restore(self):
        """Restore the original image"""
        self._current = ImageArray.Copy(self.original)

    def invert(self):
        """Invert the current image, replacing each element with its color
        complement"""
        n = 0
        # Invariant: pixels 0..n-1 have been inverted in self.current
        while n < self.current.len:
            rgb = self.current.getFlatPixel(n)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            self.current.setFlatPixel(n, rgb)
            n = n + 1 # Remember to increment

    def transpose(self):
        """Transpose the current image

        Follow this plan:

            Create a new ImageArray ia, which has no data (it is an empty
            image), but which has the number of rows and columns swapped
            from their current values in self.current

            Store the transpose of self.current in ia, using self.current's
            `getPixel` function and ia's `setPixel` function.

            Assign ia to self.current.

        The transposed image will be drawn on the screen immediately afterwards."""
        ia = ImageArray(rows=self.current.cols,cols=self.current.rows)
        r = 0
        # Invariant: rows 0..r-1 have been copied to ia[.., 0..r-1]
        while r < ia.rows:
            c = 0
            # Invariant: elements [r,0..c-1] have been copied to ia[0..c-1, r]
            while c < ia.cols:
                ia.setPixel(r, c, self.current.getPixel(c, r))
                c = c + 1 # Remember to increment
            r = r + 1 # Remember to increment

        # Replace the image
        self.current = ia

    def horizReflect(self):
        """ Reflect the current image around a vertical line through
        the middle of the image."""
        h = 0
        k = self.current.cols-1
        # Invariant: cols 0..h-1 and k+1.. have been swapped
        while h < k:
            r = 0
            # Invariant: pixels 0..r-1 of cols h and k have been swapped
            while r < self.current.rows:
                self.current.swapPixels(r, h, r, k)
                r = r + 1 # Remember to increment
            # Must change two variables to satisfy invariant
            h = h + 1 # Move h forward
            k = k - 1 # Move k backward

    def rotateLeft(self):
        """Rotate the image left via a transpose, followed by a vertical reflection."""
        self.transpose()
        self.vertReflect()

    def rotateRight(self):
        """Rotate the image right via a transpose, followed by a horizontal reflection."""
        self.transpose()
        self.horizReflect()

    # Student defined
    def vertReflect(self):
        """ Reflect the current image around a horizontal line through
        the middle of the image."""
        top_row = 0
        bottom_row = self.current.rows-1
        
        #invariant: rows O..top_row-1 and bottom_row+1.. have been swapped
        while top_row < bottom_row:
            column = 0
            while column < self.current.cols:
                # invariant: pixels 0..column - 1 of top_row and bottom_row
                # have been swapped
                self.current.swapPixels(top_row, column, bottom_row, column)
                column += 1
            # post condition: all pixels (i.e. pixels 0..self.current,cols-1)
            # in top_row and bottom_row have been swapped
            
            top_row += 1
            bottom_row -= 1
        # post condition: rows 0..(self.current.rows/2-1) have been swapped
        # with rows self.current.rows/2..self.current-1

    def jail(self):
        """Put jail bars on the current image:

        Put 3-pixel-wide horizontal bars across top and bottom,

        Put 4-pixel vertical bars down left and right, and

        Put n 4-pixel vertical bars inside, where n is (number of columns - 8) / 50.

        The n+2 vertical bars should be as evenly spaced as possible."""
        bar_color = (255, 0, 0) #red by default
        n = int(round((self.current.cols - 8) / 50))
        bar_distance = (float(self.current.cols-4)) / ((n + 1))
        # bar_distance is calculated so that (n+1)*bar_distance
        # = self.current.cols-4, where the second half of
        # the equation represents the starting column for the rightmost
        # vertical bar. bar_distance does NOT represent the actual distance
        # between the ends of two bars; that would be bar_distance - 4
        
        # Draw horizontal bars:
        self._drawHBar(0, bar_color)
        self._drawHBar(self.current.rows - 3, bar_color)
        
        # Draw vertical bars:
        current_bar_number = 0
        
        # inv: bars 0..current_bar_number-1 have been drawn
        while current_bar_number < n+2:
            self._drawVBar(int(round(current_bar_number*bar_distance)),
                           bar_color)
            current_bar_number += 1
        # post condition: bars 0..n+1 have been drawn

    def _drawHBar(self, row, pixel):
        """Helper function for jail.

            :param row: The start of the row to draw the bar
            **Precondition**: 0 <= row  and  row+2 < self.current.rows an int

            :param pixel: The pixel color to use
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        Draw a horizontal 3-pixel-wide bar at row `row` of the current
        image. So the bar is at rows row, row+1, and row+2. The bar
        uses the color given by the given rgb components."""
        col = 0
        # Invariant: pixels self.current[row..row+2][0..col-1] are color pixel
        while col < self.current.cols:
            self.current.setPixel(row,   col, pixel)
            self.current.setPixel(row+1, col, pixel)
            self.current.setPixel(row+2, col, pixel)
            col = col + 1 # Remember to increment
    
    def _drawVBar(self, column, pixel):
        """Helper function for jail.

            :param column: The start of the column to draw the bar
            **Precondition**: 0 <= column  and  column+3 < self.current.cols
            an int

            :param pixel: The pixel color to use
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        Draw a vertical 4-pixel-long bar at column `column` of the current
        image. So the bar is at columns column, column+1, column+2, and
        column+3. The bar uses the color given by the given rgb components."""
        c = column
        
        while c < column + 4:
            r = 0
            
            while r < self.current.rows:
                self.current.setPixel(r, c, pixel)
                r += 1
            
            c += 1

    def monochromify(self, color):
        """Convert the current image to monochrome according to parameter color.

            :param color: Monochrome color choice
            **Precondition**: an int equal to either the global constant `GRAY`
            or the global constant `SEPIA`

        If color is `GRAY`, then remove all color from the image by setting the
        three color components of each pixel to (an int corresponding to) that
        pixel's overall brightness, defined as
        0.3 * red + 0.6 * green + 0.1 * blue.

        If color is `SEPIA`, make the same computation but set green to
        int(0.6 * brightness) and blue to int(0.4 * brightness)."""
        assert color == GRAY or color == SEPIA, 'invalid color parameter'
        
        if color == GRAY:
            r = 0
            
            while r < self.current.rows:
                c = 0
                
                while c < self.current.cols:
                    rgb = self.current.getPixel(r, c)
                    brightness = 0.3*rgb[0] + 0.6*rgb[1] + 0.1*rgb[2]
                    new_rgb = (int(brightness), int(brightness),
                               int(brightness))
                    self.current.setPixel(r,c, new_rgb)
                    c += 1
                
                r += 1
        else:
            r = 0
            
            while r < self.current.rows:
                c = 0
                
                while c < self.current.cols:
                    rgb = self.current.getPixel(r, c)
                    brightness = 0.3*rgb[0] + 0.6*rgb[1] + 0.1*rgb[2]
                    new_rgb = (int(brightness), int(0.6*brightness),
                              int(0.4*brightness))
                    self.current.setPixel(r,c, new_rgb)
                    c += 1
                
                r += 1

    def vignette(self):
        """Simulate vignetting (corner darkening) characteristic of antique lenses.

        Darken each pixel in the image by the factor

            (d / hfD)^2

        where d is the distance from the pixel to the center of the image and
        hfD (for half diagonal) is the distance from the center of the image
        to any of the corners."""
        rows = float(self.current.rows) # Computation on floats, not ints
        cols = float(self.current.cols) # Computation on floats, not ints
        # Remember that pixel values must, in the end, be 3-tuples of ints
        
        r = 0
            
        while r < self.current.rows:
            c = 0
            
            while c < self.current.cols:
                rgb = self.current.getPixel(r, c)
                d = math.sqrt((r-(self.current.rows/2))**2 +
                    (c-(self.current.cols)/2)**2)
                h = math.sqrt((self.current.rows/2)**2 +
                    (self.current.cols/2)**2)
                new_rgb = (int((1-d**2/h**2)*rgb[0]), int((1-d**2/h**2)*rgb[1]),
                           int((1-d**2/h**2)*rgb[2]))
                self.current.setPixel(r,c, new_rgb)
                c += 1
                
            r += 1

    def decode(self, p):
        """**Return**: the number n that is hidden in pixel p of the current image.

            :param p: a pixel position
            **Precondition**: pixel position is valid
            (i.e. 0 <= p < self.current.len)

        This function assumes that n is a 3-digit number encoded as the
        last digit in each color channel (i.e., red, green and blue)."""
        rgb = self.current.getFlatPixel(p)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return (red % 10) * 100  +  (green % 10) * 10  +  blue % 10

    def encode(self, n, p):
        """Encode integer n in pixel number p of the current image.

            :param n: a number to hide
            **Precondition**: an int with 0 <= n < 1000

            :param p: a pixel position
            **Precondition**: pixel position is valid
            (i.e. 0 <= p < self.current.len)

        This function encodes a three digit number by adding (or otherwise
        changing) a single digit to each color channel (i.e., red, green and
        blue)."""
        old_pixel = self.current.getFlatPixel(p)
        old_red   = old_pixel[0]
        old_green = old_pixel[1]
        old_blue  = old_pixel[2]
        
        #Compute new red channel:
        first_digit = int(n/100)
        
        new_red = (old_red/10)*10 + first_digit
        
        if new_red - old_red > 5:       # Ensures that the difference between
            new_red -= 10               # new_red and old_red is never greater
                                        # than 5, preserving color quality
        
        if new_red > 255:
            new_red -= 10
        elif new_red < 0:
            new_red += 10
        
        #Compute new green channel:
        second_digit = int((n-100*first_digit)/10)
        
        new_green = (old_green/10)*10 + second_digit
        
        if new_green - old_green > 5: 
            new_green -= 10               
        
        if new_green > 255:
            new_green -= 10
        elif new_green < 0:
            new_green += 10
            
        #Compute new blue channel:
        third_digit = n-100*first_digit-10*second_digit
        
        new_blue = (old_blue/10)*10 + third_digit
        
        if new_blue - old_blue > 5: 
            new_blue -= 10               
        
        if new_blue > 255:
            new_blue -= 10
        elif new_blue < 0:
            new_blue += 10
        
        #Change pixel
        new_pixel = (new_red, new_green, new_blue)
        self.current.setFlatPixel(p, new_pixel)

    def hide(self, text):
        """Hide message text in this image, using the ASCII representation of
        text's characters.

        **Return**: True if message hiding possible, and False if not.

            :param text: a message to hide
            **Precondition**: a string

        If m has more than 999999 characters or the picture does not have enough
        pixels, return False without storing the message."""
        label_length = len('MSG_' + `len(text)` + ':')
        if len(text) > 999999 or label_length > self.current.len:
            return False
        else:
            self._label(len(text))
            i = 0
            while i < len(text):
                self.encode(ord(text[i]), label_length+i)
                i += 1
            return True
    
    def _label(self, l):
        """Changes the first few pixels of an image to indicate a hidden message
        
        The first 5 + (number of digits in l) are modified so that decode, when
        run with these pixels as arguments, yields a string of characters in
        the format "MSG_<l>:" where <l> is the length of the message. For
        example of message of length 100 would modify the image so that the
        first 8 pixels of the message would create the string "MSG_100:" when
        fed through decode.
        
        Precondition: l is an int < 999999 and (the number of digits is l) +
        5 + l <= the number of pixels in the image"""
        # Since this method is called only by hide, and hide guarantees that
        # the preconditions are met, there is no need to check preconditions
        label = 'MSG_' + `l` + ':'
        i = 0
        
        while i < len(label):
            self.encode(ord(label[i]), i)
            i += 1
    
    def reveal(self):
        """**Return**: The secret message from the image array. Return
        None if no message detected."""
        # Check for message:
        message_length = ''
        i = 0
        label = ''
        
        while i < 4:
            a = self.decode(i)
            if a < 0 or a > 255:
                return None
            label += chr(a)
            if label <> 'MSG_'[0:i+1]:
                return None
            i += 1
        
        while self.decode(i) <> ord(':'):
            if self.decode(i) < 0 or self.decode(i) > 255:
                print self.decode(i)
                return None
            elif self.decode(i) > ord('9') or self.decode(i) < ord('0'):
                return None
            elif i > 11:    # The maximum valid label length is 11; any label
                return None # label longer than this probably comes from
                            # bad data
            message_length += str(chr(self.decode(i)))
            i += 1
        
        i = i+1
        label_length = i
        decoded_message = ''
        message_length = int(message_length)
        
        if message_length > self.current.len - label_length:
            return None
        
        while i < label_length + message_length:
            if self.decode(i) < 0 or self.decode(i) > 255:
                return None
            decoded_message += chr(self.decode(i))
            i += 1
        return decoded_message

    def _pad3(self, n):
        """Returns a string value of n padded with 0s to be three characters.

            :param n: number to convert to string
            **Precondition**: a int, 0 <= n <= 999

        This method does not assert its preconditions."""
        if n < 10:
            return '00'+str(n)
        elif n < 100:
            return '0'+str(n)
        return str(n)

    def _pixel2str(self, pixel):
        """Helper function for getPixels to turn a pixel into a string.

            :param pixel: The pixel value
            **Precondition**: a 3-element tuple (r,g,b) where each
            value is 0..255

        Pads all colors with 0s with to make them three digits.  This makes
        them easier to 'line up'.

        This method does not assert its precondition."""
        return self._pad3(pixel[0])+':'+self._pad3(pixel[1])+':'+self._pad3(pixel[2])

    def getPixels(self, n):
        """**Return**: String that contains the first n pixels of the current image

            :param n: number of pixels to get
            **Precondition**: a positive int < self.current.len

        The pixels are shown 5 to a line, with annotation (i.e. something at
        the beginning to say what the string contains).

        To begin a new line, put an '\n' in the string. For example, type this
        at the Python interpreter and see what happens: 'ABCDE\nEFGH'.
        Use the function _pixel2str() to get the string representation of
        a pixel tuple."""
        pixel_string = ''
        i = 0
        
        # invariant: pixels 0..i-1 have been added to pixel_string. Also, the
        # final character of pixel string should be a ' ', or, if i%5 = 0, a
        # newline character. 
        while i < n:
            current_pixel = self.current.getFlatPixel(i)
            pixel_string = pixel_string + self._pixel2str(current_pixel) + ' '
            if (i + 1) % 5 == 0:
                pixel_string += '\n'
            i += 1
        return pixel_string
        # post condition: pixel_string contains pixel 0..n-1 of self.current

    # Note: You do not have to write this procedure, and if you do write it, it
    # will not be graded. But it is instructive if you have the time!
    def fuzzify(self):
        """Change the current image so that every pixel that is not on one of
        the four edges of the image is replaced with the average of its
        current value and the current values of its eight neighboring pixels.

        When implementing this function:

            FIRST, make a copy of the image.  Use the function ImageArray.Copy()

            THEN transform the copy using the values in the current image.

            THEN copy the entire transformed copy into the current image.

        Thus, the average will be the average of values in the "original"
        current image, NOT of values that have already been fuzzified."""
        # IMPLEMENT ME
        pass
    
