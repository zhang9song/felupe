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

from ._base import HexahedronElement
from ._lagrange import ArbitraryOrderLagrange


class ConstantHexahedron(HexahedronElement):
    def __init__(self):
        self.points = 8
        super().__init__(self._fun, self._grad, 1)

    def _fun(self, rst):
        "constant hexahedron shape functions"
        return np.array([1])

    def _grad(self, rst):
        "constant hexahedron gradient of shape functions"
        return np.array([[0, 0, 0]])


class Hexahedron(HexahedronElement):
    def __init__(self):
        self.points = 8
        super().__init__(self._fun, self._grad, 8)

    def _fun(self, rst):
        "linear hexahedron shape functions"
        r, s, t = rst
        return (
            np.array(
                [
                    (1 - r) * (1 - s) * (1 - t),
                    (1 + r) * (1 - s) * (1 - t),
                    (1 + r) * (1 + s) * (1 - t),
                    (1 - r) * (1 + s) * (1 - t),
                    (1 - r) * (1 - s) * (1 + t),
                    (1 + r) * (1 - s) * (1 + t),
                    (1 + r) * (1 + s) * (1 + t),
                    (1 - r) * (1 + s) * (1 + t),
                ]
            )
            * 0.125
        )

    def _grad(self, rst):
        "linear hexahedron gradient of shape functions"
        r, s, t = rst
        return (
            np.array(
                [
                    [-(1 - s) * (1 - t), -(1 - r) * (1 - t), -(1 - r) * (1 - s)],
                    [(1 - s) * (1 - t), -(1 + r) * (1 - t), -(1 + r) * (1 - s)],
                    [(1 + s) * (1 - t), (1 + r) * (1 - t), -(1 + r) * (1 + s)],
                    [-(1 + s) * (1 - t), (1 - r) * (1 - t), -(1 - r) * (1 + s)],
                    [-(1 - s) * (1 + t), -(1 - r) * (1 + t), (1 - r) * (1 - s)],
                    [(1 - s) * (1 + t), -(1 + r) * (1 + t), (1 + r) * (1 - s)],
                    [(1 + s) * (1 + t), (1 + r) * (1 + t), (1 + r) * (1 + s)],
                    [-(1 + s) * (1 + t), (1 - r) * (1 + t), (1 - r) * (1 + s)],
                ]
            )
            * 0.125
        )


