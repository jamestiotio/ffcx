"Code snippets for code generation."

__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2007-02-28"
__copyright__ = "Copyright (C) 2007 Anders Logg"
__license__  = "GNU GPL version 3 or any later version"

# Modified by Kristian Oelgaard 2009
# Modified by Marie Rognes 2007 -- 2010
# Modified by Peter Brune 2009
# Last changed: 2010-01-07

# Code snippets

header_ufc = \
"""
// This code conforms with the UFC specification version 1.0
// and was automatically generated by FFC version %(version)s.

#ifndef __%(prefix_upper)s_H
#define __%(prefix_upper)s_H

#include <cmath>
#include <stdexcept>
#include <ufc.h>
"""

header_dolfin = \
"""
// This code conforms with the UFC specification version 1.0
// and was automatically generated by FFC version %(version)s.
//
// Warning: This code was generated with the option '-l dolfin'
// and contains DOLFIN-specific wrappers that depend on DOLFIN.

#ifndef __%(prefix_upper)s_H
#define __%(prefix_upper)s_H

#include <cmath>
#include <stdexcept>
#include <fstream>
#include <ufc.h>
"""

footer = \
"""

#endif
"""

cell_coordinates = "const double * const * x = c.coordinates;\n"
evaluate_f = "f.evaluate(values, y, c);\n"

jacobian_1D = \
"""
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];

// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00;

// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 =  1.0 / detJ%(restriction)s;
"""

jacobian_2D = \
"""
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];

// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;

// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 =  J%(restriction)s_11 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = -J%(restriction)s_01 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = -J%(restriction)s_10 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 =  J%(restriction)s_00 / detJ%(restriction)s;
"""

jacobian_3D = \
"""
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_02 = x%(restriction)s[3][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];
const double J%(restriction)s_12 = x%(restriction)s[3][1] - x%(restriction)s[0][1];
const double J%(restriction)s_20 = x%(restriction)s[1][2] - x%(restriction)s[0][2];
const double J%(restriction)s_21 = x%(restriction)s[2][2] - x%(restriction)s[0][2];
const double J%(restriction)s_22 = x%(restriction)s[3][2] - x%(restriction)s[0][2];

// Compute sub determinants
const double d%(restriction)s_00 = J%(restriction)s_11*J%(restriction)s_22 - J%(restriction)s_12*J%(restriction)s_21;
const double d%(restriction)s_01 = J%(restriction)s_12*J%(restriction)s_20 - J%(restriction)s_10*J%(restriction)s_22;
const double d%(restriction)s_02 = J%(restriction)s_10*J%(restriction)s_21 - J%(restriction)s_11*J%(restriction)s_20;

const double d%(restriction)s_10 = J%(restriction)s_02*J%(restriction)s_21 - J%(restriction)s_01*J%(restriction)s_22;
const double d%(restriction)s_11 = J%(restriction)s_00*J%(restriction)s_22 - J%(restriction)s_02*J%(restriction)s_20;
const double d%(restriction)s_12 = J%(restriction)s_01*J%(restriction)s_20 - J%(restriction)s_00*J%(restriction)s_21;

const double d%(restriction)s_20 = J%(restriction)s_01*J%(restriction)s_12 - J%(restriction)s_02*J%(restriction)s_11;
const double d%(restriction)s_21 = J%(restriction)s_02*J%(restriction)s_10 - J%(restriction)s_00*J%(restriction)s_12;
const double d%(restriction)s_22 = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;

// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*d%(restriction)s_00 + J%(restriction)s_10*d%(restriction)s_10 + J%(restriction)s_20*d%(restriction)s_20;

// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 = d%(restriction)s_00 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = d%(restriction)s_10 / detJ%(restriction)s;
const double Jinv%(restriction)s_02 = d%(restriction)s_20 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = d%(restriction)s_01 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 = d%(restriction)s_11 / detJ%(restriction)s;
const double Jinv%(restriction)s_12 = d%(restriction)s_21 / detJ%(restriction)s;
const double Jinv%(restriction)s_20 = d%(restriction)s_02 / detJ%(restriction)s;
const double Jinv%(restriction)s_21 = d%(restriction)s_12 / detJ%(restriction)s;
const double Jinv%(restriction)s_22 = d%(restriction)s_22 / detJ%(restriction)s;"""

scale_factor = \
"""
// Set scale factor
const double det = std::abs(detJ);
"""

