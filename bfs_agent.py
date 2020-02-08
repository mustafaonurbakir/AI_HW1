import time
import random
from copy import deepcopy
from agent import Agent


#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


"""
  you may use the following Node class
  modify it if needed, or create your own
"""
class Node():
	
	def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, collected_apples, there_is_no_way):
		self.parent_node = parent_node
		self.level_matrix = level_matrix
		self.player_row = player_row
		self.player_col = player_column
		self.depth = depth
		self.chosen_dir = chosen_dir
		self.collected_apples = collected_apples
		self.there_is_no_way = there_is_no_way

		self.seq = ""
		#print(self.chosen_dir)
		if (self.chosen_dir == "X"):
			pass
		else:
			self.seq = parent_node.seq + self.chosen_dir



class BFSAgent(Agent):

	LEFT = "L"
	RIGHT = "R"
	UP = "U"
	DOWN = "D"
	APPLE = "A"
	FLOOR = "F"
	WALL = "W"
	
	def __init__(self):
		super().__init__()

	def createMap(self, currentNode, direction):
		newMatrix = currentNode.level_matrix
		newMatrix[currentNode.player_row][currentNode.player_col] = "F"
		if direction == self.LEFT:
			newMatrix[currentNode.player_row][currentNode.player_col - 1] = "P"
		elif direction == self.RIGHT:
			newMatrix[currentNode.player_row][currentNode.player_col + 1] = "P"
		elif direction == self.UP:
			newMatrix[currentNode.player_row - 1][currentNode.player_col] = "P"
		elif direction == self.DOWN:
			newMatrix[currentNode.player_row + 1][currentNode.player_col] = "P"
		else:
			print("direction problem. line:58")
		return newMatrix
		
	def findNumberOfApples(self, initial_level_matrix):
		appleNumber = 0
		for row in initial_level_matrix:
			for unit in row:
				if unit == self.APPLE:
					appleNumber += 1
		return appleNumber
	
	def solve(self, level_matrix, player_row, player_column):
		super().solve(level_matrix, player_row, player_column)
		move_sequence = []
		
		"""
			YOUR CODE STARTS HERE
			fill move_sequence list with directions chars
		"""
		
		initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
		s0 = Node(None, initial_level_matrix, player_row, player_column, 0, "X", 0, False)

		#empty map
		empty_matrix = initial_level_matrix
		empty_matrix[s0.player_row][s0.player_col] = 'F'
		
		#number of apples
		number_of_apples = self.findNumberOfApples(initial_level_matrix)
		print("elma: " + str(number_of_apples))
		
		#queue for BFS
		queue = []
		queue.append(s0)
		
		nodeNumber = 0
		
		while queue:
			if nodeNumber % 100 == 0:
				print(nodeNumber)
		
			print(queue[0].player_col)
			time.sleep(.5)
			currentNode = queue.pop(0)
			
			there_is_no_way = False
			
			#look at left
			if (currentNode.chosen_dir != self.RIGHT and not currentNode.there_is_no_way) or there_is_no_way:
				if currentNode.level_matrix[currentNode.player_row][currentNode.player_col - 1] == self.FLOOR:
					queue.append(Node(currentNode, self.createMap(currentNode, self.LEFT), currentNode.player_row, currentNode.player_col - 1, currentNode.depth + 1, self.LEFT, currentNode.collected_apples, there_is_no_way))
					#print("sol")
					nodeNumber += 1
				if currentNode.level_matrix[currentNode.player_row][currentNode.player_col - 1] == self.APPLE:
					if currentNode.collected_apples + 1 == number_of_apples:
						#this is a solution
						solution_node = Node(currentNode, self.createMap(currentNode, self.LEFT), currentNode.player_row, currentNode.player_col - 1, currentNode.depth + 1, self.LEFT, currentNode.collected_apples + 1, there_is_no_way)
						nodeNumber += 1
						move_sequence = list(solution_node.seq)
						print("tttttttt")
						break
					else:
						queue.append(Node(currentNode, self.createMap(currentNode, self.LEFT), currentNode.player_row, currentNode.player_col - 1, currentNode.depth + 1, self.LEFT, currentNode.collected_apples + 1, there_is_no_way))
						nodeNumber += 1
				there_is_no_way = False
					
			#look at right
			elif (currentNode.chosen_dir != self.LEFT and not currentNode.there_is_no_way) or there_is_no_way:
				if currentNode.level_matrix[currentNode.player_row][currentNode.player_col + 1] == self.FLOOR:
					queue.append(Node(currentNode, self.createMap(currentNode, self.RIGHT), currentNode.player_row, currentNode.player_col + 1, currentNode.depth + 1, self.RIGHT, currentNode.collected_apples, there_is_no_way))
					nodeNumber += 1
					#print("sag")
				if currentNode.level_matrix[currentNode.player_row][currentNode.player_col + 1] == self.APPLE:
					if currentNode.collected_apples + 1 == number_of_apples:
						#this is a solution
						solution_node = Node(currentNode, self.createMap(currentNode, self.RIGHT), currentNode.player_row, currentNode.player_col + 1, currentNode.depth + 1, self.RIGHT, currentNode.collected_apples + 1, there_is_no_way)
						move_sequence = list(solution_node.seq)
						print("lllllllll")
						break
					else:
						queue.append(Node(currentNode, self.createMap(currentNode, self.RIGHT), currentNode.player_row, currentNode.player_col + 1, currentNode.depth + 1, self.RIGHT, currentNode.collected_apples + 1, there_is_no_way))
						nodeNumber += 1
				there_is_no_way = False
			
			#look at up
			elif (currentNode.chosen_dir != self.DOWN and  not currentNode.there_is_no_way) or there_is_no_way:
				if currentNode.level_matrix[currentNode.player_row - 1][currentNode.player_col] == self.FLOOR:
					queue.append(Node(currentNode, self.createMap(currentNode, self.UP), currentNode.player_row - 1, currentNode.player_col, currentNode.depth + 1, self.UP, currentNode.collected_apples, there_is_no_way))
					#print("yukari")
					nodeNumber += 1
				if currentNode.level_matrix[currentNode.player_row - 1][currentNode.player_col] == self.APPLE:
					if currentNode.collected_apples + 1 == number_of_apples:
						#this is a solution
						solution_node = Node(currentNode, self.createMap(currentNode, self.UP), currentNode.player_row - 1, currentNode.player_col, currentNode.depth + 1, self.UP, currentNode.collected_apples + 1, there_is_no_way)
						move_sequence = list(solution_node.seq)
						print("3. bolme")
						break
					else:
						queue.append(Node(currentNode, self.createMap(currentNode, self.UP), currentNode.player_row - 1, currentNode.player_col, currentNode.depth + 1, self.UP, currentNode.collected_apples + 1, there_is_no_way))
						nodeNumber += 1
				there_is_no_way = False
			
			#look at down
			elif (currentNode.chosen_dir != self.UP and  not currentNode.there_is_no_way) or there_is_no_way:
				if currentNode.level_matrix[currentNode.player_row + 1][currentNode.player_col] == self.FLOOR: 
					queue.append(Node(currentNode, self.createMap(currentNode, self.DOWN), currentNode.player_row + 1, currentNode.player_col, currentNode.depth + 1, self.DOWN, currentNode.collected_apples, there_is_no_way))
					#print("asagi")
					nodeNumber += 1
				if currentNode.level_matrix[currentNode.player_row + 1][currentNode.player_col] == self.APPLE:
					if currentNode.collected_apples + 1 == number_of_apples:
						#this is a solution
						solution_node = Node(currentNode, self.createMap(currentNode, self.DOWN), currentNode.player_row + 1, currentNode.player_col, currentNode.depth + 1, self.DOWN, currentNode.collected_apples + 1, there_is_no_way)
						move_sequence = list(solution_node.seq)
						print("4. bolme")
						break
					else:
						queue.append(Node(currentNode, self.createMap(currentNode, self.DOWN), currentNode.player_row + 1, currentNode.player_col, currentNode.depth + 1, self.DOWN, currentNode.collected_apples + 1, there_is_no_way))
						nodeNumber += 1
				there_is_no_way = False
			
			else:
				there_is_no_way = True
		
		
		
		
		"""
			YOUR CODE ENDS HERE
			return move_sequence
		"""
		return move_sequence
		
		