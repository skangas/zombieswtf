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

from fife import fife
from fife.fife import InstanceVisual
from scripts.util import get_direction
from scripts.projectile import *
from time import time

class Weapon(object):
    def __init__(self, owner, speed, ttl, worldRef):
        self.owner = owner
        self.speed = speed
        self.ttl   = ttl
        self.worldRef = worldRef

    def fire(self, origin, direction):
        direction.normalize()
        bullet = Projectile(self.get_bullet_name(), origin,
                            direction, self.speed, self.ttl, self.owner, self.worldRef)
        return bullet

    def fire_at(self, origin, target):
        direction = get_direction(origin, target)
        return self.fire(origin, direction)

    def get_bullet_name(self):
        raise Exception("Programming Error: not implemented")

class Axe(Weapon):
    def __init__(self, owner, worldRef):
        SPEED = 10.0
        TTL = 2.0 
        super(Axe, self).__init__(owner, SPEED, TTL, worldRef)

    def get_bullet_name(self):
        return 'axe'

class Pistol(Weapon):
    def __init__(self, owner, worldRef):
        SPEED = 10.0
        TTL = 2.5
        super(Pistol, self).__init__(owner, SPEED, TTL, worldRef)

    def get_bullet_name(self):
        return 'bullet'
