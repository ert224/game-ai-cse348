# Behavior Planner Assignment

## Background 

In this assignment you will write an action planner using Heuristic Search Planning.
Behavior Planners chain sequences of actions/behaviors together to solve a problem that requires looking multiple steps into the future.
It is particularly good for solving puzzles.

Specifically, you will be implementing the heuristic search planning (HSP) algorithm.
HSP is, at its base, identical to A*.
However, actions/behaviors are much more complex than in pathfinding and there is no obvious heuristic such as Euclidean distance, such as in pathfinding. 

In behavior planning, actions can be represented in STRIPS form.
That is, each action has a name, preconditions, and effects.
Preconditions are things that must be true in the world for an action to execute.
Effects are the ways in which the world is changed if an action is executed.
Preconditions and effects are given as logical propositions, e.g., "has_key" might be a symbol that represents the fact that an agent has a key.

```
Action: Pickup_gold_in_chest
Preconditions: at_chest, gold_in_chest, has_key
Add_list: has_gold
Delete_list: gold_in_chest 
```

In the example above, the agent has the option of picking up some gold in a locked chest.
* This action can only be performed if the agent is at the chest (`at_chest`), the gold is in the chest (`gold_in_chest`), and the agent has the key (`has_key`).
* The effects are split into two parts.
    * The `add_list` are new facts that will be true about the world.
        * In particular, the agent will have the gold (`has_gold`).
    * The `delete_list` are those facts that will no longer be true (`gold_in_chest`).

The objective of a planner is to determine which actions must be executed and in what order.  

However, how do we know if any action gets the agent closer to a goal.
For example, the goal might be `has_gold`, in which case the action achieves the goal.
But the goal might also be `has_sword` and having gold might be one step toward the goal of acquiring the sword (perhaps it can be bought at a store with gold).
Does `has_gold` get us closer to the goal?
It is not clear just by looking at the propositions whether the agent is one step away or ten steps away.
Without being able to estimate how many more actions are needed to get to the goal, the best we can do is an exhaustive search such as breadth first search.

Heuristic Search Planning adds a new element to A*: it allows us to analyze the actions to make an informed guess about how many actions it takes to get to a goal.
HSP "relaxes" the planning problem in two ways.
1. First, it pretends that the delete_lists don't exist.
    * `Delete_lists` make things false and when things go from true to false then things get complicated.
    * If things can only go from false to true, then propositions add up and it is only a matter of time before the agent has "collected" all the propositions to achieve a goal state.
2. Second, HSP allows actions to happen simultaneously instead of in sequence, so we don't have to worry too much about whether one thing should happen before another thing.

It turns out that with these two relaxation problems, planning is polynomial in time complexity instead of NP-hard.
We can solve the relaxed problem in polynomial time and then use the number of steps in the simpler problem as a guess to how many steps, at a minimum, will be needed for the full planning problem.
It will never take fewer steps than the solution to the simpler problem. 

HSP calculates the heuristic value for a given state in two stages.
First it constructs a graph.
The actions are nodes in the graph.
There are two additional nodes: (1) a dummy action representing an empty goal transition in which the preconditions are the goal conditions and there is no add_list or delete_list, and (2) a dummy action representing an empty current state transition in which the add_list is the propositions true in the current state and with no preconditions or delete_list.
Think of (1) as a special action for "cleaning up" and (2) as a special action for getting set up. 

To construct the graph, create an edge between action-nodes for each pair of actions where one of the add_list propositions in action 1 matches a proposition in the preconditions of action 2.
Label the edge with the name of the proposition.
Note that two actions might have multiple edges between them and that multiple edges terminating at the same action might have the same proposition label.

The second step is to "walk" the graph and find the longest path between the dummy start action and the dummy end action.
* Create a queue.
* Add the dummy start to the queue and mark it as visited.
* Add any actions to the queue if all of their predecessors have been visited.
* If an action has multiple incoming edges with the same proposition, then only one of them must have been visited.
    * This represents a step in the relaxed planning problem where all the preconditions have been met by a preceding action.
* Continue to pop and visit action-nodes in the queue.
* For each action-node visited, compute it's distance from the start as the `dist = max(E_1, E_2, ...)` for every incoming edge.
    * `E_i` is a number we assign to each edge in the graph.
    * For each outgoing edge we assign `E_j = dist + 1 (or dist + cost if the action has a cost)`. 

When the queue is empty the heuristic value of getting from the current state (represented by the dummy start) to the goal state (represented by the dummy end) is the biggest edge cost observed. 

Now you can take any state that A* discovers and estimate the number of additional actions needed to get to the goal.
Computing the heuristic is costly since it is a polynomial: it is `O(n^2)` where `n` is the number of possible actions.
However, on average one should need to explore fewer states than an exhaustive breadth first search when using the generated HSP heuristic. 

Now implement A* as normal.
The only difference between A* used for behavior planning and pathfinding is (1) the heuristic as described above, and (2) you need to use action `add_lists` and `delete_lists` to figure out the successor states.

