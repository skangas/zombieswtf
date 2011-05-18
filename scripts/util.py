# -*- coding: utf-8 -*-
########################################################################
# Copyright (C) 2011, Stefan Kangas, Dan Rosén
########################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

from fife.fife import DoublePoint3D

def get_direction(pos1, pos2):
    x = pos2.x - pos1.x
    y = pos2.y - pos1.y
    a = DoublePoint3D(x, y)
    a.normalize()   
    return a

def scalar_mult(d,v):
    v.x *= d
    v.y *= d
    v.z *= d

def dot(u,v):
    return u.x * v.x + u.y * v.y + u.z * v.z

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 1

def line_points(loc1, loc2, step):
    """Returns the points from loc1 to loc2 with steps of size step in between."""
    # Points from x1 to x2
    x1 = loc1.getExactLayerCoordinates()
    x2 = loc2.getExactLayerCoordinates()
    
    # d is the directed increment
    d = x2 - x1
    d.normalize()
    scalar_mult(step,d)

    # dm is the mirrored direction
    dm = DoublePoint3D(d.y,d.x)
    
    # start from x1
    x = x1

    # which side of x2 is it on?
    initialSign = sign(dot(dm,x2-x))

    # list of points
    res = []

    # continue until it has passed x2
    while (sign(dot(dm,x2-x)) == initialSign):
        res.append(x)
        x = x + d

    # also add x2
    res.append(x2)
    return res
        
