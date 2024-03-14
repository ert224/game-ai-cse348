'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from moba import *

class BaselineMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		self.states += [Move, Kill]
		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.world.computeFreeLocations(self)
		self.changeState(Idle)





############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		targets = self.agent.world.getEnemyTowers(self.agent.getTeam())
		targets = sorted(targets, key=lambda x: distance(x.getLocation(), self.agent.getLocation()))
		targets = targets + self.agent.world.getEnemyBases(self.agent.getTeam())
		if len(targets) > 0:
			self.agent.changeState(Move, targets[0])
		### YOUR CODE GOES ABOVE HERE ###
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print("Hey " + str(self.victim) + ", I don't like you!")
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:

class Move(State):
	
	def __init__(self, agent, args = []):
		State.__init__(self, agent, args)
		self.target = args[0]
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# start moving
		if self.target is not None:
			self.agent.navigateTo(self.target.getLocation())

	def execute(self, delta = 0):
		State.execute(self, delta)
		if self.target is not None:
			visibleMinions = self.agent.getVisibleType(Minion)
			targetMinions = []
			for m in visibleMinions:
				if m.getTeam() != self.agent.getTeam():
					targetMinions.append(m)
#			if self.agent.getHitpoints() <= self.agent.getMaxHitpoints()/5:
#				self.agent.changeState(Heal)
			if self.target in self.agent.getVisibleType(Tower) and distance(self.agent.getLocation(), self.target.getLocation()) < SMALLBULLETRANGE:
				self.agent.changeState(Kill, self.target)
			elif self.target in self.agent.getVisibleType(Base) and distance(self.agent.getLocation(), self.target.getLocation()) < SMALLBULLETRANGE:
				self.agent.changeState(Kill, self.target)
			elif self.agent.getMoveTarget() == None and self.target is not None:
				self.agent.navigateTo(self.target.getLocation())
			'''
			elif len(targetMinions) > 0:
				for m in targetMinions:
					if distance(self.agent.getLocation(), m.getLocation()) < SMALLBULLETRANGE:
						self.agent.turnToFace(targetMinions[0].getLocation())
						self.agent.shoot()
						break
			'''

	def exit(self):
		State.exit(self)
		self.agent.stopMoving()

class Kill(State):
	
	def __init__(self, agent, args = []):
		State.__init__(self, agent, args)
		self.target = args[0]
	
	def execute(self, delta = 0):
		State.execute(self, delta)
#		if self.agent.getHitpoints() <= self.agent.getMaxHitpoints()/5:
#			self.agent.changeState(Heal)
		if self.target is not None and self.target.isAlive():
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()
		elif self.target.isAlive() == False:
			self.agent.changeState(Idle)

class Heal(State):

	def enter(self, oldstate):
		State.enter(self, oldstate)
		if self.agent.getOwner() is not None:
			self.agent.navigateTo(self.agent.getOwner().getLocation())

	def execute(self, delta = 0):
		State.execute(self, delta)
		if self.agent.getHitpoints() == self.agent.getMaxHitpoints():
			self.agent.changeState(Idle)
