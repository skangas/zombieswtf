# -*- coding: utf-8 -*-
########################################################################
# Copyright (C) 2011, Stefan Kangas
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
from math import cos,sin

class Projectile():
    def __init__(self, name, loc, direction, speed, ttl, owner):
        self.loc         = loc
        self.direction   = direction
        self.speed       = speed
        self.owner       = owner
        self.started     = time()
        self._name       = name
        self.last_update = time()
        self.ttl         = ttl

    def create(self, model, layer):
        self._obj = model.getObject(self._name, "zombieswtf")
        inst = layer.createInstance(self._obj,
                                    fife.ExactModelCoordinate(self.loc.x ,
                                                              self.loc.y ),
                                    "projectile")
        InstanceVisual.create(inst)
        self._instance = inst
        self._instance.setOverrideBlocking(True)
        self._instance.setBlocking(False)

    def get_position():
        pass
    
    def update(self):
        
        #if time() - self.started > self.ttl:
            # how to remove an instance? 
            #pass

        # basically copy from survivor :(

        timediff = time() - self.last_update
        step = self.speed * timediff
        self.last_update = time()

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

class Weapon(object):
    def __init__(self, owner, speed, ttl):
        self.owner = owner
        self.speed = speed
        self.ttl   = ttl

    def fire(self, origin, direction):
        direction.normalize()
        bullet = Projectile(self.get_bullet_name(), origin,
                            direction, self.speed, self.ttl, self.owner)
        return bullet

    def fire_at(self, origin, target):
        direction = get_direction(origin, target)
        return self.fire(origin, direction)

    def get_bullet_name(self):
        raise Exception("Programming Error: not implemented")

class Axe(Weapon):
    def __init__(self, owner):
        SPEED = 10.0
        TTL = 2.0 
        super(Axe, self).__init__(owner, SPEED, TTL)

    def get_bullet_name(self):
        return 'axe'

class Pistol(Weapon):
    def __init__(self, owner):
        SPEED = 10.0
        TTL = 2.5
        super(Pistol, self).__init__(owner, SPEED, TTL)

    def get_bullet_name(self):
        return 'bullet'