facet_determinant_1D = \
"""
// Facet determinant 1D (vertex)
const double det = 1.0;
"""

normal_direction_1D = \
"""
"""

facet_normal_1D = \
"""
// Compute facet normals from the facet scale factor constants
// FIXME: not implemented
"""

facet_determinant_2D = \
"""
// Vertices on edges
static unsigned int edge_vertices[3][2] = {{1, 2}, {0, 2}, {0, 1}};

// Get vertices
const unsigned int v0 = edge_vertices[%(facet)s][0];
const unsigned int v1 = edge_vertices[%(facet)s][1];

// Compute scale factor (length of edge scaled by length of reference interval)
const double dx0 = x%(restriction)s[v1][0] - x%(restriction)s[v0][0];
const double dx1 = x%(restriction)s[v1][1] - x%(restriction)s[v0][1];
const double det = std::sqrt(dx0*dx0 + dx1*dx1);
"""

normal_direction_2D = \
"""
const bool direction = dx1*(x%(restriction)s[%(facet)s][0] - x%(restriction)s[v0][0]) - dx0*(x%(restriction)s[%(facet)s][1] - x%(restriction)s[v0][1]) < 0;
"""

facet_normal_2D = \
"""
// Compute facet normals from the facet scale factor constants
const double n%(restriction)s0 = %(direction)sdirection ? dx1 / det : -dx1 / det;
const double n%(restriction)s1 = %(direction)sdirection ? -dx0 / det : dx0 / det;
"""

facet_determinant_3D = \
"""
// Vertices on faces
static unsigned int face_vertices[4][3] = {{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}};

// Get vertices
const unsigned int v0 = face_vertices[%(facet)s][0];
const unsigned int v1 = face_vertices[%(facet)s][1];
const unsigned int v2 = face_vertices[%(facet)s][2];

// Compute scale factor (area of face scaled by area of reference triangle)
const double a0 = (x%(restriction)s[v0][1]*x%(restriction)s[v1][2]
                 + x%(restriction)s[v0][2]*x%(restriction)s[v2][1]
                 + x%(restriction)s[v1][1]*x%(restriction)s[v2][2])
                - (x%(restriction)s[v2][1]*x%(restriction)s[v1][2]
                 + x%(restriction)s[v2][2]*x%(restriction)s[v0][1]
                 + x%(restriction)s[v1][1]*x%(restriction)s[v0][2]);

const double a1 = (x%(restriction)s[v0][2]*x%(restriction)s[v1][0]
                 + x%(restriction)s[v0][0]*x%(restriction)s[v2][2]
                 + x%(restriction)s[v1][2]*x%(restriction)s[v2][0])
                - (x%(restriction)s[v2][2]*x%(restriction)s[v1][0]
                 + x%(restriction)s[v2][0]*x%(restriction)s[v0][2]
                + x%(restriction)s[v1][2]*x%(restriction)s[v0][0]);

const double a2 = (x%(restriction)s[v0][0]*x%(restriction)s[v1][1]
                 + x%(restriction)s[v0][1]*x%(restriction)s[v2][0]
                 + x%(restriction)s[v1][0]*x%(restriction)s[v2][1])
                - (x%(restriction)s[v2][0]*x%(restriction)s[v1][1]
                 + x%(restriction)s[v2][1]*x%(restriction)s[v0][0]
                 + x%(restriction)s[v1][0]*x%(restriction)s[v0][1]);

const double det = std::sqrt(a0*a0 + a1*a1 + a2*a2);
"""

normal_direction_3D = \
"""
const bool direction = a0*(x%(restriction)s[%(facet)s][0] - x%(restriction)s[v0][0]) + a1*(x%(restriction)s[%(facet)s][1] - x%(restriction)s[v0][1])  + a2*(x%(restriction)s[%(facet)s][2] - x%(restriction)s[v0][2]) < 0;
"""

facet_normal_3D = \
"""
// Compute facet normals from the facet scale factor constants
const double n%(restriction)s0 = %(direction)sdirection ? a0 / det : -a0 / det;
const double n%(restriction)s1 = %(direction)sdirection ? a1 / det : -a1 / det;
const double n%(restriction)s2 = %(direction)sdirection ? a2 / det : -a2 / det;
"""

eta_interval_snippet = \
"""
x = 2.0*x - 1.0;
"""

