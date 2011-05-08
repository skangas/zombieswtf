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

_WEAPON_RANGED, _WEAPON_MELEE = xrange(2)

class Weapon(object):
    def __init__(self, owner):
        self.owner = owner
        self._last_shot = 0

    def fire(self, origin, direction):
        now = time()
        if time() - self._last_shot > self.get_delay():
            direction.normalize()
            self._last_shot = now
            return Projectile(self.PROJECTILE, origin, direction,
                              self.SPEED, self.TTL, self.DAMAGE,
                              self.owner)

    def fire_at(self, origin, target):
        direction = get_direction(origin, target)
        return self.fire(origin, direction)

class Axe(Weapon):
    ATTACK_RATE = 0.75
    DAMAGE      = 5.0
    PROJECTILE  = 'axe'
    SPEED       = 10.0
    TTL         = 2.0
    TYPE        = _WEAPON_RANGED

    def __init__(self, owner):
        super(Axe, self).__init__(owner)

class Pistol(Weapon):
    ATTACK_RATE = 0.2
    DAMAGE      = 1.0
    PROJECTILE  = 'bullet'
    SPEED       = 10.0
    TTL         = 2.5
    TYPE        = _WEAPON_RANGED

    def __init__(self, owner):
        super(Pistol, self).__init__(owner)
