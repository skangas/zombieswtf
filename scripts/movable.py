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

# This is an abstract class that can move an instance in a direction

from fife import fife
from math import hypot
from time import time

class Movable(object):
    def __init__(self):
        super(Movable,self).__init__()

    def setupMovable(self,instance):
        """Sets up the movable interface"""
        self.last_update = time()
        self.instance = instance

    def movePredicate(self,new_loc):
        """If this instance can crash into walls, players, etc, then override this function."""
        return True

    def newFrame(self):
        """Setup time differences since last frame."""
        self.timediff = time() - self.last_update
        self.last_update = time()

    def move(self):
        """Faces along direction, and if movePredicate is True, moves in that direction."""

        # We can probably use DoublePoint3D but reference documentation is down right now
        # so I don't know the exact functions
        # d = DoublePoint2D(self.direction.x, self.direction.y)

        x = self.direction.x * self.speed * self.timediff
        y = self.direction.y * self.speed * self.timediff

        cur_loc = self.instance.getLocation()

        # Construct the new location to face
        face_cord = cur_loc.getExactLayerCoordinates()
        face_cord.x += x * 10 # Arbitrary number > 1
        face_cord.y += y * 10
        face_loc = fife.Location(cur_loc.getLayer())
        face_loc.setExactLayerCoordinates(face_cord)

        # Change facing direction
        self.instance.setFacingLocation(face_loc)

        # Construct the new player location
        new_cord = cur_loc.getExactLayerCoordinates()
        new_cord.x += x
        new_cord.y += y
        new_loc = fife.Location(cur_loc.getLayer())
        new_loc.setExactLayerCoordinates(new_cord)

        if not self.movePredicate(new_loc):
            return

        # Update location
        self.instance.setLocation(new_loc)

        
        

    


        
