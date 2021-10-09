# -*- coding: utf-8 -*-
"""
 _______  _______  ___      __   __  _______  _______ 
|       ||       ||   |    |  | |  ||       ||       |
|    ___||    ___||   |    |  | |  ||    _  ||    ___|
|   |___ |   |___ |   |    |  |_|  ||   |_| ||   |___ 
|    ___||    ___||   |___ |       ||    ___||    ___|
|   |    |   |___ |       ||       ||   |    |   |___ 
|___|    |_______||_______||_______||___|    |_______|

This file is part of felupe.

Felupe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Felupe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Felupe.  If not, see <http://www.gnu.org/licenses/>.

"""

import numpy as np
from ._base import Field
from ..math import sym as symmetric


class FieldAxisymmetric(Field):
    """Axisymmetric field with
    
    * component 1 ...  axial component
    * component 2 ... radial component
    
    
     x_2 (radial direction)
    
      ^
      |        _
      |       / \
    --|-----------------> x_1 (axial rotation axis)
              \_^
    
    This is a modified Field class in which the radial coordinates
    are evaluated at the quadrature points. The `grad`-function is
    modified in such a way that it does not only contain the in-plane
    2d-gradient but also the circumferential stretch
    as shown in Eq.(1).

                  |  dudX(2d) :   0   |
      dudX(axi) = | ..................|                  (1)
                  |     0     : u_r/R |

    """

    def __init__(self, region, dim=2, values=0):
        """A continous axisymmetric Field on points of a two-dimensional
        `region` with dimension `dim` (default is 2) and initial point 
        `values` (default is 0).
        
        Attributes
        ----------
        region : felupe.Region
            The region on which the field will be created.
        dim : int (default is 2)
            The dimension of the field.
        values : float (default is 0.0) or array
            A single value for all components of the field or an array of
            shape (region.mesh.npoints, dim)`.
        
        Methods
        -------
        grad
            Gradient as partial derivative of field values at points w.r.t. 
            undeformed coordinates, evaluated at the integration points of
            all cells in the region. Optionally, the symmetric part of
            the gradient is evaluated.
        """
    
        # init base Field
        super().__init__(region, dim=dim, values=values)
        
        # create scalar-valued field of radial point values
        self.scalar = Field(region, dim=1, values=region.mesh.points[:, 1])
        
        # interpolate radial point values to integration points of each cell
        # in the region
        self.radius = self.scalar.interpolate()

    def _grad_2d(self, sym=False):
        "Calculate the in-plane 2d-gradient dudX_IJpe."
        
        # gradient as partial derivative of field component "I" at point "a"
        # w.r.t. undeformed coordinate "J" evaluated at quadrature point "p"
        # for each cell "e"
        g = np.einsum(
            "ca...,aJpc->...Jpc", self.values[self.region.mesh.cells], self.region.dhdX,
        )
        
        if sym:
            return symmetric(g)
        else:
            return g

    def grad(self, sym=False):
        "Return the full 3d - (symmetric) gradient dudX_IJpe."
        
        # extend dimension of in-plane 2d-gradient
        g = np.pad(self._grad_2d(sym=sym), ((0, 1), (0, 1), (0, 0), (0, 0)))
        
        # set dudX_33 = u_r / R
        g[-1, -1] = self.interpolate()[1] / self.radius
        
        return g