eta_triangle_snippet = \
"""
if (std::abs(y - 1.0) < %s)
  x = -1.0;
else
  x = 2.0 *x/(1.0 - y) - 1.0;
y = 2.0*y - 1.0;
"""

eta_tetrahedron_snippet = \
"""
if (std::abs(y + z - 1.0) < %s)
  x = 1.0;
else
  x = -2.0 * x/(y + z - 1.0) - 1.0;
if (std::abs(z - 1.0) < %s)
  y = -1.0;
else
  y = 2.0 * y/(1.0 - z) - 1.0;
z = 2.0 * z - 1.0;
"""

evaluate_basis_dof_map = \
"""
unsigned int element = 0;
unsigned int tmp = 0;
for (unsigned int j = 0; j < %d; j++)
{
  if (tmp +  dofs_per_element[j] > i)
  {
    i -= tmp;
    element = element_types[j];
    break;
  }
  else
    tmp += dofs_per_element[j];
}
"""

map_coordinates_interval = \
"""
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];

// Get coordinates and map to the reference (UFC) element
double x = (coordinates[0] - element_coordinates[0][0]) / J_00;
"""

map_coordinates_triangle = \
"""
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];

// Compute determinant of Jacobian
const double detJ = J_00*J_11 - J_01*J_10;

// Compute inverse of Jacobian
const double Jinv_00 =  J_11 / detJ;
const double Jinv_01 = -J_01 / detJ;
const double Jinv_10 = -J_10 / detJ;
const double Jinv_11 =  J_00 / detJ;

// Get coordinates and map to the reference (UFC) element
double x = (element_coordinates[0][1]*element_coordinates[2][0] -\\
            element_coordinates[0][0]*element_coordinates[2][1] +\\
            J_11*coordinates[0] - J_01*coordinates[1]) / detJ;
double y = (element_coordinates[1][1]*element_coordinates[0][0] -\\
            element_coordinates[1][0]*element_coordinates[0][1] -\\
            J_10*coordinates[0] + J_00*coordinates[1]) / detJ;
"""

map_coordinates_tetrahedron = \
"""
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_02 = element_coordinates[3][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];
const double J_12 = element_coordinates[3][1] - element_coordinates[0][1];
const double J_20 = element_coordinates[1][2] - element_coordinates[0][2];
const double J_21 = element_coordinates[2][2] - element_coordinates[0][2];
const double J_22 = element_coordinates[3][2] - element_coordinates[0][2];

// Compute sub determinants
const double d00 = J_11*J_22 - J_12*J_21;
const double d01 = J_12*J_20 - J_10*J_22;
const double d02 = J_10*J_21 - J_11*J_20;

const double d10 = J_02*J_21 - J_01*J_22;
const double d11 = J_00*J_22 - J_02*J_20;
const double d12 = J_01*J_20 - J_00*J_21;

const double d20 = J_01*J_12 - J_02*J_11;
const double d21 = J_02*J_10 - J_00*J_12;
const double d22 = J_00*J_11 - J_01*J_10;

// Compute determinant of Jacobian
double detJ = J_00*d00 + J_10*d10 + J_20*d20;

// Compute inverse of Jacobian
const double Jinv_00 = d00 / detJ;
const double Jinv_01 = d10 / detJ;
const double Jinv_02 = d20 / detJ;
const double Jinv_10 = d01 / detJ;
const double Jinv_11 = d11 / detJ;
const double Jinv_12 = d21 / detJ;
const double Jinv_20 = d02 / detJ;
const double Jinv_21 = d12 / detJ;
const double Jinv_22 = d22 / detJ;

// Compute constants
const double C0 = d00*(element_coordinates[0][0] - element_coordinates[2][0] - element_coordinates[3][0]) \\
                + d10*(element_coordinates[0][1] - element_coordinates[2][1] - element_coordinates[3][1]) \\
                + d20*(element_coordinates[0][2] - element_coordinates[2][2] - element_coordinates[3][2]);

const double C1 = d01*(element_coordinates[0][0] - element_coordinates[1][0] - element_coordinates[3][0]) \\
                + d11*(element_coordinates[0][1] - element_coordinates[1][1] - element_coordinates[3][1]) \\
                + d21*(element_coordinates[0][2] - element_coordinates[1][2] - element_coordinates[3][2]);

const double C2 = d02*(element_coordinates[0][0] - element_coordinates[1][0] - element_coordinates[2][0]) \\
                + d12*(element_coordinates[0][1] - element_coordinates[1][1] - element_coordinates[2][1]) \\
                + d22*(element_coordinates[0][2] - element_coordinates[1][2] - element_coordinates[2][2]);

// Get coordinates and map to the UFC reference element
double x = (C0 + d00*coordinates[0] + d10*coordinates[1] + d20*coordinates[2]) / detJ;
double y = (C1 + d01*coordinates[0] + d11*coordinates[1] + d21*coordinates[2]) / detJ;
double z = (C2 + d02*coordinates[0] + d12*coordinates[1] + d22*coordinates[2]) / detJ;
"""

