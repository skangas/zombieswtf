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

from fife import fife

class Agent(fife.InstanceActionListener):
    def __init__(self, settings, model, agentName, layer, uniqInMap=True):
        fife.InstanceActionListener.__init__(self)
        self.settings = settings
        self.model = model
        self.agentName = agentName
        self.layer = layer
        if uniqInMap:
            self.agent = layer.getInstance(agentName)
            self.agent.addActionListener(self)

        self.max_health = 100
        self.health     = 0

    def onInstanceActionFinished(self, instance, action):
        raise Exception('No OnActionFinished defined for Agent')

    def start(self):
        raise Exception('No start defined for Agent')

    def take_damage(self, amount):
        self.health -= amount
