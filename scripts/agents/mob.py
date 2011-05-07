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

# Handle the mobs

from fife import fife
from math import hypot
from random import *
from scripts.agents.agent import *
from time import time

class Mob(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Mob, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.layer = layer
        self.health = 10

    def onInstanceActionFinished(self, instance, action):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

_STATE_NONE, _STATE_IDLE, _STATE_ROAM, _STATE_FOLLOW, _STATE_ATTACK, _STATE_DYING, _STATE_DEAD = xrange(7)

ZOMBIE_MOVEMENT_SPEED = 1.6
ATTACK_RANGE = 1.5
PROVOKE_RANGE = 8
GIVE_UP_RANGE = 10
MIN_IDLE_TIME_MS = 400
MAX_IDLE_TIME_MS = 1500

class Zombie(Mob):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Zombie, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.state = _STATE_NONE
        self.health = 1
        self.setIdleTimer()

    def aggro(self, player):
        self.hero = player.agent

    def follow_hero(self):
        self.state = _STATE_FOLLOW
        self.agent.follow('walk', self.hero, ZOMBIE_MOVEMENT_SPEED)

    def setIdleTimer(self):
        self.idle_timer = time()
        self.idle_time = float(randint(MIN_IDLE_TIME_MS,MAX_IDLE_TIME_MS)) / 1000

    def onInstanceActionFinished(self, instance, action):
        if action.getId() == 'die' or action.getId() == 'dead':
            self.agent.act('dead', self.agent.getLocation(), False)
            self.state = _STATE_DEAD
        else:
            self.idle()

    def idle(self):
        self.state = _STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation(), False)
        self.setIdleTimer()

    def is_dead(self):
        return self.state == _STATE_DEAD or self.state == _STATE_DYING

    def roam(self):
        self.state = _STATE_ROAM
        pos = self.agent.getLocation()
        cord = pos.getExactLayerCoordinates()
        cord.x += randint(-2,2)
        cord.y += randint(-2,2)
        pos.setExactLayerCoordinates(cord)
        self.agent.move('walk', pos, ZOMBIE_MOVEMENT_SPEED)
        pass

    def start(self):
        self.idle()

    ## to save some resources, this need not to be calculated every frame
    def update(self):
        if self.state == _STATE_DYING or self.state == _STATE_DEAD:
            return

        if self.health <= 0:
            self.state = _STATE_DYING
            self.agent.act('die', self.agent.getFacingLocation(), False)
            self.agent.setOverrideBlocking(True)
            self.agent.setBlocking(False)
            return

        mecord = self.agent.getLocation().getExactLayerCoordinates()
        herocord = self.hero.getLocation().getExactLayerCoordinates()
        dist = hypot(mecord.x - herocord.x, mecord.y - herocord.y)
        if dist > GIVE_UP_RANGE and self.state == _STATE_FOLLOW:
            self.idle()
            return
        if dist <= ATTACK_RANGE:
            if self.state != _STATE_ATTACK:
                self.state = _STATE_ATTACK
                self.agent.act('attack', self.hero.getLocation(), False)
            return
        elif dist < PROVOKE_RANGE:
            if self.state != _STATE_FOLLOW:
                self.follow_hero()
            return

        if self.state == _STATE_ROAM:
            return

        now = time()
        #print '{} to {}'.format(now - self.idle_timer,self.idle_time)
        if self.state == _STATE_IDLE and now - self.idle_timer > self.idle_time:
            self.roam()

def create_mob_agents(settings, model, objectName, layer, agentClass):
    """Given an objectName (read: zombie), makes a Zombie object for each instance on the map.

    Returns the list of objects"""
    agents = []
    instances = [a for a in layer.getInstances() if a.getObject().getId() == objectName]
    i = 0
    for a in instances:
        agentName = '%s:%d' % (objectName, i)
        print 'agent created: ' + agentName
        i += 1
        agent = agentClass(settings, model, agentName, layer, False)
        agent.agent = a
        a.addActionListener(agent)
        agents.append(agent)
    return agents