map_coordinates_FIAT_triangle = \
"""
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];

// Compute determinant of Jacobian
const double detJ = J_00*J_11 - J_01*J_10;

// Compute constants
const double C0 = element_coordinates[1][0] + element_coordinates[2][0];
const double C1 = element_coordinates[1][1] + element_coordinates[2][1];

// Get coordinates and map to the reference (FIAT) element
double x = (J_01*C1 - J_11*C0 + 2.0*J_11*coordinates[0] - 2.0*J_01*coordinates[1]) / detJ;
double y = (J_10*C0 - J_00*C1 - 2.0*J_10*coordinates[0] + 2.0*J_00*coordinates[1]) / detJ;
"""

map_coordinates_FIAT_tetrahedron = \
"""
// Extract vertex coordinates
const double * const * element_coordinates = c.coordinates;

// Compute Jacobian of affine map from reference cell
const double J_00 = element_coordinates[1][0] - element_coordinates[0][0];
const double J_01 = element_coordinates[2][0] - element_coordinates[0][0];
const double J_02 = element_coordinates[3][0] - element_coordinates[0][0];
const double J_10 = element_coordinates[1][1] - element_coordinates[0][1];
const double J_11 = element_coordinates[2][1] - element_coordinates[0][1];
const double J_12 = element_coordinates[3][1] - element_coordinates[0][1];
const double J_20 = element_coordinates[1][2] - element_coordinates[0][2];
const double J_21 = element_coordinates[2][2] - element_coordinates[0][2];
const double J_22 = element_coordinates[3][2] - element_coordinates[0][2];

// Compute sub determinants
const double d00 = J_11*J_22 - J_12*J_21;
const double d01 = J_12*J_20 - J_10*J_22;
const double d02 = J_10*J_21 - J_11*J_20;

const double d10 = J_02*J_21 - J_01*J_22;
const double d11 = J_00*J_22 - J_02*J_20;
const double d12 = J_01*J_20 - J_00*J_21;

const double d20 = J_01*J_12 - J_02*J_11;
const double d21 = J_02*J_10 - J_00*J_12;
const double d22 = J_00*J_11 - J_01*J_10;

// Compute determinant of Jacobian
double detJ = J_00*d00 + J_10*d10 + J_20*d20;

// Compute constants
const double C0 = element_coordinates[3][0] + element_coordinates[2][0] \\
                + element_coordinates[1][0] - element_coordinates[0][0];
const double C1 = element_coordinates[3][1] + element_coordinates[2][1] \\
                + element_coordinates[1][1] - element_coordinates[0][1];
const double C2 = element_coordinates[3][2] + element_coordinates[2][2] \\
                + element_coordinates[1][2] - element_coordinates[0][2];

// Get coordinates and map to the reference (FIAT) element
double x = coordinates[0];
double y = coordinates[1];
double z = coordinates[2];

x = (2.0*d00*x + 2.0*d10*y + 2.0*d20*z - d00*C0 - d10*C1 - d20*C2) / detJ;
y = (2.0*d01*x + 2.0*d11*y + 2.0*d21*z - d01*C0 - d11*C1 - d21*C2) / detJ;
z = (2.0*d02*x + 2.0*d12*y + 2.0*d22*z - d02*C0 - d12*C1 - d22*C2) / detJ;
"""

combinations_snippet = \
"""
// Declare pointer to two dimensional array that holds combinations of derivatives and initialise
unsigned int **%(combinations)s = new unsigned int *[%(num_derivatives)s];

for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(combinations)s[j] = new unsigned int [%(n)s];
  for (unsigned int k = 0; k < %(n)s; k++)
    %(combinations)s[j][k] = 0;
}

// Generate combinations of derivatives
for (unsigned int row = 1; row < %(num_derivatives)s; row++)
{
  for (unsigned int num = 0; num < row; num++)
  {
    for (unsigned int col = %(n)s-1; col+1 > 0; col--)
    {
      if (%(combinations)s[row][col] + 1 > %(shape-1)s)
        %(combinations)s[row][col] = 0;
      else
      {
        %(combinations)s[row][col] += 1;
        break;
      }
    }
  }
}
"""

