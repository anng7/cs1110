# geometry.py
# Walker M. White (wmw2)
# October 13, 2012
import math
"""Module implementing affine transforms.

This is the primary module supporting geometric transformations in Assignment 5.
It contains a single class: Transform.

It depends heavily on the student implementation of a5.py. It attempts
to be somewhat robust, adjusting to missing or incomplete implementations
of the various classes in a5.py"""

# Check to see if the module matrix exists
try:
    import a5
    _loaded = True
except:
    _loaded = False


#### PRIVATE HELPER FUNCTIONS ####

# Test to see if Vector is defined and its constructor doesn't cause an exception.
def _vector_loaded():
    try:
        x = a5.Vector(1.0,2.0)
        return True
    except:
        pass
    return False


# Test to see if Matrix is defined and its constructor doesn't cause an exception.
def _matrix_loaded():
    try:
        x = a5.Matrix(1.0,0.0,0.0,1.0)
        return True
    except:
        pass
    return False


# Returns True if obj is for type Matrix.
# Returns False if obj is of different type or Matrix undefined.
def _check_matrix_type(obj):
    try:
        return type(obj) == a5.Matrix
    except:
        pass
    return False


# Returns True if obj is for type Vector.
# Returns False if obj is of different type or Vector undefined.
def _check_vector_type(obj):
    try:
        return type(obj) == a5.Vector
    except:
        pass
    return false


#### PRIMARY CLASS ####


