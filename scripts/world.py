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
from fife.fife import LightRenderer, LightRendererNode
import math, random
from fife.extensions.loaders import loadMapFile
from fife.extensions.savers import saveMapFile
from fife.extensions.fife_settings import Setting
from fife.extensions import pychan
from fife.extensions.pychan import widgets
from scripts.common.eventlistenerbase import EventListenerBase
from agents.survivor import Survivor
from fife.extensions.fife_settings import Setting
from controller import Controller

from fife.fife import DoublePoint3D

from scripts.agents.mob import *

TDS = Setting(app_name="zombieswtf")

DEFAULT_GLOBAL_LIGHT = {
    "R" : 0.0,
    "G" : 0.0,
    "B" : 0.0,
    "A" : 0.985
}

DEFAULT_SURVIVOR_LIGHT = {
    "intensity" : 1,
    "radius"    : 100,
    "subdivs"   : 32,
    "xstretch"  : 3,
    "ystretch"  : 2,
    "R"         : 150,
    "G"         : 150,
    "B"         : 150
}

class MapListener(fife.MapChangeListener):
    def __init__(self, map):
        fife.MapChangeListener.__init__(self)
        map.addChangeListener(self)

    def onMapChanged(self, map, changedLayers):
        return
        print "Changes on map ", map.getId()
        for layer in map.getLayers():
            print layer.getId()
            print "    ", ["%s, %x" % (i.getObject().getId(), i.getChangeInfo()) for i in layer.getChangedInstances()]

    def onLayerCreate(self, map, layer):
        pass

    def onLayerDelete(self, map, layer):
        pass

