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
from agent import Agent
from time import time
from fife.extensions.fife_settings import Setting
from scripts.weapons import *

#TDS = Setting(app_name="zombieswtf")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_KICK, _STATE_TALK = xrange(5)

STAMINA = 10
STAMINARECOVERY = 10

class Survivor(Agent):
    def __init__(self, settings, agentName, layer, uniqInMap=True):
        super(Survivor, self).__init__(settings, None, agentName, layer, uniqInMap)
        self.state       = _STATE_NONE
        self.idlecounter = 1
        self.move_left   = False
        self.move_right  = False
        self.move_up     = False
        self.move_down   = False
        self.last_update = time()
        self.speed       = 5.0
        self.sprint      = 5.0
        self.running     = 10.0
        self.walking     = 5.0
        self.weapon      = Pistol(self)

        self._score = 0
        self._lives = 3
        self._staminarecovery = STAMINARECOVERY
        self.recovery = 5.0
        self.init()

    def take_action(self, target):
        # TODO: check if there is something we can interact with at location

        if (self.weapon != None):
            my_loc = self.agent.getLocation().getMapCoordinates()
            bullet = self.weapon.fire(my_loc, target)
        
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

    def run(self):
        if self._stamina >= 0:
            self.speed = self.running
        else:
            self.speed = self.walking

    def update(self):
        now = time()
        blocked = False

        if not (self.move_left or self.move_right or self.move_up or self.move_down):
            self.idle()
            self.last_update = now
            return

        if self.state != _STATE_RUN:
            self.state = _STATE_RUN
            self.agent.act('run', self.agent.getFacingLocation())

        step = self.speed * (now - self.last_update)

        if self.speed == self.running and not self._exhausted:
            self._stamina -= self.sprint * (now - self.last_update)
            self.run()
            print 'run'
        if self._stamina <= 0:
            self._exhausted = True
            self._staminarecovery -= self.recovery * (now - self.last_update)
            print 'recovery'
        if self._staminarecovery <= 0:
            self._exhausted = False
            self._stamina = STAMINA
            self._staminarecovery = STAMINARECOVERY
            print 'gogo'

        x = 0
        y = 0
        if (self.move_left):
            x -= step
            y -= step
        if (self.move_right):
            x += step
            y += step
        if (self.move_up):
            x += step
            y -= step
        if (self.move_down):
            x -= step
            y += step
        if x == 0 and y == 0:
            return

        pos = self.agent.getLocation()
        cord = pos.getExactLayerCoordinates()
        cord.x += x * 10
        cord.y += y * 10
        pos.setExactLayerCoordinates(cord)
        self.agent.setFacingLocation(pos)
        
        cord.x -= x * 9
        cord.y -= y * 9
        pos.setExactLayerCoordinates(cord)
        
        self.last_update = now

        # Make sure the space is not blocked
        instances = self.agent.getLocationRef().getLayer().getInstancesAt(pos)
        for i in instances:
            if i.getId() == 'PC':
                continue
            if i.isBlocking():
                print "BLOCK", i.getId()
                return

        self.agent.setLocation(pos)