class QuadraticHexahedron(HexahedronElement):
    def __init__(self):
        self.points = 20
        super().__init__(self._fun, self._grad, 20)

    def _fun(self, rst):
        "quadratic serendipity hexahedron shape functions"
        r, s, t = rst
        return np.array(
            [
                -(1 - r) * (1 - s) * (1 - t) * (2 + r + s + t) * 0.125,
                -(1 + r) * (1 - s) * (1 - t) * (2 - r + s + t) * 0.125,
                -(1 + r) * (1 + s) * (1 - t) * (2 - r - s + t) * 0.125,
                -(1 - r) * (1 + s) * (1 - t) * (2 + r - s + t) * 0.125,
                #
                -(1 - r) * (1 - s) * (1 + t) * (2 + r + s - t) * 0.125,
                -(1 + r) * (1 - s) * (1 + t) * (2 - r + s - t) * 0.125,
                -(1 + r) * (1 + s) * (1 + t) * (2 - r - s - t) * 0.125,
                -(1 - r) * (1 + s) * (1 + t) * (2 + r - s - t) * 0.125,
                #
                (1 - r) * (1 + r) * (1 - s) * (1 - t) * 0.25,
                (1 - s) * (1 + s) * (1 + r) * (1 - t) * 0.25,
                (1 - r) * (1 + r) * (1 + s) * (1 - t) * 0.25,
                (1 - s) * (1 + s) * (1 - r) * (1 - t) * 0.25,
                #
                (1 - r) * (1 + r) * (1 - s) * (1 + t) * 0.25,
                (1 - s) * (1 + s) * (1 + r) * (1 + t) * 0.25,
                (1 - r) * (1 + r) * (1 + s) * (1 + t) * 0.25,
                (1 - s) * (1 + s) * (1 - r) * (1 + t) * 0.25,
                #
                (1 - t) * (1 + t) * (1 - r) * (1 - s) * 0.25,
                (1 - t) * (1 + t) * (1 + r) * (1 - s) * 0.25,
                (1 - t) * (1 + t) * (1 + r) * (1 + s) * 0.25,
                (1 - t) * (1 + t) * (1 - r) * (1 + s) * 0.25,
            ]
        )

    def _grad(self, rst):
        "quadratic serendipity hexahedron gradient of shape functions"
        r, s, t = rst
        return np.array(
            [
                [
                    (1 - s) * (1 - t) * (2 + r + s + t) * 0.125
                    - (1 - r) * (1 - s) * (1 - t) * 0.125,
                    (1 - r) * (1 - t) * (2 + r + s + t) * 0.125
                    - (1 - r) * (1 - s) * (1 - t) * 0.125,
                    (1 - r) * (1 - s) * (2 + r + s + t) * 0.125
                    - (1 - r) * (1 - s) * (1 - t) * 0.125,
                ],
                [
                    -(1 - s) * (1 - t) * (2 - r + s + t) * 0.125
                    + (1 + r) * (1 - s) * (1 - t) * 0.125,
                    (1 + r) * (1 - t) * (2 - r + s + t) * 0.125
                    - (1 + r) * (1 - s) * (1 - t) * 0.125,
                    (1 + r) * (1 - s) * (2 - r + s + t) * 0.125
                    - (1 + r) * (1 - s) * (1 - t) * 0.125,
                ],
                [
                    -(1 + s) * (1 - t) * (2 - r - s + t) * 0.125
                    + (1 + r) * (1 + s) * (1 - t) * 0.125,
                    -(1 + r) * (1 - t) * (2 - r - s + t) * 0.125
                    + (1 + r) * (1 + s) * (1 - t) * 0.125,
                    (1 + r) * (1 + s) * (2 - r - s + t) * 0.125
                    - (1 + r) * (1 + s) * (1 - t) * 0.125,
                ],
                [
                    (1 + s) * (1 - t) * (2 + r - s + t) * 0.125
                    - (1 - r) * (1 + s) * (1 - t) * 0.125,
                    -(1 - r) * (1 - t) * (2 + r - s + t) * 0.125
                    + (1 - r) * (1 + s) * (1 - t) * 0.125,
                    (1 - r) * (1 + s) * (2 + r - s + t) * 0.125
                    - (1 - r) * (1 + s) * (1 - t) * 0.125,
                ],
                #
                [
                    (1 - s) * (1 + t) * (2 + r + s - t) * 0.125
                    - (1 - r) * (1 - s) * (1 + t) * 0.125,
                    (1 - r) * (1 + t) * (2 + r + s - t) * 0.125
                    - (1 - r) * (1 - s) * (1 + t) * 0.125,
                    -(1 - r) * (1 - s) * (2 + r + s - t) * 0.125
                    + (1 - r) * (1 - s) * (1 + t) * 0.125,
                ],
                [
                    -(1 - s) * (1 + t) * (2 - r + s - t) * 0.125
                    + (1 + r) * (1 - s) * (1 + t) * 0.125,
                    (1 + r) * (1 + t) * (2 - r + s - t) * 0.125
                    - (1 + r) * (1 - s) * (1 + t) * 0.125,
                    -(1 + r) * (1 - s) * (2 - r + s - t) * 0.125
                    + (1 + r) * (1 - s) * (1 + t) * 0.125,
                ],
                [
                    -(1 + s) * (1 + t) * (2 - r - s - t) * 0.125
                    + (1 + r) * (1 + s) * (1 + t) * 0.125,
                    -(1 + r) * (1 + t) * (2 - r - s - t) * 0.125
                    + (1 + r) * (1 + s) * (1 + t) * 0.125,
                    -(1 + r) * (1 + s) * (2 - r - s - t) * 0.125
                    + (1 + r) * (1 + s) * (1 + t) * 0.125,
                ],
                [
                    (1 + s) * (1 + t) * (2 + r - s - t) * 0.125
                    - (1 - r) * (1 + s) * (1 + t) * 0.125,
                    -(1 - r) * (1 + t) * (2 + r - s - t) * 0.125
                    + (1 - r) * (1 + s) * (1 + t) * 0.125,
                    -(1 - r) * (1 + s) * (2 + r - s - t) * 0.125
                    + (1 - r) * (1 + s) * (1 + t) * 0.125,
                ],
                #
                [
                    -2 * r * (1 - s) * (1 - t) * 0.25,
                    -(1 - r) * (1 + r) * (1 - t) * 0.25,
                    -(1 - r) * (1 + r) * (1 - s) * 0.25,
                ],
                [
                    (1 - s) * (1 + s) * (1 - t) * 0.25,
                    -2 * s * (1 + r) * (1 - t) * 0.25,
                    -(1 - s) * (1 + s) * (1 + r) * 0.25,
                ],
                [
                    -2 * r * (1 + s) * (1 - t) * 0.25,
                    (1 - r) * (1 + r) * (1 - t) * 0.25,
                    -(1 - r) * (1 + r) * (1 + s) * 0.25,
                ],
                [
                    -(1 - s) * (1 + s) * (1 - t) * 0.25,
                    -2 * s * (1 - r) * (1 - t) * 0.25,
                    -(1 - s) * (1 + s) * (1 - r) * 0.25,
                ],
                #
                [
                    -2 * r * (1 - s) * (1 + t) * 0.25,
                    -(1 - r) * (1 + r) * (1 + t) * 0.25,
                    (1 - r) * (1 + r) * (1 - s) * 0.25,
                ],
                [
                    (1 - s) * (1 + s) * (1 + t) * 0.25,
                    -2 * s * (1 + r) * (1 + t) * 0.25,
                    (1 - s) * (1 + s) * (1 + r) * 0.25,
                ],
                [
                    -2 * r * (1 + s) * (1 + t) * 0.25,
                    (1 - r) * (1 + r) * (1 + t) * 0.25,
                    (1 - r) * (1 + r) * (1 + s) * 0.25,
                ],
                [
                    -(1 - s) * (1 + s) * (1 + t) * 0.25,
                    -2 * s * (1 - r) * (1 + t) * 0.25,
                    (1 - s) * (1 + s) * (1 - r) * 0.25,
                ],
                #
                [
                    -(1 - t) * (1 + t) * (1 - s) * 0.25,
                    -(1 - t) * (1 + t) * (1 - r) * 0.25,
                    -2 * t * (1 - r) * (1 - s) * 0.25,
                ],
                [
                    (1 - t) * (1 + t) * (1 - s) * 0.25,
                    -(1 - t) * (1 + t) * (1 + r) * 0.25,
                    -2 * t * (1 + r) * (1 - s) * 0.25,
                ],
                [
                    (1 - t) * (1 + t) * (1 + s) * 0.25,
                    (1 - t) * (1 + t) * (1 + r) * 0.25,
                    -2 * t * (1 + r) * (1 + s) * 0.25,
                ],
                [
                    -(1 - t) * (1 + t) * (1 + s) * 0.25,
                    (1 - t) * (1 + t) * (1 - r) * 0.25,
                    -2 * t * (1 - r) * (1 + s) * 0.25,
                ],
            ]
        )


class TriQuadraticHexahedron(HexahedronElement):
    def __init__(self):
        super().__init__(self._fun, self._grad, 27)

        self.points = 27

        self._lagrange = ArbitraryOrderLagrange(order=2, ndim=3)

        self._vertices = np.array([0, 2, 8, 6, 18, 20, 26, 24])
        self._edges = np.array([1, 5, 7, 3, 19, 23, 25, 21, 9, 11, 17, 15])
        self._faces = np.array([12, 14, 10, 16, 4, 22])
        self._volume = np.array([13])

        self._permute = np.concatenate(
            (self._vertices, self._edges, self._faces, self._volume)
        )

    def _fun(self, rst):
        "quadratic hexahedron shape functions"

        return self._lagrange.shape.function(rst)[self._permute]

    def _grad(self, rst):
        "quadratic hexahedron gradient of shape functions"

        return self._lagrange.shape.gradient(rst)[self._permute, :]
