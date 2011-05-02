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

# The main application class

import sys, os, re, math, random, shutil

from fife import fife

from fife.extensions import *
from scripts import world
from scripts.common import eventlistenerbase
from fife.extensions.basicapplication import ApplicationBase
from fife.extensions import pychan
from fife.extensions.pychan import widgets
from fife.extensions.fife_settings import Setting
from fife.extensions.fife_utils import getUserDataDirectory
from fife.extensions.soundmanager import SoundManager

TDS = Setting(app_name="zombieswtf")

class ApplicationListener(eventlistenerbase.EventListenerBase):
        def __init__(self, engine, world):
                super(ApplicationListener, self).__init__(engine,regCmd=True, regConsole=True, regWidget=True)
                self.engine = engine
                self.world = world

                self.quit = False
                self.aboutWindow = None

                self.rootpanel = pychan.loadXML('gui/rootpanel.xml')
                self.rootpanel.mapEvents({ 
                        'quitButton' : self.onQuitButtonPress,
                        'aboutButton' : self.onAboutButtonPress,
                        'optionsButton' : TDS.onOptionsPress
                })
                self.rootpanel.show()

        def onCommand(self, command):
                self.quit = (command.getCommandType() == fife.CMD_QUIT_GAME)
                if self.quit:
                        command.consume()

        def onConsoleCommand(self, command):
                result = ''
                if command.lower() in ('quit', 'exit'):
                        self.quit = True
                        result = 'quitting'
                elif command.lower() in ( 'help', 'help()' ):
                        self.engine.getGuiManager().getConsole().println( open( 'misc/infotext.txt', 'r' ).read() )
                        result = "-- End of help --"
                else:
                        result = self.world.onConsoleCommand(command)
                if not result:
                        try:
                                result = str(eval(command))
                        except:
                                pass
                if not result:
                        result = 'no result'
                return result

        def onQuitButtonPress(self):
                cmd = fife.Command()
                cmd.setSource(None)
                cmd.setCommandType(fife.CMD_QUIT_GAME)
                self.engine.getEventManager().dispatchCommand(cmd)

        def onAboutButtonPress(self):
                if not self.aboutWindow:
                        self.aboutWindow = pychan.loadXML('gui/help.xml')
                        self.aboutWindow.mapEvents({ 'closeButton' : self.aboutWindow.hide })
                        self.aboutWindow.distributeData({ 'helpText' : open("misc/infotext.txt").read() })
                self.aboutWindow.show()

class ZombiesWTF(ApplicationBase):
        def __init__(self):
                super(ZombiesWTF,self).__init__(TDS)
                self.world = world.World(self.engine)
                self.listener = ApplicationListener(self.engine, self.world)

                self.soundmanager = SoundManager(self.engine)
                #self.music = None

        def createListener(self):
                pass # already created in constructor

        def _pump(self):
                if self.listener.quit:
                        self.breakRequested = True
                        
                        # # get the correct directory to save the map file to
                        # mapSaveDir = getUserDataDirectory("fife", "rio_de_hola") + "/maps"
                        
                        # # create the directory structure if it does not exist
                        # if not os.path.isdir(mapSaveDir):
                        #       os.makedirs(mapSaveDir)
                        
                        # # save map file to directory
                        # self.world.save(mapSaveDir + "/savefile.xml")
                else:
                        self.world.pump()
