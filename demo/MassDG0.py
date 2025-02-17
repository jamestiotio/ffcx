# Copyright (C) 2021 Igor Baratta
#
# This file is part of FFCx.
#
# FFCx is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FFCx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with FFCx. If not, see <http://www.gnu.org/licenses/>.
#
# The bilinear form for a mass matrix.
import basix.ufl
from ufl import FunctionSpace, Mesh, TestFunction, TrialFunction, dx, inner

element = basix.ufl.element("DG", "tetrahedron", 0)
domain = Mesh(basix.ufl.element("Lagrange", "tetrahedron", 1, shape=(3, )))
space = FunctionSpace(domain, element)

v = TestFunction(space)
u = TrialFunction(space)

a = inner(u, v) * dx