class World(EventListenerBase):
    """
    The world!
    """
    def __init__(self, engine):
        super(World, self).__init__(engine, regKeys=True)
        self.engine = engine
        self.model = engine.getModel()
        self.imagepool = self.engine.getImagePool()

        self._global_light = DEFAULT_GLOBAL_LIGHT
        self._survivor_light_node = None
        self._survivor_light_opts = DEFAULT_SURVIVOR_LIGHT

        # cursor_name = TDS.get("zombieswtf", "default_crosshair")
        self.cursor_image = self.imagepool.addResourceFromFile("gui/crosshairs/crosshair6a.png")
        self.cursor_x_offset = -32
        self.cursor_y_offset = -32

        self.filename = ''
        # self.pump_ctr = 0 # for testing purposis

        # self.instancemenu = None
        self.instance_to_agent = {}
        # self.dynamic_widgets = {}

        # self.light_intensity = 1
        # self.light_sources = 0

        self.load('maps/snow.xml')

        self.controller = Controller(self.engine, self.survivor, self)

    def load(self, filename):
        self.filename = filename
        self.reset()

        self.map = loadMapFile(filename, self.engine, extensions = {'lights': True})

        self.maplistener = MapListener(self.map)

        self.initAgents()
        self.initCameras()

    def initAgents(self):
        """
        Initialize agents.
        """
        self.agentlayer = self.map.getLayer('ObjectLayer')
        self.survivor = Survivor(self.engine, TDS, 'player', self.agentlayer)
        self.instance_to_agent[self.survivor.agent.getFifeId()] = self.survivor
        self.survivor.start()
        
        self.zombies = create_mob_agents(TDS, self.model, 'zombie', self.agentlayer, Zombie)
        for zombie in self.zombies:
            self.instance_to_agent[zombie.agent.getFifeId()] = zombie
            zombie.aggro(self.survivor)
            zombie.start()
        					
    def getInstancesAt(self, clickpoint):
        """
        Query the main camera for instances on our active(agent) layer.
        """
        return self.cameras['main'].getMatchingInstances(clickpoint, self.agentlayer)

    def getLocationAt(self, clickpoint):
        """
        Query the main camera for the Map location (on the agent layer)
        that a screen point refers to.
        """
        target_mapcoord = self.cameras['main'].toMapCoordinates(clickpoint, False)
        target_mapcoord.z = 0
        location = fife.Location(self.agentlayer)
        location.setMapCoordinates(target_mapcoord)
        return location

    def onConsoleCommand(self, command):
        result = ''
        try:
            result = str(eval(command))
        except Exception, e:
            result = str(e)
        return result

    # # XXX: does not work
    # def reload(self):
    #     self.reset()
    #     model = self.engine.getModel()
    #     model.deleteMaps()
    #     self.load(self.filename)

    def initCameras(self):
        """Initialize cameras."""
        camera_prefix = self.filename.rpartition('.')[0] # Remove file extension
        camera_prefix = camera_prefix.rpartition('/')[2] # Remove path
        camera_prefix += '_'
    
        for cam in self.map.getCameras():
            camera_id = cam.getId().replace(camera_prefix, '')
            self.cameras[camera_id] = cam
            cam.resetRenderers()

        # show current coordinates
        self.cameras['main'].attach(self.survivor.agent)

        # Floating text renderers currntly only support one font.
        # ... so we set that up.
        # You'll se that for our demo we use a image font, so we have to specify the font glyphs
        # for that one.
        renderer = fife.FloatingTextRenderer.getInstance(self.cameras['main'])
        textfont = self.engine.getGuiManager().createFont('fonts/FreeSans.ttf', 0, str(TDS.get("FIFE", "FontGlyphs")));
        # renderer.changeDefaultFont(textfont)
        renderer.activateAllLayers(self.map)
        renderer.setBackground(100, 255, 100, 165)
        renderer.setBorder(50, 255, 50)
        renderer.setEnabled(True)
    
        # Activate the grid renderer on all layers
        renderer = self.cameras['main'].getRenderer('GridRenderer')
        renderer.activateAllLayers(self.map)
    
        # The following renderers are used for debugging.
        # Note that by default ( that is after calling View.resetRenderers or Camera.resetRenderers )
        # renderers will be handed all layers. That's handled here.

        # XXX: Dan: could not get these to work after changing map
        #renderer = self.cameras['main'].getRenderer('CoordinateRenderer')
        #renderer.clearActiveLayers()
        #renderer.addActiveLayer(self.map.getLayer(str(TDS.get("rio", "CoordinateLayerName"))))

        renderer = self.cameras['main'].getRenderer('QuadTreeRenderer')
        renderer.setEnabled(True)
        renderer.clearActiveLayers()
        if str(TDS.get("rio", "QuadTreeLayerName")):
            renderer.addActiveLayer(self.map.getLayer(str(TDS.get("rio", "QuadTreeLayerName"))))

        # If Light is enabled in settings then init the lightrenderer.
        if self.lightmodel != 0:
            renderer = fife.LightRenderer.getInstance(self.cameras['main'])
            renderer.setEnabled(True)
            renderer.clearActiveLayers()
            renderer.addActiveLayer(self.map.getLayer('ObjectLayer'))
            
            self._survivor_light_opts['radius'] = self.engine.getSettings().getScreenWidth() / 6
            
            self.updateLight()
            
            self.target_rotation = self.cameras['main'].getRotation()

    def updateLight(self):
        if self.lightmodel == 0:
            return
        renderer = fife.LightRenderer.getInstance(self.cameras['main'])
        renderer.removeAll("survivors")
        surv = self.agentlayer.getInstance('player')
        node = LightRendererNode(surv, self.agentlayer)
        self._survivor_light_node = node
        opts = self._survivor_light_opts
        renderer.addSimpleLight("survivors", node, opts['intensity'], opts['radius'],
                                opts['subdivs'], opts['xstretch'], opts['ystretch'],
                                opts['R'], opts['G'], opts['B'])
        c = self._global_light
        self.cameras['main'].setLightingColor(c['R'], c['G'], c['B'], c['A'])

    def reset(self):
        # if self.music:
        #     self.music.stop()
        self.map, self.agentlayer = None, None
        self.cameras = {}
        self.survivor, self.girl, self.clouds, self.beekeepers = None, None, [], []
        self.cur_cam2_x, self.initial_cam2_x, self.cam2_scrolling_right = 0, 0, True
        self.target_rotation = 0
        self.instance_to_agent = {}
        self.lightmodel = int(TDS.get("FIFE", "Lighting"))

    def pump(self):
        """
        Called every frame.
        """

        # Reset mouse cursor
	self.engine.getCursor().set(fife.CURSOR_NONE)
        self.engine.getCursor().setDrag(fife.CURSOR_IMAGE, self.cursor_image,
                                        self.cursor_x_offset, self.cursor_y_offset)

        self.survivor.update()

        for p in self.survivor.projectiles:
            if not p.created:
                continue

            if p.has_hit:
                p.layer.deleteInstance(p._instance)
                p.created = False
                continue

            p.update()

            # Collision detection for projectiles
            pos_old = p.get_last_position()
            pos = p.get_position()
            
            pt_loc = fife.Location(p.layer)
            
            # print "calling line points"
            def escapeLoop():
                for pt in line_points(pos_old, pos, 0.5):
    
                    pt_loc.setExactLayerCoordinates(pt)

                    ## Bottleneck: linear in number of objects on map
                    instances = p.layer.getInstancesAt(pt_loc,False)
                    
                    for i in instances:
                        if i.getObject().getId() in ('axe','player'):
                            continue
        
                        if i.isBlocking():
                            p.has_hit = True
                            # TODO: implement our own collison box, such
                            # that we can specify a more fine-grained
                            # collision detection than what FIFEs engine
                            # allows
                            if i.getObject().getId() in ('zombie'):
                                a  = self.instance_to_agent[i.getFifeId()]
                                a.take_damage(p.damage)
                                ## if the projectile can hit several zombies then remove this return
                                return
            escapeLoop()


        for zombie in self.zombies:
            zombie.update()

        # self.pump_ctr += 1

    def get_camera(self):
        return self.cameras['main']
