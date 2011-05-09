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
from fife.fife import DoublePoint3D
from scripts.util import get_direction
from scripts.projectile import *
from time import time
from random import *
from math import *

_WEAPON_RANGED, _WEAPON_MELEE = xrange(2)

class Weapon(object):
    PROJECTILES = 1
    def __init__(self, owner):
        super(Weapon,self).__init__()
        self.owner = owner
        self._last_shot = 0

    def fire(self, origin, direction):
        now = time()

        if time() - self._last_shot < self.ATTACK_RATE:
            return []

        self._last_shot = now
        direction.normalize()

        if self.PROJECTILES == 1:
            return [Projectile(self.PROJECTILE, origin, direction,
                               self.SPEED, self.TTL, self.DAMAGE, self.owner)]

        else: 
            n = self.PROJECTILES
            deg = atan2(direction.y,direction.x)
            _SPRAY_DEGREES = 20
            res = []
            for a in range(n):
                # Stupid spray sketch
                alpha = (a-n/2.0)*_SPRAY_DEGREES/n
                d = DoublePoint3D(cos(alpha*pi/180+deg)+gauss(0.0,0.1),
                                  sin(alpha*pi/180+deg)+gauss(0.0,0.1))
                d.normalize()
                o = DoublePoint3D(origin.x+gauss(0.0,0.2),
                                  origin.y+gauss(0.0,0.2))
                res.append(Projectile(self.PROJECTILE, o, d,
                                      self.SPEED, self.TTL, self.DAMAGE, self.owner))
            return res

    def fire_at(self, origin, target):
        direction = get_direction(origin, target)
        return self.fire(origin, direction)

class Axe(Weapon):
    ATTACK_RATE = 0.8
    DAMAGE      = 5.0
    PROJECTILE  = 'axe'
    SPEED       = 10.0
    TTL         = 2.0
    TYPE        = _WEAPON_RANGED

    def __init__(self, owner):
        super(Axe, self).__init__(owner)

class Pistol(Weapon):
    ATTACK_RATE = 0.5
    DAMAGE      = 20.0
    PROJECTILE  = 'bullet'
    SPEED       = 100.0
    TTL         = 0.5
    TYPE        = _WEAPON_RANGED

    def __init__(self, owner):
        super(Pistol, self).__init__(owner)

class Shotgun(Weapon):
    PROJECTILES = 10
    ATTACK_RATE = 1.0
    DAMAGE      = 10.0
    PROJECTILE  = 'bullet'
    SPEED       = 100.0
    TTL         = 0.5
    TYPE        = _WEAPON_RANGED
    def __init__(self, owner):
        super(Shotgun, self).__init__(owner)

