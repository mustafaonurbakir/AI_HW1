"""
Mustafa Onur Bakır
150130059

"""

from agent import Agent

class Node():
	
	def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, collected_apples):
		self.parent_node = parent_node
		self.level_matrix = level_matrix
		self.player_row = player_row
		self.player_col = player_column
		self.depth = depth
		self.chosen_dir = chosen_dir
		self.collected_apples = collected_apples

		self.seq = ""
		if (self.chosen_dir == "X"):
			pass
		else:
			self.seq = parent_node.seq + self.chosen_dir



class BFSAgent(Agent):

	# Constants for frequently used variables.
	LEFT = "L"
	RIGHT = "R"
	UP = "U"
	DOWN = "D"
	APPLE = "A"
	FLOOR = "F"
	WALL = "W"
	PERSON = "P"
	
	def __init__(self):
		super().__init__()

	# this function find the number of apples in the matrix
	def findNumberOfApples(self, initial_level_matrix):
		appleNumber = 0
		for row in initial_level_matrix:
			for unit in row:
				if unit == self.APPLE:
					appleNumber += 1
		return appleNumber

	# This function create a new matrix for movement of player
	def createMap(self, tempNode, direction):
		newMatrix = [aa[:] for aa in tempNode.level_matrix]
		newMatrix[tempNode.player_row][tempNode.player_col] = self.FLOOR

		if direction == self.LEFT:
			newMatrix[tempNode.player_row][tempNode.player_col - 1] = self.PERSON
		elif direction == self.RIGHT:
			newMatrix[tempNode.player_row][tempNode.player_col + 1] = self.PERSON
		elif direction == self.UP:
			newMatrix[tempNode.player_row - 1][tempNode.player_col] = self.PERSON
		elif direction == self.DOWN:
			newMatrix[tempNode.player_row + 1][tempNode.player_col] = self.PERSON
		else:
			print("direction problem. line:67")

		return newMatrix

	# This function find route with BFS algorithm.
	def solve(self, level_matrix, player_row, player_column):
		super().solve(level_matrix, player_row, player_column)
		move_sequence = []

		# initial node
		initial_level_matrix = [list(row) for row in level_matrix]
		s0 = Node(None, initial_level_matrix, player_row, player_column, 0, "X", 0)

		#number of apples
		number_of_apples = self.findNumberOfApples(initial_level_matrix)
		print("elma: " + str(number_of_apples))
		
		# list as a queue for BFS
		queue = []
		queue.append(s0)

		max_collexted_apple = 0

		expandedNodeNumber = 0
		travelNodeNumber = 0
		maxNodeInMemory = 0
		
		while queue:

			if len(queue) > maxNodeInMemory:
				maxNodeInMemory = len(queue)

			currentNode = queue.pop(0)
			travelNodeNumber += 1

			#look at left
			if currentNode.level_matrix[currentNode.player_row][currentNode.player_col - 1] == self.FLOOR:
				#if currentNode.collected_apples == max_collexted_apple and currentNode.seq[-2:] != "LR":
				if currentNode.seq[-4:] != "LDRU" and currentNode.seq[-4:] != "LURD" and currentNode.seq[-2:] != "LR":
					queue.append(Node(currentNode, self.createMap(currentNode, self.LEFT), currentNode.player_row, currentNode.player_col - 1, currentNode.depth + 1, self.LEFT, currentNode.collected_apples))
					expandedNodeNumber += 1
			elif currentNode.level_matrix[currentNode.player_row][currentNode.player_col - 1] == self.APPLE:
				# This is an apple
				if currentNode.collected_apples + 1 == number_of_apples:
					#this is a solution
					solution_node = Node(currentNode, self.createMap(currentNode, self.LEFT), currentNode.player_row, currentNode.player_col - 1, currentNode.depth + 1, self.LEFT, currentNode.collected_apples + 1)
					expandedNodeNumber += 1
					move_sequence = list(solution_node.seq)
					break
				else:
					#queue.clear()
					queue.append(Node(currentNode, self.createMap(currentNode, self.LEFT), currentNode.player_row, currentNode.player_col - 1, currentNode.depth + 1, self.LEFT, currentNode.collected_apples + 1))
					expandedNodeNumber += 1
					max_collexted_apple += 1
					
			#look at right
			if currentNode.level_matrix[currentNode.player_row][currentNode.player_col + 1] == self.FLOOR:
				#if currentNode.collected_apples == max_collexted_apple and currentNode.seq[-2:] != "RL":
				if currentNode.seq[-4:] != "RULD" and currentNode.seq[-4:] != "RDLU" and currentNode.seq[-2:] != "RL":
					queue.append(Node(currentNode, self.createMap(currentNode, self.RIGHT), currentNode.player_row, currentNode.player_col + 1, currentNode.depth + 1, self.RIGHT, currentNode.collected_apples))
					expandedNodeNumber += 1
			elif currentNode.level_matrix[currentNode.player_row][currentNode.player_col + 1] == self.APPLE:
				# This is an apple
				if currentNode.collected_apples + 1 == number_of_apples:
					#this is a solution
					solution_node = Node(currentNode, self.createMap(currentNode, self.RIGHT), currentNode.player_row, currentNode.player_col + 1, currentNode.depth + 1, self.RIGHT, currentNode.collected_apples + 1)
					expandedNodeNumber += 1
					move_sequence = list(solution_node.seq)
					break
				else:
					#queue.clear()
					queue.append(Node(currentNode, self.createMap(currentNode, self.RIGHT), currentNode.player_row, currentNode.player_col + 1, currentNode.depth + 1, self.RIGHT, currentNode.collected_apples + 1))
					expandedNodeNumber += 1
					max_collexted_apple += 1

			#look at up
			if currentNode.level_matrix[currentNode.player_row - 1][currentNode.player_col] == self.FLOOR:
				#if currentNode.collected_apples == max_collexted_apple and currentNode.seq[-2:] != "UD":
				if currentNode.seq[-4:] != "ULDR" and currentNode.seq[-4:] != "URDL" and currentNode.seq[-2:] != "UD":
					queue.append(Node(currentNode, self.createMap(currentNode, self.UP), currentNode.player_row - 1, currentNode.player_col, currentNode.depth + 1, self.UP, currentNode.collected_apples))
					expandedNodeNumber += 1
			elif currentNode.level_matrix[currentNode.player_row - 1][currentNode.player_col] == self.APPLE:
				# This is an apple
				if currentNode.collected_apples + 1 == number_of_apples:
					#this is a solution
					solution_node = Node(currentNode, self.createMap(currentNode, self.UP), currentNode.player_row - 1, currentNode.player_col, currentNode.depth + 1, self.UP, currentNode.collected_apples + 1)
					expandedNodeNumber += 1
					move_sequence = list(solution_node.seq)
					break
				else:
					#queue.clear()
					queue.append(Node(currentNode, self.createMap(currentNode, self.UP), currentNode.player_row - 1, currentNode.player_col, currentNode.depth + 1, self.UP, currentNode.collected_apples + 1))
					expandedNodeNumber += 1
					max_collexted_apple += 1

			#look at down
			if currentNode.level_matrix[currentNode.player_row + 1][currentNode.player_col] == self.FLOOR:
				#if currentNode.collected_apples == max_collexted_apple and currentNode.seq[-2:] != "DU":
				if currentNode.seq[-4:] != "DLUR" and currentNode.seq[-4:] != "DRUL" and currentNode.seq[-2:] != "DU":
					queue.append(Node(currentNode, self.createMap(currentNode, self.DOWN), currentNode.player_row + 1, currentNode.player_col, currentNode.depth + 1, self.DOWN, currentNode.collected_apples))
					expandedNodeNumber += 1
			elif currentNode.level_matrix[currentNode.player_row + 1][currentNode.player_col] == self.APPLE:
				# This is an apple
				if currentNode.collected_apples + 1 == number_of_apples:
					#this is a solution
					solution_node = Node(currentNode, self.createMap(currentNode, self.DOWN), currentNode.player_row + 1, currentNode.player_col, currentNode.depth + 1, self.DOWN, currentNode.collected_apples + 1)
					expandedNodeNumber += 1
					move_sequence = list(solution_node.seq)
					break
				else:
					#queue.clear()
					queue.append(Node(currentNode, self.createMap(currentNode, self.DOWN), currentNode.player_row + 1, currentNode.player_col, currentNode.depth + 1, self.DOWN, currentNode.collected_apples + 1))
					expandedNodeNumber += 1
					max_collexted_apple += 1

		self.expanded_node_count = expandedNodeNumber
		self.generated_node_count = travelNodeNumber
		self.maximum_node_in_memory_count = maxNodeInMemory

		return move_sequence