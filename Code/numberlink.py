'''NAMES OF THE AUTHOR(S): TODO'''
import time
import sys
from os import listdir,system
from search import *

#################  
# Problem class #
#################

class NumberLink(Problem):
	def __init__(self, init):
		"""  TODO: Initialize the given problem. For that you should use the state class given below. Also initialize a class instance
			"paths" that is a dictionnary where the key is the path indicator (a character) and the value a table of two dimensions
			that stocks the 2 endpoints of a path in a table like this [[x1,y1][x2,y2]]. Also initialize the first path to construct using the nextPath method."""
		self.paths = {}
		self.paths['A'] = [[0,0],[0,3]]
		self.paths['B'] = [[1,0],[1,3]]
		self.paths['C'] = [[2,0],[2,3]]
		self.paths['D'] = [[3,0],[3,3]]
		grid = [['A', '.','.', 'A'],['B','.','.','B'],['C', '.','.','C'], ['D', '.','.','D']]
		state = State(grid, 'A', [0,0],{})
		self.initial = state

	def goal_test(self, state):
		"""Return true if the given state is the goal.
			For that we check if all paths is completed."""
		for key in self.paths.keys():
			if key not in state.pathsCompleted:
				return False
		print(state.grid)
		return True
    
	def successor(self, state):
		"""Return all the successors of a current state.
			A successor is a new state in which we applied one of the following action : 
			"left", "right", "down" or "up". """
		if state.connected():
			state = self.nextPath(state)
		if state is not None:
			actions = state.possibleActions()
			print(actions)
			print(state.grid)
			for i in range(0, len(actions)):
				yield (actions[i], State(self.copyList(state.grid), state.currentPath, state.lastExtension.copy(), state.pathsCompleted.copy()).action(actions[i]))
				
				
	def copyList(self, orig):
		h = len(orig)
		l = len(orig[0])
		copy = []
		line = []
		for i in range(0, h):		
			line = []
			for j in range(0, l):
				line.append(orig[i][j])
			copy.append(line)
		return copy
	
	def nextPath(self, state):
		"""Return the new state containing the new path to construct."""
		newState = State(self.copyList(state.grid), state.currentPath, state.lastExtension.copy(), state.pathsCompleted.copy())
		n = 9;						"Number of possible actions for a path"
		for key in self.paths.keys():
			if key not in state.pathsCompleted:
				endpoint1 = self.paths[key][0]; "first endpoint"
				endpoint2 = self.paths[key][1]; "second endpoint"
				if pathExists(state.grid, endpoint1, endpoint2) != True:
					print("No path")
					pass
				n1 = self.numberOfPossibleActions(state.grid, endpoint1)
				n2 = self.numberOfPossibleActions(state.grid, endpoint2)
				temp = n1 + n2
				if temp < n:
					pathToConstruct = key
					pointToExtend = (endpoint1 if n1 < n2 else endpoint2)
					newState.currentPath = key
					newState.lastExtension = pointToExtend
		return newState
				
		
	def numberOfPossibleActions(self, grid, position):
		"""Return the number of possible action for the given element in the grid.
			grid is a table of 2 dimensions and position the coordinates of the element to consider."""
		num = 0
		i = position[0]
		j = position[1]
		if  i != 0 and grid[i-1][j] == '.':
			num = num+1
		if  i != len(grid)-1 and grid[i+1][j] == '.':
			num = num+1
		if  j != 0 and grid[i][j-1] == '.':
			num = num+1
		if  j != len(grid[0])-1 and grid[i][j+1] == '.':
			num = num+1
		return num
		
			
###############
# State class #
###############

class State:
	"""State representation of a numberlink problem.
		The grid is represented by a matrix (double dimension table) with the top left corner represented by grid[0][0].
		The currentPath indicates the current path in construction (a character).
		The lastExtension variable stores the coordinates (x,y) of the last element extented (a table with two value for x and y).
		The pathsCompleted indicates the paths already completed ( a dictionnary)."""
	def __init__(self, grid, currentPath, lastExtension, pathsCompleted):
		self.grid = grid
		self.currentPath = currentPath	
		self.lastExtension = lastExtension
		self.pathsCompleted = pathsCompleted
			
	def action(self,action):
		"""Apply the action on the grid based on the currentPath and the lastExtension coordinates.
			The action should be a string with the value of ["right", "down", "left", "up"] that indicates in which direction the lastExtension
			should be extented"""
		i = self.lastExtension[0]
		j= self.lastExtension[1]
		if action == "left":
			j = j-1
		elif action == "right":
			j = j+1
		elif action == "down":
			i = i+1
		elif action == "up":
			i = i-1
		self.grid[i][j] = self.currentPath
		self.lastExtension[0] = i
		self.lastExtension[1] = j
		if self.connected() == True:
			pass
		return self
		
	def connected(self):
		"""Check if the currentPath is finished. 
		For that we check if the last element extented has 2 neighboors from the same path (with the same character).
		If the path is finished, add the path in the pathsCompleted."""
		neighboors = 0
		i = self.lastExtension[0]
		j= self.lastExtension[1]
		if  i != len(self.grid)-1 and self.grid[i+1][j] == self.currentPath:
			neighboors = neighboors+1
		if i != 0 and self.grid[i-1][j] == self.currentPath:
			neighboors = neighboors+1
		if j != len(self.grid[0])-1 and self.grid[i][j+1] == self.currentPath:
			neighboors = neighboors+1
		if j != 0 and self.grid[i][j-1] == self.currentPath:
			neighboors = neighboors+1
		if neighboors == 2 :
			self.pathsCompleted[self.currentPath] = True
			return True
		return False
			
	def possibleActions(self):
		"""Return the possible actions possible on the current state"""
		actions = []
		"""print(self.grid)
		print(self.currentPath)
		print(self.lastExtension)"""
		i = self.lastExtension[0]
		j = self.lastExtension[1]
		if i != 0 and self.grid[i-1][j] == '.':
			actions.append("up")
		if i != len(self.grid)-1 and self.grid[i+1][j] == '.':
			actions.append("down")
		if j != 0 and self.grid[i][j-1] == '.':
			actions.append("left")
		if j != len(self.grid[0])-1 and self.grid[i][j+1] == '.':
			actions.append("right")
		return actions
		
	def __str__(self):
		print(self.grid)

###################### 
# Auxiliary function #
######################

directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]

def pathExists(grid, start, end):
	visited = [ [0 for j in range(0, len(grid[0]))] for i in range(0, len(grid)) ]
	ok = pathExistsDFS(grid, start, end, visited)
	return ok

def pathExistsDFS(grid, start, end, visited):
	for d in directions:
		i = start[0] + d[0]
		j = start[1] + d[1]
		next = [i, j]
		if i == end[0] and j == end[1]:
			return True
		if inBounds(grid, next) and grid[i][j] == '.' and not visited[i][j]:
			visited[i][j] = 1
			exists = pathExistsDFS(grid, next, end, visited)
			if exists:
				return True
	return False

def inBounds(grid, pos):
  return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

#####################
# Launch the search #
#####################

problem=NumberLink(sys.argv[1])
#example of bfs search
node=depth_first_graph_search(problem)
"""#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assuming that the __str__ function of states output the correct format"""

