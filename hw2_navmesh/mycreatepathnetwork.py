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
    



def isInsideObstacle(poly, worldPoints):
    for point in worldPoints:
        lista = pointInsidePolygonPoints(point, poly)
        if lista:
            return False
    return True   

def checkSubsetPolyList(polyList,triangle):
	if set(triangle).issubset(polyList):
		return False
	return True

def printObstacle(obstacles):
	for obstacle in obstacles:
		for edge in obstacle.getPoints():
			print(edge)


def is_clockwise(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0
   

 
def checkSubsetPoly(worldObstacles,triangle):
	for obstacle in set(worldObstacles):
		obstSet = set(obstacle.getPoints())
		if set(triangle).issubset(obstSet):
			return False
	return True

# check for obstacles
def hasObstacleBetween(point1, point2, world):
	for obstacle in world.obstacles:
			if not (rayTraceWorld(point1, point2, list(obstacle.getLines())) is None):
				return True # yes there is an obstacle 
	return False  # no there is no obstacle between the two points 
def clashesWithObstacle(point1, point2, obstacles):
	for obstacle in obstacles:
			if not (rayTraceWorld(point1, point2, list(obstacle.getLines())) is None):
				return True # yes there is an obstacle 
	return False  # no there is no obstacle between the two points 

def hasObstacleLines(point1, point2, world):
	for obstacle in world.obstacles:
			if not (rayTraceWorld(point1, point2, list(obstacle.getLines())) is None):
				return True
	return False  
 
def hitsObstacles(p1, p2, lines):
    hit = rayTraceWorldNoEndPoints(p1, p2, lines)
    if hit == p1 or hit == p2:
        return False
    return hit
def triangleHitsObs(x,y,z,lines):
	return not hitsObstacles(y, z, lines) and not hitsObstacles(x, y, lines) and not hitsObstacles(x, z, lines)
    

def getAngle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def sortCounterClockwise(points):
    center = tuple(map(sum, zip(*points)))  # Calculate the centroid as the center point
    center = (center[0] / len(points), center[1] / len(points))
    sorted_points = sorted(points, key=lambda point: getAngle(center, point))
    return sorted_points

# def mergePolys(polySet):
    
#     merged = set()
#     for poly in set(polySet):
#         for poly2 in filter(lambda x: x != poly, polySet):
#             if polygonsAdjacent(poly.getPoints(), poly2.getPoints()):
#                 holdPoints = sortCounterClockwise(set(poly.getPoints() + poly2.getPoints()))
#                 if isConvex(holdPoints):
#                     if checkSubsetPoly(polySet, holdPoints):
#                         manualObstacle = ManualObstacle(holdPoints)
#                         merged.add(manualObstacle)
#     holdMerge = set() 
#     counter = 0                  
#     for poly in merged:
#         # print("\n",poly.getPoints())
#         for poly2 in merged:
#             if poly2 == poly:
#                 # print('same\t', poly2.getPoints())
#                 continue
#             # print()
#             for p in range(1,len(poly2.getPoints())):
#                 # print(poly.getPoints()[p-1],poly.getPoints()[p])
#                 if not hitsObstacles(poly.getPoints()[p-1],poly.getPoints()[p],poly2.getLines()):
#                     holdMerge.add(poly)
       
#     return holdMerge

def mergePolys(polySet):
    merged = set()
    for triangle1 in polySet:
        for triangle2 in filter(lambda x: x != triangle1, polySet):
            for triangle3 in filter(lambda x: x != triangle2 and x != triangle1, polySet):
                # Check if the triangles share two edges
                if (polygonsAdjacent(triangle1.getPoints(), triangle2.getPoints()) and 
                    polygonsAdjacent(triangle1.getPoints(), triangle3.getPoints())):
                    # Merge the points and create a new ManualObstacle if the resulting polygon is convex and not already in merged
                    holdPoints = sortCounterClockwise(set(triangle1.getPoints() + triangle2.getPoints()+ triangle3.getPoints()))
                    if isConvex(holdPoints) and checkSubsetPoly(merged, holdPoints):
                        print(holdPoints)
                        manualObstacle = ManualObstacle(holdPoints)
                        merged.add(manualObstacle)
    return merged


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def create_lines(points, worldObstacles, agent_radius):
    lines = []
    visited = set()
    savedPoint = points[0]
    visited.add(savedPoint)
    exitCounter = len(points)
    previous_points = []  # To keep track of previous points
    
    while exitCounter:
        closestPoints = sorted(points, key=lambda p: distance(savedPoint, p))
        closest_point = None
        for currPoint in closestPoints:
            if currPoint not in visited:
                if not clashesWithObstacle(savedPoint, currPoint, worldObstacles):
                    offsetcenter1Top = (savedPoint[0], savedPoint[1] + agent_radius)
                    offsetcenter2Top = (currPoint[0], currPoint[1] + agent_radius)
                    offsetcenter1Bottom = (savedPoint[0], savedPoint[1] - agent_radius)
                    offsetcenter2Bottom = (currPoint[0], currPoint[1] - agent_radius)
                    offsetcenter1Right = (savedPoint[0] + agent_radius, savedPoint[1])
                    offsetcenter2Right = (currPoint[0] + agent_radius, currPoint[1])
                    offsetcenter1Left = (savedPoint[0] - agent_radius, savedPoint[1])
                    offsetcenter2Left = (currPoint[0] - agent_radius, currPoint[1])
                    if (not clashesWithObstacle(offsetcenter1Top, offsetcenter2Top, worldObstacles) and
                        not clashesWithObstacle(offsetcenter1Bottom, offsetcenter2Bottom, worldObstacles) and
                        not clashesWithObstacle(offsetcenter1Right, offsetcenter2Right, worldObstacles) and
                        not clashesWithObstacle(offsetcenter1Left, offsetcenter2Left, worldObstacles)):
                        closest_point = currPoint
                        break
        
        if closest_point:
            lines.append((savedPoint, closest_point))
            visited.add(closest_point)
            previous_points.append(savedPoint)  # Save the previous point
            savedPoint = closest_point
        else:
            if previous_points:  # If there are previous points to backtrack to
                savedPoint = previous_points.pop()  # Backtrack
            else:
                break  # No more points to backtrack, exit
        
        exitCounter -= 1
    
    return lines

# Creates a path node network that connects the midpoints of each nav mesh together
def myCreatePathNetwork(world, agent = None):
	nodes = [] 
	# nodes check points of the blue line
	edges = []
	# blue lines that agent travels throught
	polys = []
	#  green polygons (triangles)

	### YOUR CODE GOES BELOW HERE ###

	# Any and all of these comments before "YOUR CODE GOES ABOVE HERE" can be deleted. They are meant to help, but may not.
	
	# you don't strictly speaking need to use these. But we include in case they help you get started.
	obstacleLines = world.getLines()[4:] # the first four (i.e. 0-3) are the screen edges; this gets all but those
	worldLines = list(set(world.getLines()))
	worldPoints = world.getPoints()
	worldObstacles = world.getObstacles()
	numPoints = len(worldPoints)
	lineDict = []
	polySet = set() 
 	# Probably good for holding ManualObstacle instances
 
	# HW TODO: Create triangles that don't intersect with each other or obstacles.
		# You may need to make sure no obstacles are completely inside the triangle.
		# You may need to register the triangle's lines for later use (when merging).

	# hint 0: to iterate over a collection, the `range` function is useful. E.g. `for i in range(numPoints):`
	#
	# hint 1: We can represent a triangle as a tuple of three worldPoints: triangle = (p1, p2, p3)
	#    Tuples in python are not limited to three elements
	#
	# hint 2: It may be useful to use the ManualObstacle class to help manage complexity. E.g. ManualObstacle(triangle)
	#    Because ManualObstacle is a Obstacle, you have helper methods like draw, getLines, getPoints, and pointInside
	
	reference_point = (600, 400)  # You can choose any reference point here
	orderPoints = sorted(world.getPoints(), key=lambda p: distance(reference_point, p))
	shapes = set()

	for x in orderPoints:
		closest_points = sorted(orderPoints, key=lambda p: distance(x, p))
		for y in worldPoints:
			for z in closest_points:
				if y != z:
					triangle = (x, y, z)
					if (triangleHitsObs(x,y,z,worldLines)):
						if is_clockwise(x, y, z):
							shapes.add(triangle)
							appendLineNoDuplicates((x, y), worldLines)
							appendLineNoDuplicates((x, z), worldLines)
							appendLineNoDuplicates((y, z), worldLines)
	
	# hint 3: for debugging, it can also be useful to 'draw' centroids of hulls, e.g. NavMeshUtils.drawCentroids(world, polySet)
	for tri in shapes:
			x = tri[0]
			y = tri[1]
			z = tri[2]
			if checkSubsetPoly(worldObstacles, tri):
				inside_points = filter(lambda i, a=x, b=y, c=z: a != i and i != b and i != c, worldPoints)
				if isInsideObstacle(tri, inside_points):
					# nodes.append(NavMeshUtils.getMidpointLine((x, y)))
					# nodes.append(NavMeshUtils.getMidpointLine((x, z)))
					# nodes.append(NavMeshUtils.getMidpointLine((y, z)))
					polySet.add(ManualObstacle(tri))

	# HW TODO: Now merge triangles in a way that preserves convexity.

	# HW Hint: Now might be a good time to NavMeshUtils.drawCentroids(world, polySet)

	mergeShapes = mergePolys(polySet)
	NavMeshUtils.drawCentroids(world,mergeShapes)
 
	for i in mergeShapes:
		polys.append(i.getPoints())
	
 
	# polys = list(polysMerge)
	# HW TODO: Create the final nav mesh and create cliques out of the boundaries of each polygon.
		# Decide how you will use the boundaries and centroid of the polygon as nodes.
		# For example, if the polygon has more than 3 sides, you may just send a line from each edge to the middle
		# Note: you can link borders directly in polygons or if the centroid is unusable.
			# NB: Don't try to link a border to itself!
	nodesSet = set()
	for polygon in mergeShapes: 
		for line in polygon.getLines():
			nodesSet.add(NavMeshUtils.getMidpointLine(line))
	
	for polygon in mergeShapes: 
		centroid1 = NavMeshUtils.getCentroid(polygon.getPoints())
		nodesSet.add(centroid1)
	nodes = list(nodesSet)
 
	allLinePoints = []
 
	agent_radius = agent.getMaxRadius()  # Get the agent's physical size
	disNodes = sorted(nodes, key=lambda p: distance((0,0), p))
	# print(disNodes)
	# for centroid1 in nodes:
	# 	inside_points = filter(lambda p: p != centroid1, nodes)
	# 	for centroid2 in nodes:
	# 		offsetcenter1Top = (centroid1[0], centroid1[1] + agent_radius)
	# 		offsetcenter2Top = (centroid2[0], centroid2[1] + agent_radius)
	# 		offsetcenter1Bottom = (centroid1[0], centroid1[1] - agent_radius)
	# 		offsetcenter2Bottom = (centroid2[0], centroid2[1] - agent_radius)
	# 		offsetcenter1Right = (centroid1[0] + agent_radius, centroid1[1])
	# 		offsetcenter2Right = (centroid2[0] + agent_radius, centroid2[1])
	# 		offsetcenter1Left = (centroid1[0] - agent_radius, centroid1[1])
	# 		offsetcenter2Left = (centroid2[0] - agent_radius, centroid2[1])
	# 		if (not hasObstacleBetween(offsetcenter1Top, offsetcenter2Top, world) and
	# 			not hasObstacleBetween(offsetcenter1Bottom, offsetcenter2Bottom, world) and
	# 			not hasObstacleBetween(offsetcenter1Right, offsetcenter2Right, world) and
	# 			not hasObstacleBetween(offsetcenter1Left, offsetcenter2Left, world)):
	# 			line = (centroid1, centroid2)
	# 			edges.append(line)
	edges1 = create_lines(disNodes,worldObstacles,agent_radius)
	# revList = sorted(nodes, key=lambda p: distance((900,900), p))
	# edges2 = create_lines(revList,worldObstacles,agent_radius)
	# midList = sorted(nodes, key=lambda p: distance(reference_point, p))

	# edges3 = create_lines(midList,worldObstacles,agent_radius)
	edges = list(edges1)




	# We should only return nodes that the agent can reach on the path network.
	# Suggestion: consider using a BFS of sorts to get a connected graph.

	### YOUR CODE GOES ABOVE HERE ###
	return nodes, edges, polys