To generate a successor state, take an action.
* Check if the action is executable in the current state by checking to see if all of its preconditions are in the set of current state propositions.
    * If so, then take the current state propositions, add all propositions in the action's `add_list`, and remove all propositions in the action's `delete_list`.
    * This new set of propositions will be the new state that can be reached from the old state.

--------------------------------------------------------

## Instructions

**STEP 0**: Copy your solution to the pathnetwork homework (`mybuildpathnetwork.py`).

**STEP 1**: Implement A* for behavior planning.
In `planner.py`, find the Planner class and complete the `astar()` function.
The `astar()` function takes an initial state, a goal state, and a set of actions and produces a plan.
A plan is an ordered list of actions.
It must also return a list of visited states (in any order).
In the codebase, there are classes for `State` and `Action` that you can use.

**Hint**: initially A* will act as if it is breadth first search because the heuristic returns `h=0` for all states by default.
This will allow you to verify you have implemented your search loop correctly because it is the same for breadth first search and A*.
Then you can turn on action costs.
Then, after step 2 you can test with the HSP heuristic.

**STEP 2**: Implement the HSP heuristic function in the `compute_heuristic()` function in Planner.
The `compute_heuristic()` function takes an arbitrary state and a goal state and returns an integer.

**TESTING**: Use `rundoor.py` and `runbank.py` to test the planner.
Test the planner with an agent in `rundoormap.py` and `runbankmap.py`

-------------------------------------------------------------

## THINGS YOU NEED TO KNOW:

### `Action` class:

A container class for everything the planner needs to know about actions.
It also contains logic for executing in the game engine.

Member variables:
* `name`: string name for the action
* `preconditions`: a set (not a list) of propositions. Each proposition is a string that represents a single fact about the world that would need to be true for this action to work.
* `add_list`: a set (not a list) of propositions that become true if this action executes.
* `delete_list`: a set (not a list) of propostions that were once true but become false when the action is executed.
* `cost`: integer, how expensive the action is
* `agent`: pointer to the agent that would execute the action.
* `first`: records whether the execution loop (see below) has been executed more than once.

Member functions:
* `Reset`: reset the action and get it ready for a new execution
* `Execute`: Execute this action in the game engine. If the action requires more than one tick, this function returns None. It returns True if the action completes successfully. It returns False if the action fails to complete.
* `Enter`: Runs the first time the execution function is called.

### `MoveAction` class:

A subclass of Action that knows how to make the Agent move in the game engine.

### `DoorAction` class:

A subclass of Action that handles opening doors in the game engine.

### `TriggerAction` class:

A subclass of Action that performs discrete triggering actions in the game engine (really anything that is not Move or opening doors).

### `State` class:

A container for tracking everything the planner needs to know about a state during planning.

Member variables:
* `propositions`: a set (not a list) of propositions, where each proposition is a string representing some fact about the world.
* `g`: integer, the cost from the initial state to the state represented by this object.
* `h`: integer, the estimated cost from this state to the goal state.
* `parent`: the state that this is a successor to.
* `causing_action`: the action (Action class object) that would be used to transition from the parent state to this state.
* `id`: string, a unique identifier

Member functions:
* `get_g`: get the g-value
* `get_h`: get the h-value
* `get_f`: compute f = g + h

### `Planner` class:

The class that does the planning.
Implements `astar()` and `compute_heuristic()`.
It is also meant to be used as a super-class for an agent object in the game engine.

Member variables:
You only need to know about the following:
* `initial_state`: the initial state (State object)
* `goal_state`: the goal state (State object)
* `actions`: a list of actions (Action objects)
* `the_plan`: a list of actions (Action objects) that will be executed.

Member functions:
You only need to know about the following:
* `astar`: to be completed. Takes an initial state (State object), goal state (State Object) and list of actions (Action objects). Returns two values: a plan as a list of Action objects, and the list of visited states called the closed list.
* `compute_heuristic`: to be completed. Takes a current state (State Object), goal state (State object), and list of actions (Action objects). Returns the heuristic value of transitioning from the current state to the goal state.
* `update`: called by the game engine every tick. When there is a plan (the_plan is not empty) then it executes each action in turn. 

Additional functions:
* `is_goal`: takes a state and a goal and checks if the state is a goal state.
* `state_in_set`: return true if the given state is in a set of states
* `print_states`: for debugging, print each state in a list of states

### `NPCAgent` class

A type of `Agent` for this assignment.
Doesn't do anything in particular of interest, except is sub-classes from Planner.
The `NPCAgent` knows how to generate a plan at startup if it has an initial state and a goal. 

### `Place` class:

A rectangular area in a game map of significance to the planning problem.
The agent may need to go to one of these places.
Also some actions can only be performed in some places.

### `DoorPlace` class:

A type of `Place` where doors can be opened.

### `NPCWorld` class:

A special type of `GameWorld` that maintains a ground-truth world state as a set (not a list) of propositions (strings where each represents a fact about the world) and knows how to check the preconditions of actions that are being executed.

----------------------------------------------
