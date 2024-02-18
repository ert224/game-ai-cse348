# Path Networks

## Path Network Navigation

One of the main uses of artificial intelligence in games is to perform **path planning**, the search for a sequence of movements through the virtual environment that gets an agent from one location to another without running into any obstacles.
For now we will assume static obstacles.
In order for an agent to engage in path planning, there must be a topography for the agent to traverse that is represented in a form that can be efficiently reasoned about.

The simplest topography is a grid.
Grid topologies discretize the environment and assumes an agent can be in one discrete cell or another.
However, for many games such as 1st-person shooters, a more continuous model of space is beneficial.
Depending on the granularity of the grid, a lot of space around obstacles becomes inaccessible in grid-based approaches.
Finally, grids result in unnecessarily large number of cell transitions.

A **path network** is a set of path nodes and edges that facilitates obstacle avoidance.
The path network discretizes a continuous space into a small number of points and edges that allow transitions between points.
However, unlike a grid topology, a path network does not require the agent to be at one of the path nodes at all times.
The agent can be at any point in the terrain.
When the agent needs to move to a different location and an obstacle is in the way, the agent can move to the nearest path node accessible by straight-line movement and then find a path through the edges of the path network to another path node near to the desired destination.

![Example path network](pathnet.png)

In this assignment, you will be provided with different terrains with obstacles and hard-coded path nodes.
You must write the code to generate the path network, as a set of edges between path nodes.
An edge between path nodes exists when (a) there is no obstacle between the two path nodes, and (b) there is sufficient space on either side of the edge so that an agent can follow the line without colliding with any obstacles.

We will test path network using a random-walk navigator that moves the agent to the nearest path node and then follows a randomly generated path---sequence of adjacent path nodes.

## What you need to know

The game engine is object-oriented.
The primary object is the **GameWorld**, which is a container for all other obstacles.
Most importantly, the GameWorld object contains the terrain of the virtual environment.
The terrain is represented as a list of **Obstacle** objects, which themselves are polygons&mdash;lists of points such that there is a line between every adjacent point, and the first and last points in the list.
The GameWorld also manages the agents, bullets, resources (things that agents can gather) and computes collisions between all objects and obstacles.
The GameWorld also does important stuff like run the real-time game loop and maintain the rendering windows, but you shouldn't need to worry about that.
What you do need to know is that every iteration of the game loop, called a *tick*, the update method is called on all dynamic objects.

Below are the important bits of information about objects that you will be working with or need to know about for this assignment.

### GameWorld

GameWorld is defined in core.py

Member functions:

* `getPoints()`: returns a list of all the corners of all obstacles (and the edges of the screen). A point is a tuple of the form (x, y).
* `getLines()`: returns a list of all the lines of all obstacles (and the screen boundaries). A line is a tuple of the form (point1, point2) where points are tuples of the form (x, y).
* `getLinesWithoutBorders()`: returns a list of all the lines of the obstacles, but does not include screen boundaries. 
* `getObstacles()`: returns a list of obstacles, which are of type Obstacle.
* `getDimensions()`: returns the (x, y)-dimensions of the world.

### Obstacle

Obstacle is defined in `core.py`.
An `Obstacle` is a polygon through which `Agents` cannot move.

Member functions:

* getPoints(): returns a list of all corners in the polygon. A point is a tuple of the form (x, y).
* getLines(): returns a list of all lines in the polygon. A line is a tuple of the form (point1, point2) where points are tuples of the form (x, y).
* pointInside(point): returns True if a point (x, y) is inside the obstacle.

### Agent

Agent is defined in `core.py`.
Agent is the class type of the player avatar or non-player characters.
Aside from drawing itself, an Agent knows how to move (which it inherits from its super-class Mover) and shoot.
If it is moving to a particular destination, it updates its location every tick.
Agents maintain a timer to control how often it can shoot.

While the Agent class does know how to move in a straight line toward a given point, it does not know how to move around an environment *without colliding with obstacles*.
When instructed to move, it will move in a straight line from its current position to a target position.
The intelligence in how to avoid obstacles is contained in a sub-component of the Agent, called the **Navigator**.

Member variables:

* moveTarget: the (x, y) point to which the agent has been instructed to move to. Used for interpolating the Agent's current position at any given tick.
* navigator: an object that tells the agent how to move.

Member functions:

* moveToTarget(point): Instructs the Agent to move straight to the point (x, y), ignoring the existence of obstacles. 
* navigateTo(point): Instructs the Agent to create a path through the environment that avoids collisions. This function invokes the navigator's computePath() functionality.
* isMoving(): returns True if the agent is currently moving.
* getMoveTarget(): returns the point that the agent is currently moving toward.
* stopMoving(): stops the Agent from moving

### Navigator

Navigator is defined in core.py.
A Navigator contains the smarts for how to get around in the game world without running into obstacles.
Think of it as a brain that gets attached to an agent that controls its movement.
Its primary function is to compute a path between two points that steers the Agent clear of any obstacles.
A path is a set of intermediate way-points that the agent should navigate to in pursuit of arriving safely at its ultimate destination.
Path planning can be done in many different ways and different AI techniques will sub-class from Navigator.
Once a path is computed, it sends call-back messages to the Agent to move from intermediate way-point to intermediate way-point.

Member variables:

* agent: pointer back to the Agent object that is being guided by the AI.
* world: pointer to the GameWorld object
* source: the point (x, y) from which navigation started.
* destination: the point (x, y) to which the Agent must traverse.
* path: a list of points to traverse in order that is guaranteed not to result in a collision with an obstacle.

Member functions:

