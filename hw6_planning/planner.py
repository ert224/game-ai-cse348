from constants import *
from utils import *
from core import *

import pdb
import copy
from functools import reduce

from statesactions import *

############################
## HELPERS

### Return true if the given state object is a goal. Goal is a State object too.
def is_goal(state, goal):
  return len(goal.propositions.difference(state.propositions)) == 0

### Return true if the given state is in a set of states.
def state_in_set(state, set_of_states):
  for s in set_of_states:
    if s.propositions != state.propositions:
      return False
  return True

### For debugging, print each state in a list of states
def print_states(states):
  for s in states:
    ca = None
    if s.causing_action is not None:
      ca = s.causing_action.name
    print(s.id, s.propositions, ca, s.get_g(), s.get_h(), s.get_f())


############################
### Planner 
###
### The planner knows how to generate a plan using a-star and heuristic search planning.
### It also knows how to execute plans in a continuous, time environment.

class Planner():

  def __init__(self):
    self.running = False              # is the planner running?
    self.world = None                 # pointer back to the world
    self.the_plan = []                # the plan (when generated)
    self.initial_state = None         # Initial state (State object)
    self.goal_state = None            # Goal state (State object)
    self.actions = []                 # list of actions (Action objects)

  ### Start running
  def start(self):
    self.running = True
    
  ### Stop running
  def stop(self):
    self.running = False

  ### Called every tick. Executes the plan if there is one
  def update(self, delta = 0):
    result = False # default return value
    if self.running and len(self.the_plan) > 0:
      # I have a plan, so execute the first action in the plan
      self.the_plan[0].agent = self
      result = self.the_plan[0].execute(delta)
      if result == False:
        # action failed
        print("AGENT FAILED")
        self.the_plan = []
      elif result == True:
        # action succeeded
        done_action = self.the_plan.pop(0)
        print("ACTION", done_action.name, "SUCCEEDED")
        done_action.reset()
    # If the result is None, the action is still executing
    return result

  ### Call back from Action class. Pass through to world
  def check_preconditions(self, preconds):
    if self.world is not None:
      return self.world.check_preconditions(preconds)
    return False

  ### Call back from Action class. Pass through to world
  def get_x_y_for_label(self, label):
    if self.world is not None:
      return self.world.get_x_y_for_label(label)
    return None

  ### Call back from Action class. Pass through to world
  def trigger(self, action):
    if self.world is not None:
      return self.world.trigger(action)
    return False

  ### Generate a plan. Init and goal are State objects. Actions is a list of Action objects
  ### Return the plan and the closed list
  def astar(self, init, goal, actions):
    plan = []    # the final plan
    open = []    # the open list (priority queue) holding State objects
    closed = []  # the closed list (already visited states). Holds state objects
    ### YOUR CODE GOES HERE

    def addSuccessor(state, action):
        new_state = State(state.propositions.union(action.add_list).difference(action.delete_list))
        new_state.parent = state
        new_state.causing_action = action
        new_state.g = state.g + action.cost
        new_state.h = self.compute_heuristic(new_state, goal, actions)
        return new_state

    def isClosed(state):
        return any(c.propositions == state.propositions for c in closed)

    def isOpen(state):
        return any(o.propositions == state.propositions and o.get_f() < state.get_f() for o in open)

    if (is_goal(init, goal)):
        return plan, closed
    open.append(init)
    
    endState = None
    
    while open and not endState:
        currentState = min(open, key=lambda n: n.get_f())
        open.remove(currentState)

        successors = []
        for action in actions:
            if all(prop in currentState.propositions for prop in action.preconditions):
                new_state = addSuccessor(currentState, action)
                successors.append(new_state)

        for node in successors:
            if not endState and not isClosed(node):
                if is_goal(node, goal):
                    endState = node
                elif not isOpen(node):
                    open.append(node)

        closed.append(currentState)

    while endState and endState.causing_action:
        plan.insert(0, endState.causing_action)
        endState = endState.parent

    ### CODE ABOVE
    return plan, closed
  
  ### Compute the heuristic value of the current state using the HSP technique.
  ### Current_state and goal_state are State objects.
  def compute_heuristic(self, current_state, goal_state, actions):
      actions = actions = copy.deepcopy(actions)  # Make a deep copy just in case
      h = 0
      # Create start and end actions
      start_action = Action('start', [], current_state.propositions, [])
      end_action = Action('end', goal_state.propositions, [], [])

      actions.append(start_action)
      actions.append(end_action)

      # Build graph and initialize distances
      graph, distances = self.buildGraph(actions)

      visited = set()
      queue = [start_action]

      while queue:
          node = queue.pop(0)
          visited.add(node)
          self.setDistance(node, graph, distances)
          self.addActions(node, graph, visited, queue, distances)


      h = distances[end_action] - 2

      return h

  def buildGraph(self, actions):
      graph = {}
      distances = {}

      for action in actions:
          incoming = []
          for other_action in actions:
              for prop in action.preconditions:
                  if prop in other_action.add_list:
                      incoming.append((prop, other_action))
          graph[action] = incoming
          distances[action] = 1

      return graph, distances

  def setDistance(self, node, graph, distances):
      if graph[node]:
          dist = max(distances[edge[1]] for edge in graph[node])
          if dist > distances[node]:
              distances[node] = dist

  def addActions(self, node, graph, visited, queue, distances):
      for action in graph:
          for edge in graph[action]:
              new_dist = distances[node] + action.cost
              if edge[1] == node and new_dist > distances[action]:
                  distances[action] = new_dist
          if action not in visited and all(any(prop in act.add_list for act in visited) for prop in action.preconditions):
              queue.append(action)