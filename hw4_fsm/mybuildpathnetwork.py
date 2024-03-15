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