transform_interval_snippet = \
"""
// Compute inverse of Jacobian
const double %(Jinv)s[1][1] =  {{1.0 / J_00}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];

for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}
"""

transform_triangle_snippet = \
"""
// Compute inverse of Jacobian
const double %(Jinv)s[2][2] =  {{J_11 / detJ, -J_01 / detJ}, {-J_10 / detJ, J_00 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];

for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}
"""

transform_tetrahedron_snippet = \
"""
// Compute inverse of Jacobian
const double %(Jinv)s[3][3] =\
{{d00 / detJ, d10 / detJ, d20 / detJ},\
 {d01 / detJ, d11 / detJ, d21 / detJ},\
 {d02 / detJ, d12 / detJ, d22 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];

for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}
"""

transform2D_FIAT_snippet = \
"""
// Compute inverse of Jacobian, components are scaled because of difference in FFC/FIAT reference elements
const double %(Jinv)s[2][2] =  {{2*J_11 / detJ, -2*J_01 / detJ}, {-2*J_10 / detJ, 2*J_00 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];

for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}
"""

transform3D_FIAT_snippet = \
"""
// Compute inverse of Jacobian, components are scaled because of difference in FFC/FIAT reference elements
const double %(Jinv)s[3][3] =\
{{2*d00 / detJ, 2*d10 / detJ, 2*d20 / detJ},\
 {2*d01 / detJ, 2*d11 / detJ, 2*d21 / detJ},\
 {2*d02 / detJ, 2*d12 / detJ, 2*d22 / detJ}};

// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%(transform)s = new double *[%(num_derivatives)s];

for (unsigned int j = 0; j < %(num_derivatives)s; j++)
{
  %(transform)s[j] = new double [%(num_derivatives)s];
  for (unsigned int k = 0; k < %(num_derivatives)s; k++)
    %(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  for (unsigned int col = 0; col < %(num_derivatives)s; col++)
  {
    for (unsigned int k = 0; k < %(n)s; k++)
      %(transform)s[row][col] *= %(Jinv)s[%(combinations)s[col][k]][%(combinations)s[row][k]];
  }
}
"""

inverse_jacobian_2D = \
"""
// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;

// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 =  J%(restriction)s_11 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = -J%(restriction)s_01 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = -J%(restriction)s_10 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 =  J%(restriction)s_00 / detJ%(restriction)s;"""

inverse_jacobian_3D = """\
// Compute sub determinants
const double d00 = J%(restriction)s_11*J%(restriction)s_22 - J%(restriction)s_12*J%(restriction)s_21;
const double d01 = J%(restriction)s_12*J%(restriction)s_20 - J%(restriction)s_10*J%(restriction)s_22;
const double d02 = J%(restriction)s_10*J%(restriction)s_21 - J%(restriction)s_11*J%(restriction)s_20;

const double d10 = J%(restriction)s_02*J%(restriction)s_21 - J%(restriction)s_01*J%(restriction)s_22;
const double d11 = J%(restriction)s_00*J%(restriction)s_22 - J%(restriction)s_02*J%(restriction)s_20;
const double d12 = J%(restriction)s_01*J%(restriction)s_20 - J%(restriction)s_00*J%(restriction)s_21;

const double d20 = J%(restriction)s_01*J%(restriction)s_12 - J%(restriction)s_02*J%(restriction)s_11;
const double d21 = J%(restriction)s_02*J%(restriction)s_10 - J%(restriction)s_00*J%(restriction)s_12;
const double d22 = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;

// Compute determinant of Jacobian
double detJ%(restriction)s = J%(restriction)s_00*d00 + J%(restriction)s_10*d10 + J%(restriction)s_20*d20;

// Compute inverse of Jacobian
const double Jinv%(restriction)s_00 = d00 / detJ%(restriction)s;
const double Jinv%(restriction)s_01 = d10 / detJ%(restriction)s;
const double Jinv%(restriction)s_02 = d20 / detJ%(restriction)s;
const double Jinv%(restriction)s_10 = d01 / detJ%(restriction)s;
const double Jinv%(restriction)s_11 = d11 / detJ%(restriction)s;
const double Jinv%(restriction)s_12 = d21 / detJ%(restriction)s;
const double Jinv%(restriction)s_20 = d02 / detJ%(restriction)s;
const double Jinv%(restriction)s_21 = d12 / detJ%(restriction)s;
const double Jinv%(restriction)s_22 = d22 / detJ%(restriction)s;
"""

