#!/usr/bin/env python

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

# Start Zombies WTF

import sys, os, re, math, random, shutil

from fife import fife
print "Using the FIFE python module found here: ", os.path.dirname(fife.__file__)

from scripts.application import ZombiesWTF
from fife.extensions.fife_settings import Setting

TDS = Setting(app_name="zombieswtf")

def main():
        app = ZombiesWTF()
        app.run()

if __name__ == '__main__':
        if TDS.get("FIFE", "ProfilingOn"):
                import hotshot, hotshot.stats
                print "Starting profiler"
                prof = hotshot.Profile("fife.prof")
                prof.runcall(main)
                prof.close()
                print "analysing profiling results"
                stats = hotshot.stats.load("fife.prof")
                stats.strip_dirs()
                stats.sort_stats('time', 'calls')
                stats.print_stats(20)
        else:
                if TDS.get("FIFE", "UsePsyco"):
                        # Import Psyco if available
                        try:
                                import psyco
                                psyco.full()
                                print "Psyco acceleration in use"
                        except ImportError:
                                print "Psyco acceleration not used"
                else:
                        print "Psyco acceleration not used"
                main()
