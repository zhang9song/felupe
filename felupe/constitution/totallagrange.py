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

from ..math import (
    dot,
    ddot,
    ddot44,
    transpose,
    majortranspose,
    inv,
    dya,
    cdya,
    cdya_ik,
    cdya_il,
    det,
    identity,
    trace,
    dev,
)


class Composite:
    def __init__(self, *args):

        self.materials = args
        self.kind = "total-lagrange"

    def S(self, *args, **kwargs):
        return np.sum([m.S(*args) for m in self.materials], 0)

    def C4(self, *args, **kwargs):
        return np.sum([m.C4(*args, **kwargs) for m in self.materials], 0)


class Material:
    def __init__(self, stress, elasticity):

        self.stress = stress
        self.elasticity = elasticity
        self.kind = "total-lagrange"

    def S(self, *args, **kwargs):
        return self.stress(*args, **kwargs)

    def C4(self, *args, **kwargs):
        return self.elasticity(*args, **kwargs)


class Hydrostatic:
    def __init__(self, bulk):
        self.bulk = bulk
        self.kind = "total-lagrange"

    def dUdJ(self, J):
        return self.bulk * (J - 1)

    def d2UdJdJ(self, J):
        return self.bulk

    def S(self, F, J, C, invC):
        return self.dUdJ(J) * J * invC

    def C4(self, F, J, C, invC):
        p = self.dUdJ(J)
        q = p + self.d2UdJdJ(J) * J
        return J * (q * dya(invC, invC) - 2 * p * cdya(invC, invC))


class AsIsochoric:
    def __init__(self, material_isochoric):
        self.isochoric = material_isochoric
        self.kind = "total-lagrange"

    def S(self, F, J, C, invC):
        Cu = J ** (-2 / 3) * C
        Sb = J ** (-2 / 3) * self.isochoric.S(Cu)
        return Sb - ddot(Sb, C) / 3 * invC

    def C4(self, F, J, C, invC):
        eye = identity(C)
        P4 = cdya(eye, eye) - dya(invC, C) / 3

        Cu = J ** (-2 / 3) * C
        Sb = J ** (-2 / 3) * self.isochoric.S(Cu)

        C4u = self.isochoric.C4(Cu)
        if np.all(C4u == 0):
            PC4bP = C4u
        else:
            C4b = J ** (-4 / 3) * C4u
            PC4bP = ddot44(ddot44(P4, C4b), majortranspose(P4))

        SbC = ddot(Sb, C)

        return (
            PC4bP
            - 2 / 3 * (dya(Sb, invC) + dya(invC, Sb))
            + 2 / 9 * SbC * dya(invC, invC)
            + 2 / 3 * SbC * cdya(invC, invC)
        )
