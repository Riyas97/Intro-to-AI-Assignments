# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import time
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack() 
    start_state = problem.getStartState()
    frontier.push(start_state)
    explored = set()
    parentMap = {}
    succCache = {}
    parentMap[start_state] = start_state
    goal_state = (-1,-1)

    while (frontier.isEmpty() == False):
        parent_state = frontier.pop()

        if problem.isGoalState(parent_state):
            goal_state = parent_state
            break
        explored.add(parent_state)

        successors = getCached(problem.getSuccessors, parent_state, succCache)
        # print successors
        for i in successors:
            if i[0] not in explored:
                frontier.push(i[0])
                parentMap[i[0]] = parent_state

    path = []
    cur = goal_state
    while cur != start_state:
        path.append(cur)
        cur = parentMap[cur]
    path.append(start_state)
    path.reverse()
    
    directions = []
    for i in range(len(path) - 1):
        cur = path[i]
        next = path[i+1]

        successors = getCached(problem.getSuccessors, cur, succCache)
        
        for j in successors:
            if j[0] == next:
                directions.append(j[1])
                break
 
    return directions
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue() 
    start_state = problem.getStartState()
    frontier.push(start_state)
    explored = set()
    explored.add(start_state)
    parent = {}
    succCache = {}
    parent[start_state] = start_state
    goal_state = (-1,-1)

    while (not frontier.isEmpty()):
        u = frontier.pop()
        if problem.isGoalState(u):
                goal_state = u
                break
        
        successors = getCached(problem.getSuccessors, u, succCache)
        
        for (v,a,w) in successors:
            if v not in explored:
                frontier.push(v)
                explored.add(v)    
                parent[v] = u
        else:
            continue
        break
    
    # obtain path
    path = []
    cur = goal_state
    while cur != start_state:
        path.append(cur)
        cur = parent[cur]
    path.append(start_state)
    path.reverse()
    
    # obtain directions
    directions = []
    for i in range(len(path) - 1):
        cur = path[i]
        next = path[i+1]

        successors = getCached(problem.getSuccessors, cur, succCache)
        
        for j in successors:
            if j[0] == next:
                directions.append(j[1])
                break
    
    return directions
  
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() 
    start_state = problem.getStartState()
    frontier.push(start_state, 0)
    explored = set()
    parent = {}
    g = {}
    g[start_state] = 0
    succCache = {}
    parent[start_state] = start_state
    goal_state = (-1,-1)

    while (not frontier.isEmpty()):
        u = frontier.pop()
        if problem.isGoalState(u):
            goal_state = u
            break

        explored.add(u)
        successors = getCached(problem.getSuccessors, u, succCache)

        for (v,a,w) in successors:
            if v not in explored:
                if (not v in g) or (g[v] > g[u] + w):
                    g[v] = g[u] + w
                    parent[v] = u
            
                frontier.update(v, g[v])
                
    # obtain path
    path = []
    cur = goal_state
    while cur != start_state:
        path.append(cur)
        cur = parent[cur]
    path.append(start_state)
    path.reverse()
    
    # obtain directions
    directions = []
    for i in range(len(path) - 1):
        cur = path[i]
        next = path[i+1]

        successors = getCached(problem.getSuccessors, cur, succCache)
        
        for j in successors:
            if j[0] == next:
                directions.append(j[1])
                break
    
    return directions
        
    # util.raiseNotDefined() # REMOVE THIS ONCE YOU IMPLEMENTED YOUR CODE

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0 

def classicManhattanHeuristic(state, problem):
    goal = problem.goal
    return manhattanDistance(state, goal)

def manhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    pq = util.PriorityQueue() 
    s = problem.getStartState()
    pq.push(s, heuristic(s,problem))

    vis = set()
    parent = {}
    g = {}
    g[s] = 0


    succCache = {}
    parent[s] = s
    goal_state = (-1,-1)

    while (not pq.isEmpty()):
        u = pq.pop()
        if problem.isGoalState(u):
            goal_state = u
            break

        vis.add(u)
        successors = getCached(problem.getSuccessors, u, succCache)

        for (v,a,w) in successors:
            if v not in vis:
                if (not v in g) or (g[v] > g[u] + w):
                    g[v] = g[u] + w
                    parent[v] = u
            
                f = g[v] + heuristic(v, problem)
                pq.update(v, f)
                

    path = []
    cur = goal_state
    while cur != s:
        path.append(cur)
        cur = parent[cur]
    path.append(s)
    path.reverse()
    
    directions = []
    for i in range(len(path) - 1):
        cur = path[i]
        next = path[i+1]

        successors = getCached(problem.getSuccessors, cur, succCache)
        
        for j in successors:
            if j[0] == next:
                directions.append(j[1])
                break
    
    return directions
        


def getCached(function, param, cache):
    if param in cache:
        return cache[param]   
    cache[param] = function(param)
    return cache[param]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
