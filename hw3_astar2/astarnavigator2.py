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
import heapq


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
		# print("main", dest)
		if self.agent != None and self.world != None: 
			self.source = source
			self.destination = dest
			### Step 1: If the agent has a clear path from the source to dest, then go straight there.
			### Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
			### Tell the agent to move to dest
			
			hold = clearShot(source, dest, self.world.getLinesWithoutBorders(), self.world.getPoints(), self.agent)
			# print("main clear",hold)
			if hold:
				self.agent.moveToTarget(dest)
			else:
				### Step 2: If there is an obstacle, create the path that will move around the obstacles.
				### Find the path nodes closest to source and destination.
				start = getOnPathNetwork(source, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
				end = getOnPathNetwork(dest, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
				# print("start",start)
				# print("end",end)
				if start != None and end != None:
					### Remove edges from the path network that intersect gates
					newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates(), self.world)
					# print("\n",newnetwork)
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


def offSets(node1, node2, agent_radius):
    # Offset by the agent's radius in both horizontal and vertical directions
    offsetNode1Top = (
        node1[0],
        node1[1] + agent_radius
    )
    offsetNode2Top = (
        node2[0],
        node2[1] + agent_radius
    )
    offsetNode1Bottom = (
        node1[0],
        node1[1] - agent_radius
    )
    offsetNode2Bottom = (
        node2[0],
        node2[1] - agent_radius
    )

    offsetNode1Right = (
        node1[0] + agent_radius,
        node1[1]
    )
    offsetNode2Right = (
        node2[0] + agent_radius,
        node2[1]
    )

    offsetNode1Left = (
        node1[0] - agent_radius,
        node1[1]
    )
    offsetNode2Left = (
        node2[0] - agent_radius,
        node2[1]
    )

    return {
        "top": (offsetNode1Top, offsetNode2Top),
        "bottom": (offsetNode1Bottom, offsetNode2Bottom),
        "right": (offsetNode1Right, offsetNode2Right),
        "left": (offsetNode1Left, offsetNode2Left)
    }

### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent, offset_nodes=None):
    if offset_nodes is None:
        offset_nodes = offSets(p1, p2, agent.getMaxRadius())

    for offset1, offset2 in offset_nodes.values():
        hit = rayTraceWorldNoEndPoints(offset1, offset2, worldLines)
        if hit is not None:
            return False

    return True

def hitsObstacles(p1, p2, lines):
    hit = rayTraceWorldNoEndPoints(p1, p2, lines)
    if hit == p1 or hit == p2:
        return False
    return hit

### Given a location, find the closest pathnode that the agent can get to without collision
### agent: the agent
### location: the location to check from (typically where the agent is starting from or where the agent wants to go to) as an (x, y) point
### pathnodes: a list of pathnodes, where each pathnode is an (x, y) point
### world: pointer to the world
def getOnPathNetwork(location, pathnodes, worldLines, agent):
    closest_node = None
    min_distance = float('inf')  # Initialize with infinity

    for node in pathnodes:
        if clearShot(location, node, worldLines, [], agent):
            # print("Location 1", location)
            # print("node",node)
            dist = distance(location, node)
            if dist < min_distance:
                closest_node = node
                min_distance = dist

    return closest_node

### Implement the a-star algorithm
### Given:
### Init: a pathnode (x, y) that is part of the pathnode network
### goal: a pathnode (x, y) that is part of the pathnode network
### network: the pathnode network
### Return two values: 
### 1. the path, which is a list of states that are connected in the path network
### 2. the closed list, the list of pathnodes visited during the search process
# def astar(init, goal, network):
#     path = []
#     open_list = []
#     closed = set()
#     closed.add(init)

#     while init != goal:
#         neighbors = [node for edge in network for node in edge if init in edge and node != init]
#         neighbors.sort(key=lambda node: distance(node, goal))
#         next_node = None

#         for neighbor in neighbors:
#             if neighbor not in closed:
#                 next_node = neighbor
#                 break
#         if next_node:
#             path.append(next_node)
#             open_list.append(next_node)
#             closed.add(next_node)
#             init = next_node
#         else:
#             break

#     return path, closed
def backTrack(trackNodes, currentNode, parentNode):
	path = []
	while currentNode is not None:
		path.append(currentNode)
		currentNode = parentNode

		if parentNode is None:
			break
		else:
			parentNode = next((tn[2] for tn in trackNodes if tn[1] == parentNode), None)
	path.reverse()
 
	return path
def astar(init, goal, network):


    path = []
    open = [(0, init, None)]
    close = []
    visited = copy.deepcopy(open)

    while open:
        holdScore, currentNode, parentNode = heapq.heappop(open)
        
        if currentNode == goal:
            path = backTrack(visited, currentNode, parentNode)
            return path, close

        visited.append((holdScore, currentNode, parentNode))
        close.append(currentNode)

        for edge in network:
            if currentNode in edge:
                nextNode = edge[1] if currentNode == edge[0] else edge[0]
                if nextNode not in close:
                    holdScore = distance(nextNode, init)
                    hScore = distance(nextNode, goal)
                    fScore = holdScore + hScore
                    heapq.heappush(open, (fScore, nextNode, currentNode))

    return path, close

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
# ### Gets called after every agent.update()
# ### self: the navigator object
# ### delta: time passed since last update
tiempo = 0
def myUpdate(nav, delta):
    global tiempo
    tiempo += delta
    if tiempo > 100:
        myCheckpoint(nav)
    return None

def myCheckpoint(nav):
    global tiempo
    tiempo = 0
    currPos = nav.agent.position
    target = nav.agent.moveTarget
    agent_radius = nav.agent.getMaxRadius()
    # print("path calling",nav.path)
    if rayTraceWorld(currPos, target, nav.world.getLinesWithoutBorders()):
        nav.computePath(currPos, nav.destination)
    elif nav.path and len(nav.path) > 2:
        if rayTraceWorld(nav.path[0], nav.path[1], nav.world.getLinesWithoutBorders()):
            nav.computePath(currPos, nav.destination)
    return None




### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
    pathCopy = copy.deepcopy(path)
    agentRadius = agent.getMaxRadius()
    
    if clearShot(source, dest, world.getLinesWithoutBorders(), [], agent):
        return []

    pathCopy = [source] + pathCopy + [dest]

    for currentIdx in range(len(pathCopy)):
        nextIdx = currentIdx + 2
        while nextIdx < len(pathCopy):
            if clearShot(pathCopy[currentIdx], pathCopy[nextIdx], world.getLinesWithoutBorders(), [], agent):
                pathCopy.pop(nextIdx - 1)
            else:
                nextIdx += 1

    pathCopy.remove(source)
    pathCopy.remove(dest)

    return pathCopy



### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
	### YOUR CODE GOES BELOW HERE ###
	
	### YOUR CODE GOES ABOVE HERE ###
	return False