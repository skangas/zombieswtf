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
from fife import *
from fife.fife import DoublePoint3D
from fife.extensions.fife_settings import Setting
from scripts.weapons import *

#TDS = Setting(app_name="zombieswtf")

_STATE_NONE, _STATE_IDLE, _STATE_RUN, _STATE_KICK, _STATE_TALK = xrange(5)

class Survivor(Agent,Movable):
    FIRING_OFFSET_X = 0.5
    FIRING_OFFSET_Y = -0.5
    STAMINA = 10
    STAMINARECOVERY = 10

    def __init__(self, engine, settings, agentName, layer, uniqInMap=True):
        super(Survivor, self).__init__(settings, None, agentName, layer, uniqInMap)
        self.setupMovable(self.agent)
        self.engine      = engine
        self.state       = _STATE_NONE
        self.idlecounter = 1
        self.move_left   = False
        self.move_right  = False
        self.move_up     = False
        self.move_down   = False
        self.speed       = 6.5
        self.sprint      = 5.0
        self.running     = 10.0
        self.walking     = 5.0
        self.projectiles = []

        self._current_weapon  = 0
        self._weapons         = [Shotgun(self)]
        self._score           = 0
        self._lives           = 3
        self._staminarecovery = self.STAMINARECOVERY
        self.recovery         = 5.0
        self.init()

    def face(self, target):
        loc = self.agent.getFacingLocation().getExactLayerCoordinates()

    def take_action(self, target):
        # TODO: check if there is something we can interact with at location
        if len(self._weapons) > 0:
            weapon = self._weapons[self._current_weapon]

            my_loc = self.agent.getLocation().getMapCoordinates()

            # Face target
            face_loc = fife.Location(self.layer)
            face_loc.setExactLayerCoordinates(target)
            self.agent.setFacingLocation(face_loc)

            # Add constant to avoid player from firing from the feet
            my_loc.x += self.FIRING_OFFSET_X
            my_loc.y += self.FIRING_OFFSET_Y

            bullets = weapon.fire_at(my_loc, target)
            for b in bullets:
                b.create(self.engine.getModel(), self.layer)
                self.projectiles.append(b)
        
    def init(self):
        self._hitpoints = 10
        self._dead = False
        self._stamina = self.STAMINA
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
        # Sets up timediff
        self.newFrame()

        actually_moving = (self.move_left ^ self.move_right or 
                           self.move_up ^ self.move_down)
        
        if not actually_moving:
            self.idle()
            return

        if self.state != _STATE_RUN:
            self.state = _STATE_RUN
            self.agent.act('run', self.agent.getFacingLocation())

        if self.speed == self.running and not self._exhausted:
            self._stamina -= self.sprint * self.timediff
        if self._stamina <= 0:
            self.run(False)
            self._exhausted = True
            self._staminarecovery -= self.recovery * self.timediff
        if self._staminarecovery <= 0:
            self._exhausted       = False
            self._stamina         = self.STAMINA
            self._staminarecovery = self.STAMINARECOVERY

        self.direction = DoublePoint3D(0,0)
        if (self.move_left):
            self.direction.x -= 1
            self.direction.y -= 1
        if (self.move_right):
            self.direction.x += 1
            self.direction.y += 1
        if (self.move_up):
            self.direction.x += 1
            self.direction.y -= 1
        if (self.move_down):
            self.direction.x -= 1
            self.direction.y += 1
        self.direction.normalize()

        assert self.direction.length() != 0, "Was actually moving at speed 0; shouldn't happen."

        self.move()

    def movePredicate(self,new_loc):
        # Make sure the space is not blocked
        instances = self.agent.getLocationRef().getLayer().getInstancesAt(new_loc)
        for i in instances:
            if i.getId() == 'player':
                continue
            if i.isBlocking():
                return False
        return True


