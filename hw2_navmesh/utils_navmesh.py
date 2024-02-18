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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

'''
The following will make it so that a polygon gets highlighted everytime the 'e' button is pressed.
Make these changes to GameWorld and RandomNavMeshNavigator:

In GameWorld, replace:

	def doKeyDown(self, key):
		pos = pygame.mouse.get_pos()
		if key == 32: #space
			self.agent.shoot()
		elif key == 100: #d
			print("distance traveled", self.agent.distanceTraveled)
		elif key == 101: #e
			point = (pos[0] + self.agent.rect.center[0] - self.camera[0], pos[1] + self.agent.rect.center[1] - self.camera[1])
			self.agent.navigator.doDebug(self, point)

In RandomNavMeshNavigator, add:

	def doDebug(self, world, point):
		NavMeshUtils.myDoDebug(self, world, point)
'''

### We include the below as additional utility methods that may aid you in solving the navmesh assignment
### Example use: NavMeshUtils.drawCentroids(world, pols)
	
class NavMeshUtils:

	@staticmethod
	def myDoDebug(nav, world, point):
		drawCross(world.debug, point, (0, 255, 0), 10, 2)
		for poly in nav.navmesh:
			if pointInsidePolygonPoints(point, poly):
				drawPolygon(poly, world.debug, (255, 0, 0), 3, False)
				#centroid = getCentroid(poly) 
				centroid = [sum(p)/len(poly) for p in zip(*poly)]
				drawCross(world.debug, centroid, (255, 0, 0), 5, 2)

	@staticmethod
	# Draws the locations of centroids for all passed-in obstacles.
	def drawCentroids(world, polys):
		for poly in polys:
			centroid = NavMeshUtils.getCentroid(poly.getPoints())
			drawCross(world.debug, centroid, (255, 0, 0))
	
	@staticmethod
	# Gets the centroid of a polygon defined by points.
	def getCentroid(poly):
		totalX = totalY = 0
		polygonLength = len(poly)
		for point in poly:
			totalX += point[0]
			totalY += point[1]
		centroid = (totalX / polygonLength, totalY / polygonLength)
		return centroid

	@staticmethod
	# Find the intersection between a line and the given lines, excluding lines that the points are on.
	def rayTraceOther(world, p1, p2, lines):
		# Check if the line goes into an obstacle (further than just touching the border).
		for obstacle in world.getObstacles():
			obstaclePoints = obstacle.getPoints()
			numPoints = len(obstaclePoints)
			match = -1
			for i in range(numPoints):
				# Check if the two points are on the polygon and non-adjacent.
				if obstaclePoints[i] == p1 or obstaclePoints[i] == p2:
					if match == -1:
						match = i
					else:
						difference = i - match
						if difference > 1 and difference < numPoints - 1:
							midpoint = NavMeshUtils.getMidpoint(p1, p2)
							if obstacle.pointInside(midpoint):
								return midpoint
							else:
								# Accounts for concave polygons.
								obstacleLines = obstacle.getLines()
								for line in obstacleLines:
									valid = True
									for linePoint in line:
										if linePoint == p1 or linePoint == p2:
											valid = False
											break
									if valid:
										intersect = rayTrace(p1, p2, line)
										if intersect != None:
											return intersect
		return rayTraceWorld(p1, p2, NavMeshUtils.filterLines([p1, p2], lines))

	@staticmethod
	# Returns the midpoint of a line.
	def getMidpointLine(line):
		return NavMeshUtils.getMidpoint(line[0], line[1])

	@staticmethod
	# Returns the midpoint between two points.
	def getMidpoint(p1, p2):
		return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

	@staticmethod
	# Return the points at .25 and .75 along the line between p1 and p2.
	def getQuarterPoints(p1, p2):
		return [(p1[0] + (p2[0] - p1[0]) *.25, p1[1] + (p2[1] - p1[1]) * .25), (p1[0] + (p2[0] - p1[0]) * .75, p1[1] + (p2[1] - p1[1]) * .75)]

	@staticmethod
	def getQuarterPointsLine(line):
		return NavMeshUtils.getQuarterPoints(line[0], line[1])

	@staticmethod
	# Returns a list of lines that do not intersect with the given points.
	def filterLines(points, lines):
		otherLines = []
		for line in lines:
			for point in points:
				valid = True
				for linePoint in line:
					if point == linePoint:
						valid = False
						break
				if valid:
					intersect = rayTrace(point, (-10, -10), line)
					if intersect != None:
						for i in range(2):
							if (between(point[i], intersect[i], intersect[i])):
								valid = False
								break
				if not valid:
					break
			if valid:
				otherLines.append(line)
		return otherLines

	@staticmethod
	# Checks if a polygon's points are in the same order as the given line.
	# Also returns the index where the line is contained in the polygon.
	def getPolygonOrder(line, polygon):
		polygonPoints = polygon.getPoints()
		polygonLength = len(polygonPoints)
		for i in range(polygonLength):
			if polygonPoints[i] == line[0]:
				if polygonPoints[i + 1] == line[1]:
					return i, True
				else:
					return polygonLength - 1, False
			elif polygonPoints[i] == line[1]:
				if polygonPoints[i + 1] == line[0]:
					return i, False
				else:
					return polygonLength - 1, True
		return -1, True

	@staticmethod
	# Converts old polygons to new polygons in the line dictionary.
	def convertLines(lineDict, polygon, polygonLines, newPolygon):
		for oldLine in polygonLines:
			if oldLine in lineDict:
				lineDict[oldLine] = [newPolygon if p == polygon else p for p in lineDict[oldLine]]
			else:
				reverse = (oldLine[1], oldLine[0])
				if reverse in lineDict:
					lineDict[reverse] = [newPolygon if p == polygon else p for p in lineDict[reverse]]
	
	@staticmethod
	# Gets the extremes of a polygon.
	def getBounds(polygon):
		minX = maxX = polygon[0][0]
		minY = maxY = polygon[0][1]
		polygonLength = len(polygon)
		for i in range(1, polygonLength):
			minX = min(minX, polygon[i][0])
			maxX = max(maxX, polygon[i][0])
			minY = min(minY, polygon[i][1])
			maxY = max(maxY, polygon[i][1])
		return minX, minY, maxX, maxY

	@staticmethod
	# Checks if the agent can fit in a path.
	def checkClearPath(line, world, agent):
		radius = agent.getMaxRadius()
		# Find the bounding box of the path to check for collisions with obstacles.
		node1 = numpy.matrix(line[0])
		node2 = numpy.matrix(line[1])
		between = node2 - node1
		backOffset = NavMeshUtils.normalize(between) * radius
		sideOffset = backOffset * numpy.matrix('0,1;-1,0')
		boundingBox = [NavMeshUtils.vecToList(node1 - backOffset + sideOffset),
						NavMeshUtils.vecToList(node1 - backOffset - sideOffset),
						NavMeshUtils.vecToList(node2 + backOffset - sideOffset),
						NavMeshUtils.vecToList(node2 + backOffset + sideOffset)]

		# Check to see if any obstacles intersect the path.
		valid = True
		for obstacle in world.obstacles:
			for line in obstacle.getLines():
				if rayTrace(boundingBox[0], boundingBox[3], line) != None or rayTrace(boundingBox[1], boundingBox[2], line) != None:
					valid = False
					break
			# Edge case of a small obstacle entirely within the sides of the path.
			if valid and pointInsidePolygonPoints(obstacle.getPoints()[0], boundingBox):
				valid = False
			if not valid:
				break
		return valid

	@staticmethod
	# Normalizes a vector.
	def normalize(vector):
		norm = numpy.linalg.norm(vector)
		if norm == 0:
			return vector
		else:
			return vector / norm

	@staticmethod
	# Converts a numpy matrix vector to a list.
	def vecToList(vector):
		return vector.tolist()[0]