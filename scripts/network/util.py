# -*- coding: utf-8 -*-
########################################################################
# Copyright (C) 2011 The Unknown Horizons Team <team@unknown-horizons.org>
# Copyright (C) 2011 Stefan Kangas
########################################################################
# This file is part of ZombiesWTF.
#
# ZombiesWTF is free software: you can redistribute it and/or modify
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
# ###################################################

import random

def randomUUID():
	"""Generate a random UUID."""
	return [ random.randint(0, 255) for dummy in range(0, 16) ]

def uuidToString(u):
	return "-".join(["%02x" * 4, "%02x" * 2, "%02x" * 2, "%02x" * 2,  "%02x" * 6]) % tuple(u)

def uuidFromString(s):
	s = s.replace('-', '')
	return [ int(s[i : i + 2], 16) for i in range(0, 32, 2) ]
