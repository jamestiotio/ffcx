__author__ = "Anders Logg (logg@tti-c.org)"
__date__ = "2004-10-04 -- 2005-04-28"
__copyright__ = "Copyright (c) 2004 Anders Logg"
__license__  = "GNU GPL Version 2"

# FIAT modules
from FIAT import quadrature
from FIAT.shapes import *
from FIAT.Lagrange import Lagrange, VectorLagrange

shape_to_string = { LINE: "Line", TRIANGLE: "Triangle", TETRAHEDRON: "Tetrahedron" }
string_to_shape = { "Line": LINE, "Triangle": TRIANGLE, "Tetrahedron": TETRAHEDRON }

class FiniteElement:

    """A FiniteElement represents a finite element in the classical
    sense as defined by Ciarlet. The actual work is done by FIAT and
    this class serves as the interface to FIAT finite elements from
    within FFC.

    A FiniteElement is specified by giving the name and degree of the
    finite element, together with the name of the reference cell:

      name:   "Lagrange", "Hermite", ...
      degree: 0, 1, 2, ...
      shape:  "line", "triangle", "tetrahedron"

    The degree and shape must match the chosen type of finite element."""

    def __init__(self, name, shape, degree):
        "Create FiniteElement."

        # Initialize data
        self.name = name
        self.element = None
        self.table = None

        # FIXME: Should be able to ask FIAT about this
        self.tmp_rank = None
        self.tmp_tensordims = []

        # Choose shape
        if shape == "line":
            fiat_shape = LINE
        elif shape == "triangle":
            fiat_shape = TRIANGLE
        elif shape == "tetrahedron":
            fiat_shape = TETRAHEDRON
        else:
            raise RuntimeError, "Unknown shape " + str(shape)

        # Choose function space
        if name == "Lagrange":

            self.element = Lagrange(fiat_shape, degree)

            # FIXME: Should be able to ask FIAT about this
            self.tmp_rank = 0
            self.tmp_tensordims = []
            
        elif name == "Vector Lagrange":

            self.element = VectorLagrange(fiat_shape, degree)

            # FIXME: Should be able to ask FIAT about this
            self.tmp_rank = 1
            if fiat_shape == TRIANGLE:
                self.tmp_tensordims = [2]
            else:
                self.tmp_tensordims = [3]
                
        else:
            raise RuntimeError, "Unknown finite element: " + str(name)

        return

    def basis(self):
        "Return basis of finite element space."
        return self.element.function_space()

    def degree(self):
        "Return degree of polynomial basis."
        return self.basis().degree()

    def shape(self):
        "Return shape used for element."
        return self.element.domain_shape()

    def spacedim(self):
        "Return dimension of finite element space."
        return len(self.basis())

    def shapedim(self):
        "Return dimension of of shape."
        return dims[self.shape()]

    def rank(self):
        "Return rank of basis functions."
        return self.tmp_rank
    
    def tensordim(self, i):
        "Return size of given dimension."
        return self.tmp_tensordims[i]

    def __repr__(self):
        "Print nicely formatted representation of FiniteElement."
        return "%s finite element of degree %d on a %s" % \
               (self.name, self.degree(), shape_to_string[self.shape()])

if __name__ == "__main__":

    print "Testing finite element"
    print "----------------------"

    P1 = FiniteElement("Lagrange", "triangle", 1)
    Q1 = FiniteElement("Lagrange", "triangle", 1, 3)
    
    P2 = FiniteElement("Lagrange", "triangle", 2)

    quadrature = quadrature.make_quadrature(P1.fiat_shape, 5)

    w1 = P1.basis()[0];
    w2 = Q1.basis()[0][0];

    I1 = quadrature(w1.deriv(0))
    I2 = quadrature(w2.deriv(0))

    print "I1 = " + str(I1)
    print "I2 = " + str(I2)