class Transform(object):
    """Instances are affine transforms (matrix + offset vector).
    
    A transform represents a mathematical function ``T(x)`` which takes
    a vector and produces a new vector.  The function is defined
    ``T(x) = A*x + b`` where A is a matrix and b is a vector.
    
    The matrix ``A`` represents a *linear* transformation such as scaling,
    rotation, or reflection.  The vector ``b`` is the translation component.
    
    To compute the value ``T(x)``, use the method ``transform``."""
    _matrix = None # Linear component of transform
    _vector = None # Translation component of transform
    
    @property
    def matrix(self):
        """Linear component of transform. Stored as a Matrix object (or None).
        
        *This attribute may not be altered after the object is constructed.*"""
        return self._matrix
    
    @property
    def vector(self):
        """Translation component of transform. Stored as a Vector object (or None).
        
        *This attribute may not be altered after the object is constructed.*"""
        return self._vector
    
    @classmethod
    def Identity(cls):
        """**Constructor** (alternate): Returns an Identity transform.
        
        Both the matrix and vector component are None, indicating that
        the method ``transform`` should use the default values."""
        self = cls()
        return self
    
    @classmethod
    def Rotation(cls,angle):
        """**Constructor** (alternate): Returns a Rotation transform for the given angle.

            :param angle: the angle of rotation
            **Precondition**: a number (float or int).
        
        The matrix is a rotation Matrix, while the vector component is None. The
        method ``transform`` will use the default value of translation.
        
        Should this constructor fail (because of an incomplement implementation
        in module ``a5``, it will return an Identity transform."""
        try:
            matrix = a5.Matrix(math.cos(angle),-math.sin(angle),
                               math.sin(angle),math.cos(angle))
            self = cls(matrix)
            return self
        except:
            pass
        
        return cls.Identity()
    
    @classmethod
    def Reflection(cls,x=1,y=0):
        """**Constructor** (alternate): Returns a Reflection transform about the given vector.

            :param x: the x coordinate of the vector to reflect about
            **Precondition**: a number (float or int).

            :param y: the y coordinate of the vector to reflect about
            **Precondition**: a number (float or int).
        
        The matrix is a reflection Matrix, while the vector component is None. The
        method ``transform`` will use the default value of translation.
        
        Should this constructor fail (because of an incomplement implementation
        in module ``a5``, it will return an Identity transform."""
        try:
            norm   = x*x+y*y # dot product
            matrix = a5.Matrix((x*x-y*y)/norm,
                               (2*x*y)/norm,
                               (2*x*y)/norm,
                               (y*y-x*x)/norm)
            self = cls(matrix)
            return self
        except:
            pass
        
        return cls.Identity()
    
    @classmethod
    def Projection(cls,x=1,y=0):
        """**Constructor** (alternate): Returns a Projection transform on to the given vector.

            :param x: the x coordinate of the vector to project on
            **Precondition**: a number (float or int).

            :param y: the y coordinate of the vector to project on
            **Precondition**: a number (float or int).
        
        The matrix is a projection Matrix, while the vector component is None. The
        method ``transform`` will use the default value of translation.
        
        Should this constructor fail (because of an incomplement implementation
        in module ``a5``, it will return an Identity transform."""
        try:
            norm   = x*x+y*y # dot product
            matrix = a5.Matrix(x*x/norm,x*y/norm,
                               x*y/norm,y*y/norm)
            self = cls(matrix)
            return self
        except:
            pass
        
        return cls.Identity()
    
    @classmethod
    def Scale(cls,sx,sy=None):
        """**Constructor** (alternate): Returns a Scale transform for the given magnification.

            :param x: the magnification in the x direction
            **Precondition**: a number (float or int).

            :param y: the magnification in the y direction
            **Precondition**: a number (float or int).
        
        The matrix is a scaling Matrix, while the vector component is None. The
        method ``transform`` will use the default value of translation.
        
        Should this constructor fail (because of an incomplement implementation
        in module ``a5``, it will return an Identity transform."""
        try:
            sy = sx if sy is None else sy
            matrix = a5.Matrix(sx,0,0,sy)
            self = cls(matrix)
            return self
        except:
            pass
        
        return cls.Identity()
    
    @classmethod
    def ShearX(cls,k):
        """**Constructor** (alternate): Returns a Shear transform along the x-axis.

            :param k: the shear amount
            **Precondition**: a number (float or int).

        The matrix is a shear Matrix, while the vector component is None. The
        method ``transform`` will use the default value of rotation.
        
        Should this constructor fail (because of an incomplement implementation
        in module ``a5``, it will return an Identity transform."""
        try:
            matrix = a5.Matrix(1,k,0,1)
            self = cls(matrix)
            return self
        except:
            pass
        
        return cls.Identity()

    @classmethod
    def ShearY(cls,k):
        """**Constructor** (alternate): Returns a Shear transform along the y-axis.

            :param k: the shear amount
            **Precondition**: a number (float or int).

        The matrix is a shear Matrix, while the vector component is None. The
        method ``transform`` will use the default value of translation.
        
        Should this constructor fail (because of an incomplement implementation
        in module ``a5``, it will return an Identity transform."""
        try:
            matrix = a5.Matrix(1,0,k,1)
            self = cls(matrix)
            return self
        except:
            pass
        
        return cls.Identity()
    
    @classmethod
    def Translation(cls,x=0,y=0):
        """**Constructor** (alternate): Returns a Translation transform by the given amount.

            :param x: amount to translate in the x direction
            **Precondition**: a number (float or int).

            :param y: amount to translate in the y direction
            **Precondition**: a number (float or int).
        
        The matrix is None, which means that the Transform will use the identity
        for the matrix part.  The vector is the amount of translation.
        
        Should this constructor fail (because of an incomplement implementation
        in module ``a5``, it will return an Identity transform."""
        try:
            if x != 0 or y != 0:
                vector = a5.Vector(x,y)
            else:
                vector = None
        
            self = cls(None,vector)
            return self
        except:
            pass
        
        return cls.Identity()
    
    def __init__(self,matrix=None,vector=None):
        """**Constructor**: Returns a transform with the given matrix and offset vector.
        
            :param matrix: the Matrix component
            **Precondition**: either a Matrix object or None.

            :param vector: the Vector component
            **Precondition**: either a Vector object or None.
        
        Either matrix and/or vector may be None (and these are the default values).
        If matrix is None, the transform will use the identity matrix.  If vector
        is None, the transform will use the vector (0,0) as the translation."""
        if not _loaded:
            return
        
        assert (matrix is None or _check_matrix_type(matrix)), 'argument '+`matrix`+' has unsupported type'
        assert (vector is None or _check_vector_type(vector)), 'argument '+`vector`+' has unsupported type'
        self._matrix = matrix
        self._vector = vector
    
    def __str__(self):
        """**Returns**: A string representation of this transform.
        
        Format is either Ax+b or Ax, where A is the matrix component."""
        # Compute the matrix representation
        if self.matrix is None:
            lstring = '[[1.0, 0.0], [[0.0, 1.0]]'
        else:
            lstring = ('[['+str(self.matrix.a)+', '+str(self.matrix.b)+'], '+
                       '['+str(self.matrix.c)+', '+str(self.matrix.d)+']]')
            
        # Compute the string representation
        if self.vector is None:
            ostring = ''
        else:
            ostring = ' + ('+str(self.vector.x)+', '+str(self.vector.y)+')'
        
        # Glue results together.
        return lstring+'x'+ostring
    
    def __repr__(self):
        """**Returns**: A unambiguous representation of this transform.
        
        Simply attaches the class name to the ``__str__`` representation."""
        return `self.__class__`+str(self)
    
    def __eq__(self,other):
        """**Returns**: True if other is a Transform with same contents as this one; False otherwise"""
        return (isinstance(other, Transform) and
                self.matrix == other.matrix and self.vector == other.vector)
    
    def __ne__(self,other):
        """**Returns**: False if other is a Transform with same contents as this one; True otherwise"""
        return not self == other
    
    def transform(self,position):
        """**Returns**: Function T(x) applied to position.
        
        If Vector in the module ``a5`` is not yet implemented, then this
        function returns the tuple (0,0).
        
        If ``matrix`` is None, or the method ``__mul__`` is not implemented,
        the position will not be multiplied by anything.  Hence it will be
        the same as if ``matrix`` were the identity. 
        
        If ``vector`` is None, or the method ``__add__`` is not implemented,
        the position will not be translated.  Hence it will be
        the same as if ``vector`` were (0,0). 
        
        **Precondition**: ``position`` is either a Vector or a tuple with two elements.
        The return type of this function is the same type as `position``."""
        if not (_loaded and _vector_loaded()):
            return (0,0)
        
        assert (type(position) == tuple or type(position) == a5.Vector), 'argument '+`position`+' does not represent a position'
        result = position
        if (type(position) == tuple):
            result = a5.Vector(position[0],position[1])
        
        try:
            if not (self.matrix is None):
                result = self.matrix*result
        except:
            pass
        
        try:
            if not (self.vector is None):
                result = result+self.vector
        except:
            pass
        
        if (type(position) == tuple):
           return (result.x,result.y)
        
        return result
    
    def compose(self,other):
        """**Returns**: The composition T(S(x)) where S(x) is the transform given by ``other``.
        
        If the method ``__mul__`` is not fully implemented in Matrix, this method
        returns a copy of this transform.
        
        **Precondition**: other is a Transform**"""
        matrix = self.matrix
        vector = self.vector
        translate = other.vector
        try:
            if self.matrix is None:
                matrix = other.matrix
            elif not (other.matrix is None):
                matrix = self.matrix*other.matrix
            
            if not (self.matrix is None or translate is None):
                translate = self.matrix*translate
            
            if self.vector is None:
                vector = translate
            elif not (translate is None):
                vector = self.vector+translate
        except:
            pass
        
        return Transform(matrix,vector)
