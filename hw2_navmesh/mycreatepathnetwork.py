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

import logging
import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *
from itertools import permutations, combinations

from utils_navmesh import NavMeshUtils
    


def hitsObstacles(p1, p2, lines):
    hit = rayTraceWorldNoEndPoints(p1, p2, lines)
    if hit == p1 or hit == p2:
        return False
    return hit

def checkInsidePoints(poly, worldPoints):
    for point in worldPoints:
        lista = pointInsidePolygonPoints(point, poly)
        if lista:
            return False
    return True   
def checkSubsetPoly(worldObstacles,triangle):
	for obstacle in set(worldObstacles):
		obstSet = set(obstacle.getPoints())
		if set(triangle).issubset(obstSet):
			return False
	return True
def checkSubsetPolyList(polyList,triangle):
	if set(triangle).issubset(polyList):
		return False
	return True
def appendTriangleNoDuplicates(triangle, polys):
    # Check permutations of the triangle to avoid duplicates
    for permut in permutations(triangle):
        if polys.count(permut):
            return  # Triangle already exists in the list, so we don't append it
    polys.append(triangle)
    return polys

def printObstacle(obstacles):
	for obstacle in obstacles:
		for edge in obstacle.getPoints():
			print(edge)

# Creates a path node network that connects the midpoints of each nav mesh together
def myCreatePathNetwork(world, agent = None):
	nodes = [] 
	
	edges = []
	# blue lines   
	polys = []
	#  green polygons (triangles)

	# you don't strictly speaking need to use these. But we include in case they help you get started.
	obstacleLines = world.getLines()[4:] # the first four (i.e. 0-3) are the screen edges; this gets all but those
	worldLines = list(set(world.getLines()))
	worldPoints = world.getPoints()
	worldObstacles = world.getObstacles()
	numPoints = len(worldPoints)
	lineDict = []
	polySet = set() 
 	# Probably good for holding ManualObstacle instances
	print(worldLines)
	for x in worldPoints:
		for y in filter(lambda i, a=x: a != i, worldPoints):
			for z in filter(lambda i, a=x, b=y: a != i and i != b, worldPoints):
				triangle = (x, y, z)
				if checkSubsetPoly(worldObstacles,triangle):
					if not hitsObstacles(x, y, lineDict) and not hitsObstacles(x, z, lineDict) and not hitsObstacles(y, z, lineDict) and not hitsObstacles(y, z, worldLines) and not hitsObstacles(x, y, worldLines) and not hitsObstacles(x, z, worldLines):
						inside_points = filter(lambda i, a=x, b=y, c=z: a != i and i != b and i != c, worldPoints)
						if checkInsidePoints(triangle, inside_points):
							polys.append(triangle)
						appendLineNoDuplicates((x, y), lineDict)
						appendLineNoDuplicates((x, z), lineDict)
						appendLineNoDuplicates((y, z), lineDict)
    # Ensure triangles do not get made inside objects
	# print(polys)
	# print('\n dic lines')
	# print(lineDict)
	# print('\n world obs')
	# print(type(worldObstacles))
	# # print(worldObstacles)
	# printObstacle(worldObstacles)
	# hint 0: to iterate over a collection, the `range` function is useful. E.g. `for i in range(numPoints):`
	#
	# hint 1: We can represent a triangle as a tuple of three worldPoints: triangle = (p1, p2, p3)
	#    Tuples in python are not limited to three elements
	#
	# hint 2: It may be useful to use the ManualObstacle class to help manage complexity. E.g. ManualObstacle(triangle)
	#    Because ManualObstacle is a Obstacle, you have helper methods like draw, getLines, getPoints, and pointInside
	#
	# hint 3: for debugging, it can also be useful to 'draw' centroids of hulls, e.g. NavMeshUtils.drawCentroids(world, polySet)

	### YOUR CODE GOES BELOW HERE ###

	# Any and all of these comments before "YOUR CODE GOES ABOVE HERE" can be deleted. They are meant to help, but may not.
	
	# HW TODO: Create triangles that don't intersect with each other or obstacles.
		# You may need to make sure no obstacles are completely inside the triangle.
		# You may need to register the triangle's lines for later use (when merging).

	# HW TODO: Now merge triangles in a way that preserves convexity.

	# HW Hint: Now might be a good time to NavMeshUtils.drawCentroids(world, polySet)
	# NavMeshUtils.drawCentroids(world, polySet)

	# HW TODO: Create the final nav mesh and create cliques out of the boundaries of each polygon.
		# Decide how you will use the boundaries and centroid of the polygon as nodes.
		# For example, if the polygon has more than 3 sides, you may just send a line from each edge to the middle
		# Note: you can link borders directly in polygons or if the centroid is unusable.
			# NB: Don't try to link a border to itself!

	# We should only return nodes that the agent can reach on the path network.
	# Suggestion: consider using a BFS of sorts to get a connected graph.

	### YOUR CODE GOES ABOVE HERE ###
	return nodes, edges, polys