* computePath(source, destination): Find a path through the terrain (causing path to be not None) and call back to the Agent to start moving. This default functionality just instructs the agent to move straight to the destination. This function will be overridden by sub-classes implementing particular path planning techniques.
* doneMoving(): the Navigator invokes this function when the agent has reached its moveTarget. doneMoving contains logic to determine what to do next. If there is a path, it will select the next point in the path as the next moveTarget and call back to the Agent.
* checkpoint(): called when the Agent reaches a point on the path.
* smooth(): optimizes the path to take shortcuts whenever possible and thereby create smoother, more efficient motion.

### PathNetworkNavigator

PathNetworkNavigator is defined in core.py. A PathNetworkNavigator is a specialization of a Navigator that works on path networks and contains the smarts for how to get around in the game world. Its primary function is to compute a path between two points that steers the Agent clear of any obstacles.

Member variables:

* pathnodes: a list of points of the form (x, y) that comprise a path network.
* pathnetwork: a list of lines of the form ((x1, y1), (x2, y2)) that comprise a path network.

Member functions:

* computePath(source, destination): Find a path through the path network (causing path to be not None) and call back to the Agent to start moving. This default functionality just instructs the agent to move to the destination.

### RandomNavigator

RandomNavigator is defined in randomnavigator.py. The RandomNavigator causes the Agent to perform a random walk of the path network. The random path terminates after 100 path nodes and the Agent moves directly to its destination from the last random point reached. Thus, the Agent can possibly collide with obstacles if random path does not reach the destination before the threshold is reached.

Member functions:

* computePath(source, destination): Find a path through the path network (causing path to be not None) and call back to the Agent to start moving. This default functionality just instructs the agent to move to the destination. The path is created by finding the closest path nodes to the source and then randomly selecting successor path nodes in the path network until the closest node to the destination is found. If the path length exceeds 100, then the Agent will be sent to its destination without further collision avoidance.

### Miscellaneous utility functions

Miscellaneous utility functions are found in utils.py.

* distance(point1, point2): returns the distance between two points. Points are tuples of the form (x, y).
* calculateIntersectPoint(point1, point2, point3, point4): returns a point (x, y) at the intersection of two lines, or None if the lines are parallel. One line is between point1 and point2 and the other line between point3 and point4.
* rayTrace(point1, point2, line): returns the intersection point (x, y) if a beam between point1 and point2 crosses the given line.
* rayTraceWorld(point1, point2, worldlines): performs a ray trace against every line in worldlines and returns the first intersection point found. worldlines is a list of lines of the form ((x1, y1), (x2, y2)).
* rayTraceNoEndpoints(point1, point2, line): same as rayTrace(), but doesn't check collisions with the end points of the two lines.
* rayTraceWorldNoEndpoints(point1, point2, worldlines): same as rayTraceWorld(), but doesn't check end points of any lines compared against each other.
* pointInsidePolygonPoints(point, listofpoints): returns True if point is within a polygon defined by listofpoints. Points are tuples of form (x, y).
* pointInsidePolygonLines(point, lines): returns True if point is within a polygon defined by lines. The point is of the form (x, y). Lines is a list of tuples of the form ((x1, y1), (x2, y2)).
* drawCross(surface, point, color, size, width): draw a cross on a PyGame drawing surface. Point is the center of the cross, a tuple of the form (x, y). Color is a tuple of the form (red, green, blue) with values between 0 and 255, each. size is the length of the lines in the cross. width is the width of the lines.
* minimumDistance(line, point): returns the shortest distance between a point (x, y) and a line ((x1, y1), (x2, y2)).
* findClosestUnobstructed(point, nodes, lines): returns the point in nodes that is closest to the given point for which none of the given lines comes between the found point and the given point. 

## Instructions

To complete this assignment, you must (1) implement code to generate a path network for a set of given path nodes in a given terrain. The path network should guarantee that an agent will not collide with an obstacle between any starting point and any destination point in the world. Because we haven't gotten to the part where the Agent can be controlled intelligently, we will use a  RandomNavigator, which walks randomly around for a while before proceeding directly to its destination.

To run the project code, use the following commands:

```
python runrandomnavigator0.py
python runrandomnavigator1.py
python runrandomnavigator2.py
python runrandomnavigator3.py
python runrandomnavigator4.py
```

### Step 1: Create the edges in the path network.

Modify mybuildpathnetwork.py and complete the myBuildPathNetwork() function. myBuildPathNetwork() takes in a list of pathnodes, a reference to the GameWorld object, and a reference to the agent doing the navigation. myBuildPathNetwork() must return a list of lines between any path nodes that should be considered adjacent. The list of lines must be computed such that each line originates and terminates at a path node (use shallow copies so the game engine can correlate the list of pathnodes and the list of edges) and an agent following the line will not collide with any obstacle.

## Grading

We will grade your solution based on the following criterion:
* **Reachability (10 points)**: the path network should be such that an agent can navigate from any path node to any other path node along any edge in the network without colliding with an obstacle. We will run a number of tests between randomly chosen path nodes and deduct points for each collision.

## Hints

Make sure any edge in the path network is traversable by an agent that has physical size. That is, edges in the path network should never come too close to any Obstacle such that an agent blindly following the path edge collides with an Obstacle.

Use agent.getMaxRadius() for the agent's physical size. This should be big enough to prevent most collisions but also be small enough to prevent disjoint graphs.

## Submission

To submit your solution, upload your modified mybuildpathnetwork.py **to gradescope**. All work should be done within this file.

You should not modify any other files in the game engine.

DO NOT upload the entire game engine.

DO NOT upload to CANVAS.