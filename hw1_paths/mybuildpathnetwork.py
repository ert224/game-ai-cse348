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
# Erick Tepan
# ert224
# cse348 
# hw1
'''
core.py
Member Funcs
-	getPoints() returns a list of all  the corners of all the obstables (and the lines of the screen) 
	A point is a tuple of the form (x,y)

-	getLines() returns a list of all the lines of all obstacles (and screen boundries). 
	A line is a touple of the form (point1,point2) where points boundries are touples of the form (x,y)

- 	getLinesWithoutBorders() returns a list of all the lines of the obstables, but does not include screen boundries 

-	getObstables() returns a list of obstacles which are of type Obstable. 

-	getDimensions() returns the (x,y) - dimensions of the world 


Obstacle
Member Funcs

-	getPoints() returns a list of all corners in the polygon. A point is a touple of the form(x,y)
-	getLines() returns a  list of all lines in the polygon. A line is a tuple of the form (point1,point2)
	where points are touples of the form(x,y)

- pointInside(point) returns true if a point (x,y) is inside the obstacle 

Agent aka player
Member Vars
	move in straight line to locations
	Navigator sub comp to avoid obstacles 
- 	moveTarget() the (x,y) point to which the Agent has been instructed to move to. 
	Used for interpolating the Agents current possition ar any given tick
-	navigator : an object that tells the agent how to move

Member Funcs
-	moveToTarget(point) Instruct the Agent to move straight to the point (x,y), ignoring the existence of obstacles 
- 	navigateTo() Instructs Agent to create a path through the environment that avoids collitions. 
	This function invokes the navigators computePath() functionality

-	isMoving() returns true if the agent is currently moving
-	getMoveTarget() returns the point that the agent is currently moving towards 
-	stopMoving() stop agent from moving 

Navigators 
member vars
-	agent - pointer back to the agent object that is being guided by the AI
- 	world - pointer to the GameWorld object 
-	source - the point (x,y) to which the Agent must traverse
-	path - a list of points to traverse in order that is guaranteed not results  in a collison  with an obstacles 

member funcs
-	computePath(source,destination) find a path through the terrain (causing path to be not None) and call back to the Agent to start moving. 
	this default functionality just instructs  the agent to move straight to the destination. This function will be overriden by sub-classes
	implementing particular  path planning techniques 

-	doneMoving() the Navigator invokes this function when the agent has reached its moveTarget. 
	doneMoving contains logic to determine what to do next.
	if there is a path, it will select the next point in the path as the next moveTarget and call back to the Agent 

-	checkpoint() called when the Agent reaches a point on the path
- 	smooth() optimizes the path to take shortcuts whenever possible and thereby create smoother, more efficient motion 

Pathnetwork navigator
member vars
-	pathnodes - a list of points of the form (x,y) that compromise a path network.
-	pathNetwork -	a list of lines of the form ((x1,y1),(x2,y2)) that comprise a path network

Member funcs
-	computePath(source,destination) find a path through the path network (causing path to be not None) and call back to the Agent
	to start moving. This default function just instructs the agent to move to the destination.

Random Navigatior randomnavigator.py
Member functions
-	computePath(source,destination) Find a path through the path network (causing path to be not None), and call back to the aganet to start
	moving. This default functionality just instructs the agent to move to the destination. 
	The path is created by finding the closet path nodes to the source and then the randomly selecting sucessor path nodes in the path 
	network until the closet node to the destination is found. 
	If the path length exceeds 100, then the Agent will be sent to its destination without further collision avoidance.

Miscellaneous Utils funcs
-	distance(point1,point2) returns the distance between two points. Points are tuples of the form(x,y)
- 	calculateIntersectPoint (point1,point2,point3,point4) return a point (x,y) at the intersection of two lines or None if the lines are 
	parallel. One line is in between point1 and point2 and the other line is between point3 and the point4
-	rayTrace(point1,point2,line) return a point (x,y) if a beam between point1 and point2 cross the given line
-	rayTraceWorld(point1,point2,worldline) performs a ray trace against every line in worldlines and return the first intersection point found.
	wordlines is a list of lines of the form ((x1,y1)(x2,y2)).
-	rayTraceNoEndPoints(point1,point2,line) same as rayTrace() but doesnt check collisions with the end points of the two lines
-	rayTraceWorldNoEndPoints(point1,point2,worldlines)same as rayTraceWorld() but doesnt check end points of any lines compared against each other
-	pointInsidePolygonLines(point,lines) return true if point is within a polygon defined by listofpoints 
	point is of the form (x,y). Lines is a list of the form ((x1,y1)(x2,y2))
-	drawCross(surface,point,color,size,width) draw a cross on the PyGame drawing surface.
	point is the center of the cross, a tuple of the form(x,y). Color is a tuple of the form (red,green,blue) with values between 0 and 255 each.
	size is the length of the lines in the cross. width is the with of the lines.

-	minimumDistance(line,point) returns the shortest distance between a point(x,y) and a line ((x1,y1)(x2,y2))
-	findClosestUnobstructed(point,nodes,lines) returns the point in nodes that is closest to the given point for which none of the given lines
	comes between the found point and the given point. 

- 	agent.getMaxRadius() for the agents physical size 
'''
import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates the path network as a list of lines between all path nodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent=None):
    lines = []  
    agent_radius = agent.getMaxRadius() # Get the agent's physical size
    # print(agent_radius)
    # print(agent_radius*2)
    
    # check for obstacles
    def hasObstacleBetween(point1, point2):
        for obstacle in world.obstacles:
            # for edge in obstacle.getLines():
                if not (rayTraceWorld(point1, point2, list(obstacle.getLines())) is None):
                    return True
        return False
    
    for i in range(len(pathnodes)):
        for j in range(i + 1, len(pathnodes)):
            node1 = pathnodes[i]
            node2 = pathnodes[j]
            # print(node1, node2)

            # Check for obstacles between the given line 
            if not hasObstacleBetween(node1, node2):
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

                # Check for enough space on all sides 
                if (not hasObstacleBetween(offsetNode1Top, offsetNode2Top) and not hasObstacleBetween(offsetNode1Bottom, offsetNode2Bottom) and
                    not hasObstacleBetween(offsetNode1Right, offsetNode2Right) and not hasObstacleBetween(offsetNode1Left, offsetNode2Left)):
                    lines.append((node1, node2))

    return lines