map_onto_physical_1D = \
"""
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][%(j)s][0];
const double w1 = X[i][%(j)s][0];

// Compute affine mapping y = F(X)
double y[1];
y[0] = w0*x[0][0] + w1*x[1][0];
"""
map_onto_physical_2D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][%(j)s][0] - X[i][%(j)s][1];
const double w1 = X[i][%(j)s][0];
const double w2 = X[i][%(j)s][1];

// Compute affine mapping y = F(X)
double y[2];
y[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0];
y[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1];
"""

map_onto_physical_3D = \
"""
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X[i][%(j)s][0] - X[i][%(j)s][1] - X[i][%(j)s][2];
const double w1 = X[i][%(j)s][0];
const double w2 = X[i][%(j)s][1];
const double w3 = X[i][%(j)s][2];

// Compute affine mapping y = F(X)
double y[3];
y[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0] + w3*x[3][0];
y[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1] + w3*x[3][1];
y[2] = w0*x[0][2] + w1*x[1][2] + w2*x[2][2] + w3*x[3][2];
"""

calculate_dof = \
"""
// Take directional components
for(int k = 0; k < %(dim)d; k++)
  result += values[k]*D[i][%(index)s][k];
// Multiply by weights
result *= W[i][%(index)s];
"""

only_jacobian_1D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];"""

only_jacobian_2D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];"""

only_jacobian_3D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_02 = x%(restriction)s[3][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];
const double J%(restriction)s_12 = x%(restriction)s[3][1] - x%(restriction)s[0][1];
const double J%(restriction)s_20 = x%(restriction)s[1][2] - x%(restriction)s[0][2];
const double J%(restriction)s_21 = x%(restriction)s[2][2] - x%(restriction)s[0][2];
const double J%(restriction)s_22 = x%(restriction)s[3][2] - x%(restriction)s[0][2];"""

cell_integral_call =\
"""%(reset_tensor)s

tabulate_tensor_tensor(A, w, c);
tabulate_tensor_quadrature(A, w, c);"""

exterior_facet_integral_call =\
"""%(reset_tensor)s

tabulate_tensor_tensor(A, w, c, facet);
tabulate_tensor_quadrature(A, w, c, facet);"""

interior_facet_integral_call =\
"""%(reset_tensor)s

tabulate_tensor_tensor(A, w, c0, c1, facet0, facet1);
tabulate_tensor_quadrature(A, w, c0, c1, facet0, facet1);"""

private_declarations = \
{"cell_integral_combined":\
"""
/// Tabulate the tensor for the contribution from a local cell
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c) const
{
%(tabulate_tensor)s
}
""",
"cell_integral_header":\
"""
/// Tabulate the tensor for the contribution from a local cell
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c) const;
""",
"cell_integral_implementation":\
"""
/// Tabulate the tensor for the contribution from a local cell
void %(classname)s::%(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c) const
{
%(tabulate_tensor)s
}
""",
"exterior_facet_integral_combined":\
"""
/// Tabulate the tensor for the contribution from a local exterior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const
{
%(tabulate_tensor)s
}
""",
"exterior_facet_integral_header":\
"""
/// Tabulate the tensor for the contribution from a local exterior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const;
""",
"exterior_facet_integral_implementation":\
"""
/// Tabulate the tensor for the contribution from a local exterior facet
void %(classname)s::%(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const
{
%(tabulate_tensor)s
}
""",
"interior_facet_integral_combined":\
"""
/// Tabulate the tensor for the contribution from a local interior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const
{
%(tabulate_tensor)s
}
""",
"interior_facet_integral_header":\
"""
/// Tabulate the tensor for the contribution from a local interior facet
void %(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const;
""",
"interior_facet_integral_implementation":\
"""
/// Tabulate the tensor for the contribution from a local interior facet
void %(classname)s::%(function_name)s(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const
{
%(tabulate_tensor)s
}
"""}

# Mappings to code snippetes
jacobian = {1: jacobian_1D, 2: jacobian_2D, 3: jacobian_3D}
