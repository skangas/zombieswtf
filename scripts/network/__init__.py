# -*- coding: utf-8 -*-
########################################################################
# Copyright (C) 2011 The Unknown Horizons Team <team@unknown-horizons.org>
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

import platform
import os

def find_enet_module():
  type = platform.system().lower()

  arch = platform.architecture()[0]
  if arch == '32bit':
    arch = '86'
  elif arch == '64bit':
    arch = '64'
  else:
    assert False, "Failed to detect system architecture!"
  version = platform.python_version_tuple()
  dir = "%s-x%s" % (type, arch)

  dirpy = "%s-%s%s" % (dir, version[0], version[1])
  if os.path.exists(os.path.join(os.path.dirname(__file__), dirpy)):
    dir = dirpy

  try:
    arch_module = __import__(dir, globals(), locals(), fromlist=["enet"])
    return arch_module.enet
  except ImportError:
    pass
  raise ImportError("Failed to import enet. Maybe there is no version for your platform (%s)" % (dir))

class NetworkException(Exception):
  pass

class NotConnected(NetworkException):
  def __str__(self):
    return "Client is not connected"

class ClientException(NetworkException):
  pass

class AlreadyConnected(ClientException):
  pass

class NotInGameLobby(ClientException):
  pass

class NotInServerMode(ClientException):
  pass

class UnableToConnect(ClientException):
  pass

class CommandError(ClientException):
  pass

class FatalError(ClientException):
  pass
