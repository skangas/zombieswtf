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

import time

class ExtScheduler(object):
	"""The ExtScheduler is used for time based events that are not part of
	the simulation(gui, menu, scrolling). To start a timed callback, call
	add_new_object() to make the TimingThread Class create a CallbackObject
	for you. @param pump: pump list the scheduler registers itself with.
	"""

	def __init__(self, pump):
		super(ExtScheduler, self).__init__()
		self.schedule = []
		self.pump = pump
		self.pump.append(self.tick)

	def tick(self):
		"""Threads main loop
		@param tick_id: int id of the tick.
		"""
		# loop through schedule until an object doesn't match the time criteria
		for tup in self.schedule:
			if tup[0] <= time.time():
				obj = self.schedule.pop(0)[1]
				obj.callback()
				if obj.loops > 0 or obj.loops is -1:
					self.add_object(obj) # re-add object
			else:
				break

	def add_object(self, obj):
		"""Adds a new CallbackObject instance to the callbacks list
		@param object: CallbackObject type object, containing all necessary  information
		"""
		if obj.loops > 0:
			obj.loops -= 1
		self.schedule.append(((time.time() + obj.run_in), obj))
		self.schedule.sort()

	def add_new_object(self, callback, class_instance, run_in=1, loops=1):
		"""Creates a new CallbackObject instance and calls the self.add_object() function.
		@param callback: function callback, which is called run_in time.
		@param class_instance: class instance the function belongs to.
		@param run_in: float number of seconds after which the callback is called. Standard is 1, run next second.
		@param loops: How often the callback is called. -1 = infinite times. Standard is 1, run once."""
		obj = CallbackObject(callback, class_instance, run_in, loops)
		self.add_object(obj)

	def rem_all_classinst_calls(self, class_instance):
		"""Removes all callbacks from the scheduler that belong to the class instance class_inst."""
		for tup in self.schedule:
			if tup[1].class_instance is class_instance:
				self.schedule.remove(tup)

	def rem_call(self, instance, callback):
		"""Removes all callbacks of 'instance' that are 'callback'
		@param instance: the instance that would execute the call
		@param callback: the function to remove
		"""
		for tup in self.schedule:
			if tup[1].class_instance is instance and tup[1].callback == callback:
				self.schedule.remove(tup)

	def __del__(self):
		self.schedule = []
		self.pump.remove(self.tick)
		self.pump = None


class CallbackObject(object):
	"""Class used by the ExtScheduler Class to organize callbacks."""
	def __init__(self,  callback, class_instance, run_in=1, loops=1):
		"""Creates the CallbackObject instance.
		@param callback: lambda function callback, which is called run_in ticks.
		@param class_instance: class instance the original function(not the lambda function!) belongs to.
		@param run_in: int number of ticks after which the callback is called. Standard is 1, run next tick.
		@param loops: How often the callback is called. -1 = infinite times. Standard is 1, run once.
		"""
		self.callback = callback
		self.class_instance = class_instance
		self.run_in = run_in
		self.loops = loops

