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

# Dangerous zombies!

from fife import fife
from scripts.agents.mob import *
from math import hypot
from time import time
from random import *

_STATE_NONE, _STATE_IDLE, _STATE_FOLLOW, _STATE_SPURIOUS = xrange(4)

ZOMBIE_SPEED = 1.6
PROVOKE_RANGE = 5
GIVE_UP_RANGE = 10
MIN_IDLE_TIME_MS = 400
MAX_IDLE_TIME_MS = 1000

class Zombie(Mob):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Zombie, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.setIdleTimer()

    def aggro(self, player):
        self.hero = player.agent

    def setIdleTimer(self):
        self.idle_timer = time()
        self.idle_time = float(randint(MIN_IDLE_TIME_MS,MAX_IDLE_TIME_MS)) / 1000

    def onInstanceActionFinished(self, instance, action):
        self.idle()

    def start(self):
        self.idle()

    def idle(self):
        self.state = _STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation(), False)
        self.setIdleTimer()

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('attack', self.hero, ZOMBIE_SPEED)

    def spurious(self):
        #print 'spurios wakeup!'
        self.state = _STATE_SPURIOUS
        pos = self.agent.getLocation()
        cord = pos.getExactLayerCoordinates()
        cord.x += randint(-2,2)
        cord.y += randint(-2,2)
        pos.setExactLayerCoordinates(cord)
        self.agent.move('attack', pos, ZOMBIE_SPEED)
        pass

    ## to save some resources, this need not to be calculated every frame
    def update(self):
        mecord = self.agent.getLocation().getExactLayerCoordinates()
        herocord = self.hero.getLocation().getExactLayerCoordinates()
        dist = hypot(mecord.x - herocord.x, mecord.y - herocord.y)
        # print 'distance to hero: {}'.format(dist)
        if dist > GIVE_UP_RANGE and self.state == _STATE_FOLLOW:
            self.idle()
            return
        if dist < PROVOKE_RANGE and self.state != _STATE_FOLLOW:
            self.follow_hero()
            return

        if self.state == _STATE_SPURIOUS:
            return

        now = time()
        #print '{} to {}'.format(now - self.idle_timer,self.idle_time)
        if self.state == _STATE_IDLE and now - self.idle_timer > self.idle_time:
            self.spurious()



