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

from scripts.util import get_angle
from time import time

class Projectile():
    def __init__(self, x, y, angle, speed, ttl, owner):
        self.x       = x
        self.y       = y
        self.angle   = angle
        self.speed   = speed
        self.owner   = owner
        self.started = time()

    def get_position():
        pass

class Weapon(object):
    def __init__(self, owner, speed, ttl):
        self.owner = owner
        self.speed = speed
        self.ttl   = ttl

    def fire(self, origin, angle):
        bullet = Projectile(origin.x, origin.y, angle, self.speed, self.ttl, self.owner)
        return bullet

    def fire_at(self, origin, target):
        angle = get_angle(origin, target)
        fire(origin, angle)

class Pistol(Weapon):

    def __init__(self, owner):
        SPEED = 10.0
        TTL = 2.5
        super(Pistol, self).__init__(owner, SPEED, TTL)

