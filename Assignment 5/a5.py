# a5.py
# Quinn Beightol (qeb2)
# 10/30/2012
"""Primary module for Assignment 5.

This module contains the Vector and Matrix classes to be implemented as
part of this assignment."""
import math

class Vector(object):
    """Instances are a vector in 2-dimensional space.
    
    The vector has two attributes: x and y. It represents a vector of the
    form (x,y). It is a mutable object, so the attributes values can be
    altered at any time."""
    _x = 0.0 #x-coordinate field
    _y = 0.0 #y-coordinate field
    
    @property
    def x(self):
        """x-coordinate; value is a number"""
        return self._x
    
    @x.setter
    def x(self, value):
        assert type(value) == float or type(value) == int, (value+' is not a '
                                                            +'valid x-component'
                                                            +'; the argument '
                                                            +'must be a number')
        if type(value) == int:
            self._x = float(value)
        else:
            self._x = value
    
    @property
    def y(self):
        """y-coordinate; value is a number"""
        return self._y
    
    @y.setter
    def y(self, value):
        assert type(value) == float or type(value) == int, (value+' is not a '
                                                            +'valid y-component'
                                                            +'; the argument '
                                                            +'must be a number')
        if type(value) == int:
            self._y = float(value)
        else:
            self._y = value
    
    def __init__(self,x=0.0,y=0.0):
        """Constructor: Creates a new Vector (x, y).
        
        The x and y values are 0.0 by default, unless otherwise specified.
        
        Precondition: x and y are numbers (either an int or float)"""
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Returns: a new Vector that is the sum of self and other.
        
        This method should not alter the contents of either self or other.
        
        Precondition: other is a Vector obect."""
        assert isinstance(other, Vector), (other+' is not a vector; only '
                                           +'vectors can be added to other '
                                           +'vectors')
        
        return Vector(self.x + other.x, self.y + other.y)


class Matrix(object):
    """Instances are 2x2 matrices.
    
    The matrix has three attributes: a, b, c, and d. It represents a matrix
    of the form::
    
        a    b
        c    d
        
    It is a *immutable* object, so the attributes values cannot be altered
    after the object is constructed."""
    _a = 1.0
    _b = 0.0
    _c = 0.0
    _d = 1.0
    
    @property
    def a(self):
        """top-left value of the matrix; value is a number"""
        return self._a
    
    @property
    def b(self):
        """top-right value of the matrix; value is a number"""
        return self._b
    
    @property
    def c(self):
        """bottom-left value of the matrix; value is a number"""
        return self._c
    
    @property
    def d(self):
        """bottom-right value of the matrix; value is a number"""
        return self._d
    
    def __init__(self,a=1.0,b=0.0,c=0.0,d=1.0):
        """Constructor: Creates a new Matrix [[a,b], [c,d]]
        
        By default, this constructor makes the identity matrix. Hence the
        default values of a and d are 1.0, and the default values of b and d
        are 1.0, unless otherwise specified.
        
        Precondition: a, b, c, and d are numbers (either an int or a float)."""
        assert type(a) == float or type(a) == int, (a+' is not a valid matrix '
                                                    +'element; the arguments '
                                                    +'must be a number')
        assert type(b) == float or type(b) == int, (b+' is not a valid matrix '
                                                    +'element; the arguments '
                                                    +'must be a number')
        assert type(c) == float or type(c) == int, (c+' is not a valid matrix '
                                                    +'element; the arguments '
                                                    +'must be a number')
        assert type(d) == float or type(d) == int, (d+' is not a valid matrix '
                                                    +'element; the arguments '
                                                    +'must be a number')
        
        self._a = float(a)
        self._b = float(b)
        self._c = float(c)
        self._d = float(d)
    
    def __mul__(self, other):
        """Returns: A new value which is the multiple of this matrix and other
        
        If other is a Vector, the result is a Vector using standard Matrix *
        Vector multiplication.
        
        If other is a Matrix, the result is a matrix using matrix
        multiplication. We assume that self is the matrix on the left and other
        is on the right.
        
        Neither self nor other are modified.
        
        Precondition: other is either a Matrix or a Vector"""
        assert (isinstance(other, Matrix) or
                isinstance(other, Vector)), ('A matrix cannot be multiplied by '
                                             +other+'; argument must be a '
                                             +'Matrix or Vector')
        
        if isinstance(other, Vector):
            x = self.a * other.x + self.b * other.y
            y = self.c * other.x + self.d * other.y
            return Vector(x,y)
        
        if isinstance(other, Matrix):
            a = self.a * other.a + self.b * other.c
            b = self.a * other.b + self.b * other.d
            c = self.c * other.a + self.d * other.c
            d = self.c * other.b + self.d * other.d
            return Matrix(a,b,c,d)   