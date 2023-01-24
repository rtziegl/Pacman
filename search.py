# Authors:
# Youssef Ben Bella.
# Ryley Ziegler.

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
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


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

    def backtrack(v, pt):
        # Pop off top of pt which holds our tuples.
        # It's our next state after backtrack is complete.
        after_back_state = pt.pop()
        i = len(pt) - 1
        special_state = True

        # Looping from leaf nodes to each parent looking for unvisited children.
        while special_state:

            s = problem.getSuccessors(pt[i][0])
            # Pop each state until the parent state with an unvisited child is reached.
            # Save state to add it back after the loop breaks.
            unvisited_children_state = pt.pop()

            # Check for parents with unvisited children.
            for mat, dre, cost in s:
                if mat not in v:
                    # Append the state with the unvisited children.
                    pt.append(unvisited_children_state)
                    # Append the state that we took off in beginning (next state after backtrack).
                    pt.append(after_back_state)
                    # Break the loop
                    special_state = False
                    break
            i -= 1

    def move(s, m, v, p, fd, pt):

        # Made in_v for keeping tack of what's been visited per iteration of move.
        in_v = []

        # If the successor isn't in v push to the stack (m) and append the matrix and directions to an array (p).
        # Otherwise, append to in_v. to see what has been visited.
        for mat, dre, cost in s:
            if mat not in v:
                m.push(mat)
                p.append((mat, dre))
            else:
                in_v.append(mat)

        # Pop the state at the top of the stack, store in popped_state.
        popped_state = m.pop()

        # This ensures only the visited states are appended to list pt.
        # Otherwise, all directions for all successors are included.
        for states in p:
            if popped_state in states:
                pt.append(states)

        # If the amount of states in v for this iteration are the same amount as the s (meaning all successors visited),
        # then this means we need to backtrack bc all states down this path have been visited.
        if len(in_v) == len(s):
            # After this completes, the pt (tuples with directions list) is fully updated with correct directions..
            backtrack(v, pt)

        # If current popped_state is not the goal generate new successors (s).
        # Append to v, which holds all matrix of visited states.
        # Recursively call move with new successors.
        # Otherwise, goal state is found, and we append the directions (tuples[1]) to the list returned fd.
        if not problem.isGoalState(popped_state):
            s = problem.getSuccessors(popped_state)
            v.append(popped_state)
            move(s, m, v, p, fd, pt)
        else:
            for tuples in pt:
                fd.append(tuples[1])

        # Return without first state (dummy start state).
        return fd[1:]

    mat_l = util.Stack()
    successors = problem.getSuccessors(problem.getStartState())
    visited = [problem.getStartState()]
    path = []
    final_directions = []
    popped_tuples = []

    # Add start state in case of backtrack to root.
    false = (problem.getStartState(), 'na')
    # Append start state to pt bc it needs it in case of backtrack to root.
    popped_tuples.append(false)

    directions = move(successors, mat_l, visited, path, final_directions, popped_tuples)

    print 'Final Directions: ', directions
    return directions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    def find_solution(pt):
        reversed_directions = []
        # Chop off dummy start state.
        pt = pt[1:]
        # Index equal to the length of pt (popped_tuples).
        i = len(pt) - 1
        special_state = True
        initial_state = pt[i][0]
        reversed_directions.append(pt[i])

        # Looping from leaf nodes to each parent with a md = 1 ensuring a correct path to start.
        while special_state:
            if i != 0 and util.manhattanDistance(initial_state, pt[i][0]) == 1:
                reversed_directions.append(pt[i])
                initial_state = (pt[i][0])
                i -= 1
            elif i == 0 and util.manhattanDistance(initial_state, pt[i][0]) == 1:
                reversed_directions.append(pt[i])
                break
            elif i == 0 and util.manhattanDistance(initial_state, pt[i][0]) != 1:
                break
            elif i != 0 and util.manhattanDistance(initial_state, pt[i][0]) != 1:
                i -= 1

        # Reversing the reverse directions.
        reversed_directions.reverse()

        return reversed_directions

    def move(s, m, v, p, fd, pt):
        # Made in_v for keeping tack of what's been visited per iteration of move.
        in_v = []

        # If the successor isn't in v push to the stack (m) and append the matrix and directions to an array (p).
        # Otherwise, append to in_v. to see what has been visited.
        for mat, dre, cost in s:
            if mat not in v:
                m.push(mat)
                p.append((mat, dre))
            else:
                in_v.append(mat)

        # Pop the state at the top of the stack, store in popped_state.
        popped_state = m.pop()

        # This ensures only the visited states are appended to list pt.
        # Otherwise, all directions for all successors are included.
        for states in p:
            if popped_state in states:
                pt.append(states)

        # If current popped_state is not the goal generate new successors (s).
        # Append to v, which holds all matrix of visited states.
        # Recursively call move with new successors.
        # Otherwise, goal state is found, and we append the directions (tuples[1]) to the list returned fd.
        if not problem.isGoalState(popped_state):
            s = problem.getSuccessors(popped_state)
            v.append(popped_state)
            move(s, m, v, p, fd, pt)
        else:
            pt = find_solution(pt)
            for tuples in pt:
                fd.append(tuples[1])

        return fd

    mat_l = util.Queue()
    successors = problem.getSuccessors(problem.getStartState())
    visited = [problem.getStartState()]
    path = []
    final_directions = []
    popped_tuples = []

    # Add start state in case of backtrack to root.
    false = (problem.getStartState(), 'na')
    # Append start state to pt bc it needs it in case of backtrack to root.
    popped_tuples.append(false)

    directions = move(successors, mat_l, visited, path, final_directions, popped_tuples)

    print 'Final Directions: ', directions
    return directions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    def find_solution(pt):
        reversed_directions = []
        # Chop off dummy start state.
        pt = pt[1:]
        # Index equal to the length of pt (popped_tuples).
        i = len(pt) - 1
        special_state = True
        initial_state = pt[i][0]
        reversed_directions.append(pt[i])

        # Looping from leaf nodes to each parent with a md = 1 ensuring a correct path to start.
        while special_state:
            if i != 0 and util.manhattanDistance(initial_state, pt[i][0]) == 1:
                reversed_directions.append(pt[i])
                initial_state = (pt[i][0])
                i -= 1
            elif i == 0 and util.manhattanDistance(initial_state, pt[i][0]) == 1:
                reversed_directions.append(pt[i])
                break
            elif i == 0 and util.manhattanDistance(initial_state, pt[i][0]) != 1:
                break
            elif i != 0 and util.manhattanDistance(initial_state, pt[i][0]) != 1:
                i -= 1

        # Reversing the reverse directions.
        reversed_directions.reverse()

        return reversed_directions

    def move(s, m, v, p, fd, pt):
        # Made in_v for keeping tack of what's been visited per iteration of move.
        in_v = []

        # If the successor isn't in v push to the stack (m) and append the matrix and directions to an array (p).
        # Otherwise, append to in_v. to see what has been visited.
        for mat, dre, cost in s:
            if mat not in v:
                # Determining priority for UCS.
                m.push(mat, cost)
                p.append((mat, dre))
            else:
                in_v.append(mat)

        # Pop the state at the top of the stack, store in popped_state.
        popped_state = m.pop()

        # This ensures only the visited states are appended to list pt.
        # Otherwise, all directions for all successors are included.
        for states in p:
            if popped_state in states:
                pt.append(states)

        # If current popped_state is not the goal generate new successors (s).
        # Append to v, which holds all matrix of visited states.
        # Recursively call move with new successors.
        # Otherwise, goal state is found, and we append the directions (tuples[1]) to the list returned fd.
        if not problem.isGoalState(popped_state):
            s = problem.getSuccessors(popped_state)
            v.append(popped_state)
            move(s, m, v, p, fd, pt)
        else:
            pt = find_solution(pt)
            for tuples in pt:
                fd.append(tuples[1])

        return fd

    mat_l = util.PriorityQueue()
    successors = problem.getSuccessors(problem.getStartState())
    visited = [problem.getStartState()]
    path = []
    final_directions = []
    popped_tuples = []

    # Add start state in case of backtrack to root.
    false = (problem.getStartState(), 'na')
    # Append start state to pt bc it needs it in case of backtrack to root.
    popped_tuples.append(false)

    directions = move(successors, mat_l, visited, path, final_directions, popped_tuples)

    print 'Final Directions: ', directions
    return directions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    def find_solution(pt):
        reversed_directions = []
        # Chop off dummy start state.
        pt = pt[1:]
        # Index equal to the length of pt (popped_tuples).
        i = len(pt) - 1
        special_state = True
        initial_state = pt[i][0]
        reversed_directions.append(pt[i])

        # Looping from leaf nodes to each parent with a md = 1 ensuring a correct path to start.
        while special_state:
            if i != 0 and util.manhattanDistance(initial_state, pt[i][0]) == 1:
                reversed_directions.append(pt[i])
                initial_state = (pt[i][0])
                i -= 1
            elif i == 0 and util.manhattanDistance(initial_state, pt[i][0]) == 1:
                reversed_directions.append(pt[i])
                break
            elif i == 0 and util.manhattanDistance(initial_state, pt[i][0]) != 1:
                break
            elif i != 0 and util.manhattanDistance(initial_state, pt[i][0]) != 1:
                i -= 1

        # Reversing the reverse directions.
        reversed_directions.reverse()

        return reversed_directions

    def move(s, m, v, p, fd, pt):
        # Made in_v for keeping tack of what's been visited per iteration of move.
        in_v = []

        # If the successor isn't in v push to the stack (m) and append the matrix and directions to an array (p).
        # Otherwise, append to in_v. to see what has been visited.
        for mat, dre, cost in s:
            if mat not in v:
                # Determining priority for A*.
                cost = cost + heuristic(mat, problem)
                m.push(mat, cost)
                p.append((mat, dre))
            else:
                in_v.append(mat)

        # Pop the state at the top of the stack, store in popped_state.
        popped_state = m.pop()

        # This ensures only the visited states are appended to list pt.
        # Otherwise, all directions for all successors are included.
        for states in p:
            if popped_state in states:
                pt.append(states)

        # If current popped_state is not the goal generate new successors (s).
        # Append to v, which holds all matrix of visited states.
        # Recursively call move with new successors.
        # Otherwise, goal state is found, and we append the directions (tuples[1]) to the list returned fd.
        if not problem.isGoalState(popped_state):
            s = problem.getSuccessors(popped_state)
            v.append(popped_state)
            move(s, m, v, p, fd, pt)
        else:
            pt = find_solution(pt)
            for tuples in pt:
                fd.append(tuples[1])

        return fd

    mat_l = util.PriorityQueue()
    successors = problem.getSuccessors(problem.getStartState())
    visited = [problem.getStartState()]
    path = []
    final_directions = []
    popped_tuples = []

    # Add start state in case of backtrack to root.
    false = (problem.getStartState(), 'na')
    # Append start state to pt bc it needs it in case of backtrack to root.
    popped_tuples.append(false)

    directions = move(successors, mat_l, visited, path, final_directions, popped_tuples)

    print 'Final Directions: ', directions
    return directions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
