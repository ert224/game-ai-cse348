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



###############################
### AStarNavigator2
###
### Creates a path node network and implements the A* algorithm to create a path to the given destination.
			
class AStarNavigator2(PathNetworkNavigator):

				
	### Finds the shortest path from the source to the destination using A*.
	### self: the navigator object
	### source: the place the agent is starting from (i.e., its current location)
	### dest: the place the agent is told to go to
	def computePath(self, source, dest):
		self.setPath(None)
		### Make sure the next and dist matrices exist
		if self.agent != None and self.world != None: 
			self.source = source
			self.destination = dest
			### Step 1: If the agent has a clear path from the source to dest, then go straight there.
			### Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
			### Tell the agent to move to dest
			if clearShot(source, dest, self.world.getLinesWithoutBorders(), self.world.getPoints(), self.agent):
				self.agent.moveToTarget(dest)
			else:
				### Step 2: If there is an obstacle, create the path that will move around the obstacles.
				### Find the path nodes closest to source and destination.
				start = getOnPathNetwork(source, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
				end = getOnPathNetwork(dest, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
				print("start",start)
				print("end",end)
				if start != None and end != None:
					### Remove edges from the path network that intersect gates
					newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates(), self.world)
					print("\n",newnetwork)
					closedlist = []
					### Create the path by traversing the pathnode network until the path node closest to the destination is reached
					path, closedlist = astar(start, end, newnetwork)
					if path is not None and len(path) > 0:
						### Determine whether shortcuts are available
						path = shortcutPath(source, dest, path, self.world, self.agent)
						### Store the path by calling self.setPath()
						self.setPath(path)
						if self.path is not None and len(self.path) > 0:
							### Tell the agent to move to the first node in the path (and pop the first node off the path)
							first = self.path.pop(0)
							self.agent.moveToTarget(first)
		return None
		
	### Called when the agent gets to a node in the path.
	### self: the navigator object
	def checkpoint(self):
		myCheckpoint(self)
		return None

	### This function gets called by the agent to figure out if some shortcuts can be taken when traversing the path.
	### This function should update the path and return True if the path was updated.
	def smooth(self):
		return mySmooth(self)

# Dont have to wait to reach a node to update 
	def update(self, delta):
		myUpdate(self, delta)



### Removes any edge in the path network that intersects a worldLine (which should include gates).
def unobstructedNetwork(network, worldLines, world):
	newnetwork = []
	for l in network:
		hit = rayTraceWorld(l[0], l[1], worldLines)
		if hit == None:
			newnetwork.append(l)
	return newnetwork



### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
    for line in worldLines:
        if rayTraceWorldNoEndPoints(p1, p2, [line]) is not None:
        	# path is blocked
            return False  
    agent.moveToTarget(p2)
    return True

# Function to check for obstacles between two points
def hasObstacleBetween(point1, point2, worldLines):
	for line in worldLines:
		if rayTraceWorld(point1, point2, [line]) is not None:
			return True  # Obstacle detected
	return False

### Given a location, find the closest pathnode that the agent can get to without collision
### agent: the agent
### location: the location to check from (typically where the agent is starting from or where the agent wants to go to) as an (x, y) point
### pathnodes: a list of pathnodes, where each pathnode is an (x, y) point
### world: pointer to the world
def getOnPathNetwork(location, pathnodes, worldLines, agent):
    sortedNodes = sorted(pathnodes, key=lambda p: distance(location, p))
    for node in sortedNodes:
        if not hasObstacleBetween(location, node, worldLines):
    		# Return the closest reachable path node
            return node  
	### YOUR CODE GOES ABOVE HERE ###
    return None  # Return None if no reachable path node is found

def clashesWithObstacle(point1, point2, obstacles):
	for obstacle in obstacles:
			if not (rayTraceWorld(point1, point2, list(obstacle.getLines())) is None):
				return True # yes there is an obstacle 
	return False  # no there is no obstacle between the two points 

### Implement the a-star algorithm
### Given:
### Init: a pathnode (x, y) that is part of the pathnode network
### goal: a pathnode (x, y) that is part of the pathnode network
### network: the pathnode network
### Return two values: 
### 1. the path, which is a list of states that are connected in the path network
### 2. the closed list, the list of pathnodes visited during the search process
def astar(init, goal, network):
    path = []
    open_list = []
    closed = set()
    closed.add(init)

    while init != goal:
        neighbors = [node for edge in network for node in edge if init in edge and node != init]
        neighbors.sort(key=lambda node: distance(node, goal))
        next_node = None

        for neighbor in neighbors:
            if neighbor not in closed:
                next_node = neighbor
                break

        if next_node:
            path.append(next_node)
            open_list.append(next_node)
            closed.add(next_node)
            init = next_node
        else:
            break

    return path, closed


# Navigator
### Path: the planned path of nodes
### World: a pointer to the world object
### Agent: the agent doing the navigation
### source: where starting from
### destination: where trying to go

# Agent
### moveTarget: where to move to. Setting this to non-None value activates movement (update fn)
### moveOrigin: where moving from.
### navigator: model that does path planning
### firerate: how often agent can fire
### firetimer: how long since last firing
### canfire: can the agent fire?
### hitpoints: amount of damage the agent can take
### team: symbol referring to the team (or None)
### distanceTraveled: the total amount of distance traveled by the agent

#world 
### Gates: lines (p1, p2) where gates can appear
### timer: running timer
### alarm: when timer is greater than this number, gate switches
### gate: the active gate

def myCheckpoint(nav):
    # agent = nav.agent
    # world = nav.world
    # source = nav.source
    # desPath = nav.path
    # dest = nav.destination
    # move_target = agent.getMoveTarget()

    # # Check if the entire path is still valid
    # path_valid = True
    # for i in range(len(desPath) - 1):
    #     point1 = desPath[i]
    #     point2 = desPath[i + 1]
    #     if hasObstacleBetween(point1, point2, world.getLines()) or hasObstacleBetween(point1, point2, world.getLinesWithoutBorders()):
    #         path_valid = False
    #         break

    # if not path_valid:
    #     # Create a new path
    #     new_path = getOnPathNetwork(source, dest, world.getLines(), world.getLinesWithoutBorders())
    #     if new_path:
    #         agent.setPath(new_path)
    #         return
    #     else:
    #         # No valid path found, stop moving
    #         agent.stopMoving()
    # else:
    #     # Check if the next path node is still reachable
    #     if move_target is not None:
    #         if hasObstacleBetween(agent.moveOrigin, move_target, world.getLines()) or hasObstacleBetween(agent.moveOrigin, move_target, world.getLinesWithoutBorders()):
    #             # Next node is not reachable, create a new path
    #             new_path = agent.navigator.findPath(source, dest, world.getLines(), world.getLinesWithoutBorders())
    #             if new_path:
    #                 agent.setPath(new_path)
    #             else:
    #                 # No valid path found, stop moving
    #                 agent.stopMoving()

    return None


# ### Gets called after every agent.update()
# ### self: the navigator object
# ### delta: time passed since last update
def myUpdate(nav, delta):
    agent = nav.agent
    world = nav.world
    source = nav.source
    desPath = nav.path
    dest = nav.destination
    moveTarget = agent.moveTarget
    print("agent:", agent)
    print("world", world)
    print("sourve",source)
    print("desPath", desPath)
    print("destiation", dest)
    if moveTarget is not None:
        if hasObstacleBetween(agent.moveOrigin, moveTarget, world.getLines()):
            # Next node is not reachable, create a new path
            new_path = getOnPathNetwork(source, (dest[0],dest[1]), world.getLines(), world.getLinesWithoutBorders())
            agent.setPath(new_path)
    return None








### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
	path = copy.deepcopy(path)
	### YOUR CODE GOES BELOW HERE ###
	
	### YOUR CODE GOES BELOW HERE ###
	return path


### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
	### YOUR CODE GOES BELOW HERE ###
	
	### YOUR CODE GOES ABOVE HERE ###
	return False

