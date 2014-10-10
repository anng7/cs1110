# a5test.py
# Quinn Beightol
# 10/30/2012
"""Unit Test for Assignment A5"""
import cunittest
import a5

def test_vector_constructor():
    """Tests the constructor for vector objects"""
    #Test default values of the vector constructor:
    v = a5.Vector()
    cunittest.assert_floats_equal(0.0, v.x)
    cunittest.assert_floats_equal(0.0, v.y)
    
    #Test constructro when both arguments are floats
    v = a5.Vector(3.14, 2.72)
    cunittest.assert_floats_equal(3.14, v.x)       
    cunittest.assert_floats_equal(2.72, v.y)
    
    #Test that the constructor (setters, technically) converts ints to floats:
    v = a5.Vector(1,1.5)
    cunittest.assert_floats_equal(1.0, v.x)
    cunittest.assert_floats_equal(1.5, v.y)
    
    v = a5.Vector(.1,42)
    cunittest.assert_floats_equal(.1, v.x)
    cunittest.assert_floats_equal(42.0, v.y)
    
    v = a5.Vector(3,4)
    cunittest.assert_floats_equal(3.0, v.x)
    cunittest.assert_floats_equal(4.0, v.y)


def test_vector_addition():
    """Tests addition between vectors"""
    perfect = a5.Vector(6,28)
    numbers = a5.Vector(496, 8128)
    v = perfect + numbers 
    cunittest.assert_floats_equal(502.0, v.x)
    cunittest.assert_floats_equal(8156.0, v.y)
    
    a = a5.Vector(8.08, 0.7734)
    b = a5.Vector(-8.08, -0.7734)
    v = a + b
    cunittest.assert_floats_equal(0.0, v.x)
    cunittest.assert_floats_equal(0.0, v.y)
    
    a = a5.Vector(1.0, 1.0)
    b = a5.Vector(0.0, 0.0)
    v = a + b
    cunittest.assert_floats_equal(1.0, v.x)
    cunittest.assert_floats_equal(1.0, v.y)


def test_matrix_constructor():
    """Tests the constructor for matrices"""
    #Test default values for matrices:
    m = a5.Matrix()
    cunittest.assert_floats_equal(1.0, m.a)
    cunittest.assert_floats_equal(0.0, m.b)
    cunittest.assert_floats_equal(0.0, m.c)
    cunittest.assert_floats_equal(1.0, m.d)
    
    #Test matrix constructor with float arguments:
    m = a5.Matrix(1.23, 2.34, 3.45, 4.56)
    cunittest.assert_floats_equal(1.23, m.a)
    cunittest.assert_floats_equal(2.34, m.b)
    cunittest.assert_floats_equal(3.45, m.c)
    cunittest.assert_floats_equal(4.56, m.d)
    
    #Test matrix constructor with int arguments
    # (ints should be converted to floats)
    m = a5.Matrix(1,2,3,4)
    cunittest.assert_floats_equal(1.0, m.a)
    cunittest.assert_floats_equal(2.0, m.b)
    cunittest.assert_floats_equal(3.0, m.c)
    cunittest.assert_floats_equal(4.0, m.d)


def test_matrix_vector_multiplication():
    """Tests multiplication between matrices and vectors"""
    #Test x-component of resulting vector
    m = a5.Matrix(5,7,0,0)
    v = a5.Vector(3,2)
    result = m * v
    cunittest.assert_floats_equal(29.0, result.x)
    cunittest.assert_floats_equal(0.0, result.y)
    
    #Test y-component of resulting vector:
    m = a5.Matrix(0,0,2,3)
    v = a5.Vector(1,1)
    result = m * v
    cunittest.assert_floats_equal(0.0, result.x)
    cunittest.assert_floats_equal(5.0, result.y)
    
    #Identity Matrix Test Case:
    m = a5.Matrix(1,0,0,1)
    v = a5.Vector(426.317, 9921.33)
    result = m * v
    cunittest.assert_floats_equal(426.317, result.x)
    cunittest.assert_floats_equal(9921.33, result.y)
    
    #General Test Case:
    m = a5.Matrix(0,1,2,3)
    v = a5.Vector(1,0)
    result = m * v
    cunittest.assert_floats_equal(0.0, result.x)
    cunittest.assert_floats_equal(2.0, result.y)
    
    #Identity Matrix Test Case:
    m = a5.Matrix(1,0,0,1)
    v = a5.Vector(426.317, 9921.33)
    result = m * v
    cunittest.assert_floats_equal(426.317, result.x)
    cunittest.assert_floats_equal(9921.33, result.y)


def test_matrix_matrix_multiplication():
    """Tests multiplication between matrices"""
    #Test element a of the resulting matrix:
    m1 = a5.Matrix(3,5,0,0)
    m2 = a5.Matrix(1,0,1,0)
    result = m1 * m2
    cunittest.assert_floats_equal(8.0,result.a)
    cunittest.assert_floats_equal(0.0,result.b)
    cunittest.assert_floats_equal(0.0,result.c)
    cunittest.assert_floats_equal(0.0,result.d)
    
    #Test element b of the resulting matrix:
    m1 = a5.Matrix(3,5,0,0)
    m2 = a5.Matrix(0,2,0,7)
    result = m1 * m2
    cunittest.assert_floats_equal(0.0,result.a)
    cunittest.assert_floats_equal(41.0,result.b)
    cunittest.assert_floats_equal(0.0,result.c)
    cunittest.assert_floats_equal(0.0,result.d)
    
    #Test element c of the resulting matrix:
    m1 = a5.Matrix(0,0,1,7)
    m2 = a5.Matrix(3,0,2,0)
    result = m1 * m2
    cunittest.assert_floats_equal(0.0,result.a)
    cunittest.assert_floats_equal(0.0,result.b)
    cunittest.assert_floats_equal(17.0,result.c)
    cunittest.assert_floats_equal(0.0,result.d)
    
    #Test element d of the resulting matrix:
    m1 = a5.Matrix(0,0,2,3)
    m2 = a5.Matrix(0,9,0,1)
    result = m1 * m2
    cunittest.assert_floats_equal(0.0,result.a)
    cunittest.assert_floats_equal(0.0,result.b)
    cunittest.assert_floats_equal(0.0,result.c)
    cunittest.assert_floats_equal(21.0,result.d)
    
    #General Test Case:
    m1 = a5.Matrix(1,2,3,4)
    m2 = a5.Matrix(4,3,2,1)
    result = m1 * m2
    cunittest.assert_floats_equal(8.0,result.a)
    cunittest.assert_floats_equal(5.0,result.b)
    cunittest.assert_floats_equal(20.0,result.c)
    cunittest.assert_floats_equal(13.0,result.d)
    
    #Identity Matrix Test Case:
    m1 = a5.Matrix(1,0,0,1)
    m2 = a5.Matrix(1,4,9,16)
    result = m1 * m2
    cunittest.assert_floats_equal(1.0,result.a)
    cunittest.assert_floats_equal(4.0,result.b)
    cunittest.assert_floats_equal(9.0,result.c)
    cunittest.assert_floats_equal(16.0,result.d)


#application code    
if __name__ == "__main__":
    test_vector_constructor()
    test_vector_addition()
    test_matrix_constructor()
    test_matrix_vector_multiplication()
    test_matrix_matrix_multiplication()
    print "Module a5 is working correctly"