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

"""
Handle all interactive actions from the player
"""

from fife import fife
from scripts.common.eventlistenerbase import EventListenerBase

class Controller(EventListenerBase):
    def __init__(self, engine, survivor, world):
        self.engine   = engine
        self.survivor = survivor
        self.world    = world
        self.camera   = world.get_camera()

        # self.eventmanager = engine.getEventManager()
        super(Controller, self).__init__(engine, regMouse=True, regKeys=True)

        self.keybindings = {'move_left':  [fife.Key.A],
                            'move_right': [fife.Key.E, fife.Key.D],
                            'move_down':  [fife.Key.O, fife.Key.S],
                            'move_up':    [fife.Key.COMMA, fife.Key.W],
                            'run':        [fife.Key.LEFT_SHIFT]}

        # FIXME: deprecated
        engine.getEventManager().setNonConsumableKeys([
                fife.Key.ESCAPE,])


    def keyPressed(self, evt):
        keyval = evt.getKey().getValue()
        keystr = evt.getKey().getAsString().lower()

        # system keys
        if keyval == fife.Key.ESCAPE:
            pass # TODO: show main menu
        elif keyval == fife.Key.F10:
            self.engine.getGuiManager().getConsole().toggleShowHide()
            evt.consume()
        elif keystr == 'p':
            self.engine.getRenderBackend().captureScreen('screenshot.png')
            evt.consume()

        # movement keys
        elif keyval in self.keybindings['move_left']:
            self.survivor.move_left  = True
        elif keyval in self.keybindings['move_right']:
            self.survivor.move_right = True
        elif keyval in self.keybindings['move_down']:
            self.survivor.move_down  = True
        elif keyval in self.keybindings['move_up']:
            self.survivor.move_up    = True
        elif keyval in self.keybindings['run']:
            self.survivor.run(True)
            print evt.getName()

        # debug keys
        elif keystr == 't':
            r = self.camera.getRenderer('GridRenderer')
            r.setEnabled(not r.isEnabled())
        elif keystr == 'c':
            r = self.camera.getRenderer('CoordinateRenderer')
            r.setEnabled(not r.isEnabled())
        # elif keystr == 'r':
        #     self.world.reload()

    def keyReleased(self, evt):
        keyval = evt.getKey().getValue()

        # movement keys
        if keyval   in self.keybindings['move_left']:
            self.survivor.move_left  = False
        elif keyval in self.keybindings['move_right']:
            self.survivor.move_right = False
        elif keyval in self.keybindings['move_down']:
            self.survivor.move_down  = False
        elif keyval in self.keybindings['move_up']:
            self.survivor.move_up    = False
        elif keyval in self.keybindings['run']:
            self.survivor.run(False)

    def mousePressed(self, evt):
        if evt.isConsumedByWidgets():
            return

        clickpoint = fife.ScreenPoint(evt.getX(), evt.getY())
        if (evt.getButton() == fife.MouseEvent.LEFT):
            loc = self.getLocationAt(clickpoint).getMapCoordinates()
            self.survivor.take_action(loc)

        if (evt.getButton() == fife.MouseEvent.RIGHT):
            instances = self.getInstancesAt(clickpoint)
            print "selected instances on agent layer: ", [i.getObject().getId() for i in instances]

    def getLocationAt(self, clickpoint):
        target_mapcoord = self.camera.toMapCoordinates(clickpoint, False)
        target_mapcoord.z = 0
        location = fife.Location(self.world.agentlayer)
        location.setMapCoordinates(target_mapcoord)
        return location

    def getInstancesAt(self, clickpoint):
        return self.camera.getMatchingInstances(clickpoint, self.world.agentlayer)

    def mouseReleased(self, evt):
        pass    
    def mouseEntered(self, evt):
        pass
    def mouseExited(self, evt):
        pass
    def mouseClicked(self, evt):
        pass
    def mouseWheelMovedUp(self, evt):
        pass    
    def mouseWheelMovedDown(self, evt):
        pass
    def mouseMoved(self, evt):
        pass
    def mouseDragged(self, evt):
        pass
    def mouseMoved(self, evt):
        pass
