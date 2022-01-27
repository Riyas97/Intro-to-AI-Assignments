# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy

abcd = []

def printgrid(puzzle):
    for i in puzzle:
        for j in i:
            print j,
        print ""
    print ""

checked = 0

def select(puzzle, domain):
    global checked
    global abcd
    # printgrid(puzzle)

    checked += 1    
    x, y = (-1, -1)
    lim = 10
    lowest_degree = 30



    all_filled = True
    for i in range(0, 9):
        for j in range(0, 9):
            if puzzle[i][j] == 0:
                curr = len(domain[i][j])
                
                all_filled = False

                if curr == 0:
                    return False
                
                deg =  count_degree(puzzle, i, j)

                if curr < lim or (curr == lim and deg < lowest_degree):
                    x, y = (i, j)
                    lim = curr
                    lowest_degree = deg

    if all_filled:
        abcd = copy.deepcopy(puzzle)
        # printgrid(abcd)
        return True
    
    for i in domain[x][y]:
        domain2 = copy.deepcopy(domain)
        puzzle2 = copy.deepcopy(puzzle)
        puzzle2[x][y] = i
        remove(puzzle2, domain2, x, y)
        result = select(puzzle2, domain2)
        if result:
            return True
    
    return False
    
def remove(puzzle, domain, i, j):
    num = puzzle[i][j]

    for k in range(9):
        domain[i][k].discard(num)
        domain[k][j].discard(num)

    i2 = 3 * (i // 3)
    j2 = 3 * (j // 3)
    for ii in range(3):
        for jj in range(3):
            domain[i2 + ii][j2 + jj].discard(puzzle[i][j])

def count_degree(puzzle, i, j):
    count = 0
    for k in range(9):
        if puzzle[i][k] == 0:
            count += 1
        if puzzle[k][j] == 0:
            count += 1
    
    i2 = 3 * (i // 3)
    j2 = 3 * (j // 3)
    for ii in range(3):
        for jj in range(3):
            if puzzle[ii+i2][jj+j2] == 0:
                count += 1

    count -= 3
    return count

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def set_domain(self):
        return 

    def solve(self):
        # TODO: Write your code here
        self.domain = [[set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(0, 9)] for _ in range(0,9)]
        for i in range (0, 9):
            for j in range (0, 9):
                if self.puzzle[i][j] != 0:
                    self.domain[i][j] = set([self.puzzle[i][j]]) 
                    for k in range (0,9):
                        self.domain[i][k].discard(self.puzzle[i][j])
                        self.domain[k][j].discard(self.puzzle[i][j])

                    i2 = 3 * (i // 3)
                    j2 = 3 * (j // 3)
                    for ii in range(3):
                        for jj in range(3):
                            # print i, j, ii +i2, jj+j2
                            self.domain[i2 + ii][j2 + jj].discard(self.puzzle[i][j])

        
        select(self.puzzle, self.domain)

        printgrid(abcd)
        print checked


        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

    


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
