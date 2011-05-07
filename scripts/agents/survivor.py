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
import random

from math import hypot
from agent import Agent
from time import time
from fife.extensions.fife_settings import Setting
from scripts.weapons import *

#TDS = Setting(app_name="zombieswtf")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_KICK, _STATE_TALK = xrange(5)

STAMINA = 10
STAMINARECOVERY = 10

class Survivor(Agent):
    def __init__(self, engine, settings, agentName, layer, uniqInMap=True):
        super(Survivor, self).__init__(settings, None, agentName, layer, uniqInMap)
        self.engine      = engine
        #self.agent.setOverrideBlocking(True)
        #self.agent.setBlocking(False)
        self.state       = _STATE_NONE
        self.idlecounter = 1
        self.move_left   = False
        self.move_right  = False
        self.move_up     = False
        self.move_down   = False
        self.last_update = time()
        self.speed       = 6.5
        self.sprint      = 5.0
        self.running     = 10.0
        self.walking     = 5.0
        self.weapon      = Axe(self)
        self.projectiles = []

        self._score           = 0
        self._lives           = 3
        self._staminarecovery = STAMINARECOVERY
        self.recovery         = 5.0
        self.init()

    def take_action(self, target):
        # TODO: check if there is something we can interact with at location
        if (self.weapon != None):
            my_loc = self.agent.getLocation().getMapCoordinates()
            bullet = self.weapon.fire_at(my_loc, target)
            if bullet:
                bullet.create(self.engine.getModel(), self.layer)
                self.projectiles.append(bullet)
        
    def init(self):
        self._hitpoints = 10
        self._dead = False
        self._stamina = STAMINA
        self._exhausted = False

    def respawn(self):
        if self._lives >= 0:
            self.init()

    def onInstanceActionFinished(self, instance, action):
        self.idle()

    def start(self):
        self.idle()

    def idle(self):
        self.state = _STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation())

    def getScore(self):
        return self._score

    def getLives(self):
        return self._lives

    def incScore(self, sc):
        self._score += sc

    def setLives(self, lives):
        self._lives = lives

    def kick(self, target):
        self.state = _STATE_KICK
        self.agent.act('kick', target)

    def talk(self, target):
        self.state = _STATE_TALK
        self.agent.act('talk', target)

    def run(self, running):
        if self._stamina >= 0 and running:
            print 'run'
            self.speed = self.running
        else:
            self.speed = self.walking

    def update(self):
        timediff = time() - self.last_update
        self.last_update = time()
        
        actually_moving = (self.move_left ^ self.move_right or 
                           self.move_up ^ self.move_down)
        
        if not actually_moving:
            self.idle()
            return

        if self.state != _STATE_RUN:
            self.state = _STATE_RUN
            self.agent.act('run', self.agent.getFacingLocation())

        step = self.speed * timediff

        if self.speed == self.running and not self._exhausted:
            self._stamina -= self.sprint * timediff
        if self._stamina <= 0:
            self.run(False)
            self._exhausted = True
            self._staminarecovery -= self.recovery * timediff
        if self._staminarecovery <= 0:
            self._exhausted = False
            self._stamina = STAMINA
            self._staminarecovery = STAMINARECOVERY

        x = 0
        y = 0
        if (self.move_left):
            x -= 1
            y -= 1
        if (self.move_right):
            x += 1
            y += 1
        if (self.move_up):
            x += 1
            y -= 1
        if (self.move_down):
            x -= 1
            y += 1
        l = hypot(x,y)
        assert l != 0, "Was actually moving at speed 0; shouldn't happen."
        x /= l
        y /= l
        x *= step
        y *= step

        pos = self.agent.getLocation()
        cord = pos.getExactLayerCoordinates()
        cord.x += x * 10
        cord.y += y * 10
        pos.setExactLayerCoordinates(cord)
        self.agent.setFacingLocation(pos)
        
        cord.x -= x * 9
        cord.y -= y * 9
        pos.setExactLayerCoordinates(cord)

        # Make sure the space is not blocked
        instances = self.agent.getLocationRef().getLayer().getInstancesAt(pos)
        for i in instances:
            if i.getId() == 'player':
                continue
            if i.isBlocking():
                return

        self.agent.setLocation(pos)

