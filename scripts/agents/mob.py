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
from scripts.agents.agent import *

class Mob(Agent):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        super(Mob, self).__init__(settings, model, agentName, layer, uniqInMap)
        self.layer = layer
        self.health = 10

    def onInstanceActionFinished(self, instance, action):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def take_damage(self, amount):
        self.health -= amount

def create_mob_agents(settings, model, objectName, layer, agentClass):
    agents = []
    instances = [a for a in layer.getInstances() if a.getObject().getId() == objectName]
    i = 0
    for a in instances:
        agentName = '%s:i:%d' % (objectName, i)
        print 'agent created: ' + agentName
        i += 1
        agent = agentClass(settings, model, agentName, layer, False)
        agent.agent = a
        a.addActionListener(agent)
        agents.append(agent)
    return agents
