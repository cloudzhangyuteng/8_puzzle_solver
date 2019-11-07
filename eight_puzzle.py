from queue import PriorityQueue
import copy
import time

trivial = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '*']]
veryEasy = [['1', '2', '3'], ['4', '5', '6'], ['7', '*', '8']]
easy = [['1', '2', '*'], ['4', '5', '3'], ['7', '8', '6']]
doable = [['*', '1', '2'], ['4', '5', '3'], ['7', '8', '6']]
oh_boy = [['8', '7', '1'], ['6', '*', '2'], ['5', '4', '3']]
impossible = [['1', '2', '3'], ['4', '5', '6'], ['8', '7', '*']]
goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '*']]

class Node:
    def __init__(self, data, gn, hn):
        self.data = data
        self.gn = gn
        self.hn = hn
        return

    def __lt__(self, other):
        if(self.hn + self.gn) < (other.gn + other.hn):
            return True
        else:
            return False

def printPuzzle(puzzle):
    print(*puzzle, sep = "\n")

def moveLeft(originPuzzle, x, y):
    puzzle = copy.deepcopy(originPuzzle)
    if puzzle[x][y] == puzzle[0][0] or puzzle[x][y] == puzzle[1][0] or puzzle[x][y] == puzzle[2][0]:
        return None
    else:
        tmp = puzzle[x][y-1]
        puzzle[x][y-1] = puzzle[x][y]
        puzzle[x][y] = tmp
        return puzzle

def moveRight(originPuzzle, x, y):
    puzzle = copy.deepcopy(originPuzzle)
    if puzzle[x][y] == puzzle[0][2] or puzzle[x][y] == puzzle[1][2] or puzzle[x][y] == puzzle[2][2]:
        return None
    else:
        tmp = puzzle[x][y+1]
        puzzle[x][y+1] = puzzle[x][y]
        puzzle[x][y] = tmp
        return puzzle

def moveUp(originPuzzle, x, y):
    puzzle = copy.deepcopy(originPuzzle)
    if puzzle[x][y] == puzzle[0][0] or puzzle[x][y] == puzzle[0][1] or puzzle[x][y] == puzzle[0][2]:
        return None
    else:
        tmp = puzzle[x-1][y]
        puzzle[x-1][y] = puzzle[x][y]
        puzzle[x][y] = tmp
        return puzzle

def moveDown(originPuzzle, x, y):
    puzzle = copy.deepcopy(originPuzzle)
    if puzzle[x][y] == puzzle[2][0] or puzzle[x][y] == puzzle[2][1] or puzzle[x][y] == puzzle[2][2]:
        return None
    else:
        tmp = puzzle[x+1][y]
        puzzle[x+1][y] = puzzle[x][y]
        puzzle[x][y] = tmp
        return puzzle

def findStar(puzzle):
    for i in puzzle:
        for j in i:
            if j == '*':
                return puzzle.index(i), i.index(j)

def misplacedTiles(puzzle):
    num_misplaced = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if  (puzzle[i][j] != goal[i][j]) and (puzzle[i][j] != '*'):
                num_misplaced += 1

    return num_misplaced

