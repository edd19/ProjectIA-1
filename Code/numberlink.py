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
		pass

	def goal_test(self, state):
		pass
    
	def successor(self, state):
		if state.connected():
			"choose a new path and verify if that path is possible"
		else:
			"do a while loop with all action possible, it must be a yield"

###############		
# State class #
###############

class State:
	"""State representation of a numberlink problem.
		The grid is represented by a matrix (double dimension table) with the top left corner represented by grid[0][0].
		The currentPath indicates the current path in construction (a character).
		The lastExtension variable stores the coordinates (x,y) of the last element extented (a table with two value for x and y)."""
	def __init__(self, grid, currentPath, lastExtension):
		self.grid = grid
		self.currentPath = currentPath	
		self.lastExtension = lastExtension	
			
	def action(action):
		"""Apply the action on the grid based on the currentPath and the lastExtension coordinates.
			The action should be a string with the value of ["right", "down", "left", "up"] that indicates in which direction the lastExtension
			should be extented"""
		i = lastExtension[0]
		j= lastExtension[1]
		if action == "left":
			i = i-1
		elif action == "right":
			i = i+1
		elif action == "down":
			j = j+1
		elif action == "up":
			j = j-1
		grid[i][j] = currentPath
		lastExtension[0] = i
		lastExtension[1] = j
		
	def connected(self):
		"""Check if the currentPath is finished. 
		For that we check if the last element extented has 2 neighboors from the same path (with the same character)."""
		neighboors = 0
		i = lastExtension[0]
		j= lastExtension[1]
		if grid[i+1][j] == currentPath:
			neighboors = neighboors+1
		if grid[i-1][j] == currentPath:
			neighboors = neighboors+1
		if grid[i][j+1] == currentPath:
			neighboors = neighboors+1
		if grid[i][j-1] == currentPath:
			neighboors = neighboors+1
		return (neighboors==2)
			
	def possibleActions(self):
		"""Return the possible actions possible on the current state"""
		actions = []
		i = lastExtension[0]
		j= lastExtension[1]
		if i != 0 and grid[i-1][j] == '.':
			actions.append("left")
		if i != len(actions) and grid[i+1][j] == '.':
			actions.append("right")
		if j != 0 and grid[i][j+1] == '.':
			actions.append("down")
		if j != len(actions[0]) and grid[i][j-1] == '.':
			actions.append("up")
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
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assuming that the __str__ function of states output the correct format

