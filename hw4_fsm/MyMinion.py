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

class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle,Move,ShootTower,ShootBase]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		# self.states += [Move, Kill]
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
		print(targets)
		if len(targets) > 0:
			self.agent.changeState(Move, targets[0])
		else: 
			targets = self.agent.world.getEnemyNPCs(self.agent.getTeam())
			targets = sorted(targets, key=lambda x: distance(x.getLocation(), self.agent.getLocation()))
			if len(targets) > 0:
				self.agent.changeState(Move, targets[0])
		### YOUR CODE GOES ABOVE HERE ###
		return None

# Recommended states for a Minion are: 
# - move, 
# - attack tower, 
# - attack base, 
# - attack enemy minion, 
# - attack enemy hero. 
# These are suggestions and not all are strictly necessary.

# Targets are prioritized as follows: 
 	# - closest enemy tower, 
  	# - closest enemy base, 
   	# - closest enemy minion.
    
class Move(State):
	def __init__(self, agent, args=[]):
		State.__init__(self, agent, args)
		self.target = args[0]  # Target to move towards

	def enter(self, oldstate):
		State.enter(self, oldstate)
		# Start moving towards the target
		if self.target is not None:
			self.agent.navigateTo(self.target.getLocation())

	def execute(self, delta=0):
		State.execute(self, delta)
		# Check if the agent has reached the target
		if self.target in self.agent.getVisibleType(Tower) and distance(self.agent.getLocation(), self.target.getLocation()) < SMALLBULLETRANGE:
				self.agent.changeState(ShootTower, self.target)
		if self.target in self.agent.getVisibleType(Base) and distance(self.agent.getLocation(), self.target.getLocation()) < SMALLBULLETRANGE:
				self.agent.changeState(ShootBase, self.target)	
		if self.target in self.agent.getVisibleType(Minion) and distance(self.agent.getLocation(), self.target.getLocation()) < SMALLBULLETRANGE:
				self.agent.changeState(ShootMinion, self.target)	
		if self.target is not None and self.agent.getLocation() == self.target.getLocation():
			self.agent.changeState(Idle)


	def exit(self):
		State.exit(self)
		# self.agent.stopMoving()
		self.agent.navigateTo(self.target.getLocation())

class ShootTower(State):
	def __init__(self, agent, args=[]):
		State.__init__(self, agent, args)
		self.target = args[0]  
		self.agent.bulletclass = TowerBullet
		
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# Turn to face the tower
		self.agent.turnToFace(self.target.getLocation())

	def execute(self, delta=0):
		State.execute(self, delta)
		# Shoot at the tower
		self.agent.shoot()
		if self.target in self.agent.getVisibleType(Base) and distance(self.agent.getLocation(), self.target.getLocation()) < SMALLBULLETRANGE:
			self.agent.changeState(ShootBase, self.target)
		elif self.target.isAlive() == False:
			self.agent.changeState(Idle)

class ShootBase(State):
    def __init__(self, agent, args=[]):
        State.__init__(self, agent, args)
        self.target = args[0]  
        self.agent.bulletclass = BaseBullet
		
    def enter(self, oldstate):
        State.enter(self, oldstate)
        # Turn to face the base
        self.agent.turnToFace(self.target.getLocation())

    def execute(self, delta=0):
        State.execute(self, delta)
        # Shoot at the base
        self.agent.shoot()
        if self.target in self.agent.getVisibleType(Minion) and distance(self.agent.getLocation(), self.target.getLocation()) < SMALLBULLETRANGE:
            self.agent.changeState(ShootMinion, self.target)	
        if self.target.isAlive() == False:
            self.agent.changeState(Idle)

class ShootMinion(State):
    def __init__(self, agent, args=[]):
        State.__init__(self, agent, args)
        self.target = args[0]  
        self.agent.bulletclass = SmallBullet  
		
    def enter(self, oldstate):
        State.enter(self, oldstate)
        # Turn to face the minion
        self.agent.turnToFace(self.target.getLocation())

    def execute(self, delta=0):
        State.execute(self, delta)
        # Shoot at the minion
        self.agent.shoot()
    
        # Check if the minion is still alive
        if self.target.isAlive() == False:
            self.agent.changeState(Idle)

    
    