def manhattanDistance(puzzle):
    mdistance = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i][j] != '*':
                row_difference = abs(i - ((int(puzzle[i][j]) - 1) // 3))
                col_difference = abs(j - ((int(puzzle[i][j]) - 1) % 3))
                mdistance += row_difference + col_difference
    return mdistance

def generalSearch(puzzle, heuristic):
    print()
    checkDuplicate = []
    num_of_expand = 0
    cost = 0
    qSize = []

    q = PriorityQueue()
    q.put((0, Node(puzzle, 0, 0)))
    
    while not q.empty():
        tmp = q.get()
        checkDuplicate.append(tmp[1].data)

        #print("head")
        printPuzzle(tmp[1].data)
        print("current depth: ", tmp[1].gn)
        print()
        
        if tmp[1].data == goal:
            print("finish. found solution")
            print("number of nodes expanded: ", num_of_expand)
            if len(qSize) == 0:
                print("Max queue size: ", 0)
            else:
                print("Max queue size: ", max(qSize))
            print("Depth of solution: ", tmp[1].gn)
            return tmp[1].data
            break
        else:
            print("Expanding...")
            x, y = findStar(tmp[1].data)
            if y != 0:
                #print("move left")
                if heuristic == 1:
                    left = Node(moveLeft(tmp[1].data, x, y), tmp[1].gn + 1, 0)
                elif heuristic == 2:
                    left = Node(moveLeft(tmp[1].data, x, y), tmp[1].gn + 1, misplacedTiles(tmp[1].data))
                elif heuristic == 3:
                    left = Node(moveLeft(tmp[1].data, x, y), tmp[1].gn + 1, manhattanDistance(tmp[1].data))
                
                if left.data not in checkDuplicate:
                    q.put((left.gn + left.hn, left))
                    checkDuplicate.append(left.data)
                    num_of_expand += 1
#                    printPuzzle(left.data)
#                    print()

            if y != 2:
                #print("move right")
                if heuristic == 1:
                    right = Node(moveRight(tmp[1].data, x, y), tmp[1].gn + 1, 0)
                elif heuristic == 2:
                    right = Node(moveRight(tmp[1].data, x, y), tmp[1].gn + 1, misplacedTiles(tmp[1].data))
                elif heuristic == 3:
                    right = Node(moveRight(tmp[1].data, x, y), tmp[1].gn + 1, manhattanDistance(tmp[1].data))

                if right.data not in checkDuplicate:
                    q.put((right.gn + right.hn, right))
                    checkDuplicate.append(right.data)
                    num_of_expand += 1
#                    printPuzzle(right.data)
#                    print()

            if x != 0:
                #print("move up")
                if heuristic == 1:
                    up = Node(moveUp(tmp[1].data, x, y), tmp[1].gn + 1, 0)
                elif heuristic == 2:
                    up = Node(moveUp(tmp[1].data, x, y), tmp[1].gn + 1, misplacedTiles(tmp[1].data))
                elif heuristic == 3:
                    up = Node(moveUp(tmp[1].data, x, y), tmp[1].gn + 1, manhattanDistance(tmp[1].data))

                if up.data not in checkDuplicate:
                    q.put((up.gn + up.hn, up))
                    checkDuplicate.append(up.data)
                    num_of_expand += 1
#                    printPuzzle(up.data)
#                    print()

            if x != 2:
                #print("move down")
                if heuristic == 1:
                    down = Node(moveDown(tmp[1].data, x, y), tmp[1].gn + 1, 0)
                elif heuristic == 2:
                    down = Node(moveDown(tmp[1].data, x, y), tmp[1].gn + 1, misplacedTiles(tmp[1].data))
                elif heuristic == 3:
                    down = Node(moveDown(tmp[1].data, x, y), tmp[1].gn + 1, manhattanDistance(tmp[1].data))

                if down.data not in checkDuplicate:
                    q.put((down.gn + down.hn, down))
                    checkDuplicate.append(down.data)
                    num_of_expand += 1
#                    printPuzzle(down.data)
#                    print()
            qSize.append(q.qsize())

def main():
    puzzle = []
    
    choice = input("Welcome to Bertie Woosters 8-puzzle solver.\nType '1' to use a default puzzle, or '2' to enter your own puzzle\n")
    
    if choice == "1":
        choice2 = input("Enter '1' for Trival, '2' for Very Easy, '3' for Easy, '4' for Doable, '5' for Oh Boy, '6' for IMPOSSIBLE\n")
        if choice2 == "1":
            puzzle = trivial
        if choice2 == "2":
            puzzle = veryEasy
        if choice2 == "3":
            puzzle = easy
        if choice2 == "4":
            puzzle = doable
        if choice2 == "5":
            puzzle = oh_boy
        if choice2 == "6":
            puzzle = IMPOSSIBLE

    if choice == "2":
        row0, row1, row2 = ([],) * 3
        
        print("Enter your puzzle, use a * to represent the blank.")
        row0 = input("Enter the first row, use space or tabs between numbers:\n").split()
        puzzle.append(row0)
        row1 = input("Enter the second row, use space or tabs between numbers:\n").split()
        puzzle.append(row1)
        row2 = input("Enter the third row, use space or tabs between numbers:\n").split()
        puzzle.append(row2)

    print("\nYour puzzle is")
    printPuzzle(puzzle)
    print()
    choice3 = input("Enter your choice of algorithm:\n1. Uniform Cost Search\n2. A* with the Misplaced Tile heuristic\n3. A* with the Manhattan distance heuristic\n")

    start = 0
    end = 0
    if choice3 == "1":
        start = time.clock()
        generalSearch(puzzle, 1)
        end = time.clock()
        print("CPU time: ", end - start)
    if choice3 == "2":
        start = time.clock()
        generalSearch(puzzle, 2)
        end = time.clock()
        print("CPU time: ", end - start)
    if choice3 == "3":
        start = time.clock()
        generalSearch(puzzle, 3)
        end = time.clock()
        print("CPU time: ", end - start)

main()
