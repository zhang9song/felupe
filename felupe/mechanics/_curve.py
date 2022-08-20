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

from ._job import Job
from ..tools import force


class CharacteristicCurve(Job):
    def __init__(self, steps, boundary):

        super().__init__(steps, self._callback)

        self.boundary = boundary
        self.x = []
        self.y = []

    def _callback(self, substep):

        self.x.append(substep.x[0].values[self.boundary.points[0]])
        self.y.append(force(substep.x, substep.fun, self.boundary))

    def plot(
        self, xaxis=0, yaxis=0, xlabel="x", ylabel="y", fig=None, ax=None, **kwargs
    ):

        import matplotlib.pyplot as plt

        self.evaluate(**kwargs)

        x = np.array(self.x)
        y = np.array(self.y)

        if fig is None or ax is None:
            fig, ax = plt.subplots()

        ax.plot(x[:, xaxis], y[:, yaxis], ".-")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return fig, ax
