# -*- coding: utf-8 -*-
########################################################################
# Copyright (C) 2011, Stefan Kangas
# Copyright (C) 2011, Dan Rosén
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

from fife import fife
from fife.fife import InstanceVisual
from scripts.util import get_direction
from time import time

class Projectile():
    def __init__(self, name, loc, direction, speed, ttl, damage, owner):
        self._name       = name
        self.loc         = loc
        self.direction   = direction
        self.speed       = speed
        self.ttl         = ttl
        self.damage      = damage
        self.owner       = owner

        self.active      = False

        self._started     = time()
        self._last_update = time()
        self._instance   = None

    def create(self, model, layer):
        self.layer = layer
        self._obj = model.getObject(self._name, "zombieswtf")
        inst = layer.createInstance(self._obj,
                                    fife.ExactModelCoordinate(self.loc.x ,
                                                              self.loc.y ),
                                    "projectile")
        InstanceVisual.create(inst)
        self._instance = inst
        self._instance.setOverrideBlocking(True)
        self._instance.setBlocking(False)
        self.active = True

    def get_position(self):
        assert self._instance
        return self._instance.getLocation()

    def hit(self):
        self.active = False

    def update(self):
        
        if not self.active or time() - self._started > self.ttl:
            return

        # basically copy from survivor :(

        timediff = time() - self._last_update
        step = self.speed * timediff
        self._last_update = time()

        x = step * self.direction.x
        y = step * self.direction.y

        pos = self._instance.getLocation()
        cord = pos.getExactLayerCoordinates()
        cord.x += x * 10
        cord.y += y * 10
        pos.setExactLayerCoordinates(cord)
        self._instance.setFacingLocation(pos)
        
        cord.x -= x * 9
        cord.y -= y * 9
        pos.setExactLayerCoordinates(cord)

        self._instance.setLocation(pos)
