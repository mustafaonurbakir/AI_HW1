"""
Mustafa Onur Bakır
150130059

"""

from agent import Agent
import heapq


class Node():
    
    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, h_value):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir
        self.h = h_value
        
        self.seq = ""
        if (self.chosen_dir == "X"):
            pass
        else:
            self.seq = parent_node.seq + self.chosen_dir
    
    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h
       

class PriorityQueue: 
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


class AStarAgent(Agent):

    #Constants for frequently used variables.
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"
    APPLE = "A"
    FLOOR = "F"
    WALL = "W"
    PLAYER = "P"
    TRACE = "X"

    def __init__(self):
        super().__init__()

    #this function find the number of apples in the matrix
    def findNumberOfApples(self, initial_level_matrix):
        appleNumber = 0
        for row in initial_level_matrix:
            for unit in row:
                if unit == self.APPLE:
                    appleNumber += 1
        return appleNumber

    #this function calculate the distance between two coordinates
    def findManhattanDistance(self, player_row, player_col, apple_row, apple_col):
        vertical_distance = player_col - apple_col
        horizontal_distance = player_row - apple_row

        if vertical_distance < 0:
            vertical_distance *= -1
        if horizontal_distance < 0:
            horizontal_distance *= -1

        return horizontal_distance + vertical_distance

    #this function return the coordinates of nearest apple for current_node
    def findNearestApple(self, current_node):
        apples_position = []

        #find all apples coordinates
        for row in range(len(current_node.level_matrix)):
            for unit in range(len(current_node.level_matrix[row])):
                if current_node.level_matrix[row][unit] == self.APPLE:
                    apples_position.append([row, unit])

        shortest_dist = 0
        nearest_apple = []

        #compare distance for all apples
        for one_apple_position in apples_position:
            new_dist = self.findManhattanDistance(current_node.player_row, current_node.player_col, one_apple_position[0], one_apple_position[1])
            if new_dist < shortest_dist or shortest_dist == 0:
                shortest_dist = new_dist
                nearest_apple.clear()
                nearest_apple.append(one_apple_position[0])
                nearest_apple.append(one_apple_position[1])

        return nearest_apple

    #This function create a new matrix for movement of player
    def createMap(self, tempNode, direction):
        newMatrix = [aa[:] for aa in tempNode.level_matrix]
        newMatrix[tempNode.player_row][tempNode.player_col] = self.TRACE

        if direction == self.LEFT:
            newMatrix[tempNode.player_row][tempNode.player_col - 1] = self.PLAYER
        elif direction == self.RIGHT:
            newMatrix[tempNode.player_row][tempNode.player_col + 1] = self.PLAYER
        elif direction == self.UP:
            newMatrix[tempNode.player_row - 1][tempNode.player_col] = self.PLAYER
        elif direction == self.DOWN:
            newMatrix[tempNode.player_row + 1][tempNode.player_col] = self.PLAYER
        else:
            print("direction problem!")

        return newMatrix

    #This function clear the trace of player
    def clearTrace(self, level_matrix):
        for row in range(len(level_matrix)):
            for col in range(len(level_matrix[row])):
                if level_matrix[row][col] == self.TRACE:
                    level_matrix[row][col] = self.FLOOR
        return level_matrix

    #This function find route with A* algorithm.
    def aStarMove(self, starting, apple):

        queue = PriorityQueue()
        queue.put(starting, self.findManhattanDistance(starting.player_row, starting.player_col, apple[0], apple[1]))

        #this set the statistic value
        if queue.elements[0][0] > self.maximum_node_in_memory_count:
            self.maximum_node_in_memory_count = queue.elements[0][0]

        while True:
            currentNode = queue.get()

            #this calculate value for statistic
            self.generated_node_count += 1

            #if player reach the apple, return last node
            if currentNode.player_row == apple[0] and currentNode.player_col == apple[1]:
                return currentNode

            # look at left. if exist a way, add to list
            if currentNode.level_matrix[currentNode.player_row][currentNode.player_col - 1] == self.FLOOR or \
                    currentNode.level_matrix[currentNode.player_row][currentNode.player_col - 1] == self.APPLE:
                self.expanded_node_count += 1
                distance = self.findManhattanDistance(currentNode.player_row, currentNode.player_col - 1, apple[0], apple[1]) + 1
                queue.put(Node(currentNode, self.createMap(currentNode, self.LEFT), currentNode.player_row,
                                  currentNode.player_col - 1, currentNode.depth + 1, self.LEFT,
                                  distance), distance)

            # look at right. if exist a way, add to list
            if currentNode.level_matrix[currentNode.player_row][currentNode.player_col + 1] == self.FLOOR or \
                    currentNode.level_matrix[currentNode.player_row][currentNode.player_col + 1] == self.APPLE:
                self.expanded_node_count += 1
                distance = self.findManhattanDistance(currentNode.player_row, currentNode.player_col + 1, apple[0], apple[1]) + 1
                queue.put(Node(currentNode, self.createMap(currentNode, self.RIGHT), currentNode.player_row,
                                  currentNode.player_col + 1, currentNode.depth + 1, self.RIGHT,
                                  distance), distance)

            # look at up. if exist a way, add to list
            if currentNode.level_matrix[currentNode.player_row - 1][currentNode.player_col] == self.FLOOR or \
                    currentNode.level_matrix[currentNode.player_row - 1][currentNode.player_col] == self.APPLE:
                self.expanded_node_count += 1
                distance = self.findManhattanDistance(currentNode.player_row - 1, currentNode.player_col, apple[0], apple[1]) + 1
                queue.put(Node(currentNode, self.createMap(currentNode, self.UP), currentNode.player_row - 1,
                                  currentNode.player_col, currentNode.depth + 1, self.UP,
                                  distance), distance)

            # look at down. if exist a way, add to list
            if currentNode.level_matrix[currentNode.player_row + 1][currentNode.player_col] == self.FLOOR or \
                    currentNode.level_matrix[currentNode.player_row + 1][currentNode.player_col] == self.APPLE:
                self.expanded_node_count += 1
                distance = self.findManhattanDistance(currentNode.player_row + 1, currentNode.player_col, apple[0], apple[1]) + 1
                queue.put(Node(currentNode, self.createMap(currentNode, self.DOWN), currentNode.player_row + 1,
                                  currentNode.player_col, currentNode.depth + 1, self.DOWN,
                                  distance), distance)


    def solve(self, level_matrix, player_row, player_column):
        super().solve(level_matrix, player_row, player_column)

        initial_level_matrix = [list(row) for row in level_matrix]
        initial_h = None  #  fill this value with your heuristic function

        current_node = Node(None, initial_level_matrix, player_row, player_column, 0, "X", initial_h)

        #number of apples in the game
        number_of_apples = self.findNumberOfApples(initial_level_matrix)

        for i in range(number_of_apples):
            #coordinates of nearest apple for current node
            nearest_apple = self.findNearestApple(current_node)

            #player position and its target coordinates
            current_node = self.aStarMove(current_node, nearest_apple)

            #for the next apple, current node set
            current_node.chosen_dir = 'X'
            current_node.level_matrix = self.clearTrace(current_node.level_matrix)

        #current_node include the final road map
        return list(current_node.seq)