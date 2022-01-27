# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy
import time

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.domain = [[set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(0, 9)] for _ in range(0,9)]

    def obtain_init_domain(self):
        """
        Responsible for obtaining domain for every grid location
        """
        for i in range (0, 9):
            for j in range (0, 9):
                if self.puzzle[i][j] != 0:
                    self.domain[i][j] = set([self.puzzle[i][j]]) 
                    for k in range (0, 9):
                        # remove from same row, same column
                        self.domain[i][k].discard(self.puzzle[i][j])
                        self.domain[k][j].discard(self.puzzle[i][j])
                    # remove from 3x3 block
                    i2 = 3 * (i // 3)
                    j2 = 3 * (j // 3)
                    for ii in range(3):
                        for jj in range(3):
                            self.domain[i2 + ii][j2 + jj].discard(self.puzzle[i][j])
    
    def select_unassigned_var(self):
        """
        Responsible for choosing unassigned variable (if any)
        Uses MRV heruistic
        """
        selected_x, selected_y = (-1, -1)
        lim = 10
        for i in range(0, 9):
            for j in range(0, 9):
                if self.puzzle[i][j] == 0:
                    curr = len(self.domain[i][j])
                    if curr < lim:
                        lim = curr
                        selected_x, selected_y = (i, j)
        return selected_x, selected_y
        
    def inference(self, value, x, y):
        """
        Does one step forward checking
        Updates domain of puzzle[x][y] and its neighbours in same row, column and grid
        """
        # to store whether inference returns failure
        infer_failure = False 
        # to store all the values not satisfied for a grid location
        inference = {} 
        inference[(x, y)] = self.domain[x][y] 

        # update domain to value 
        self.domain[x][y] = set([value]) 
        
        # update domain of neighbours in same row, column and grid
        for k in range(0, 9):
            if k != x:
                if value in self.domain[k][y]:
                    inference[(k, y)] = value
                    self.domain[k][y].discard(value)
                    if len(self.domain[k][y]) == 0:
                        infer_failure = True
            if k != y:
                if value in self.domain[x][k]:
                    inference[(x, k)] = value
                    self.domain[x][k].discard(value)
                    if len(self.domain[x][k]) == 0:
                        infer_failure = True

        i2 = 3 * (x // 3)
        j2 = 3 * (y // 3)
        for ii in range(3):
            for jj in range(3):
                if i2 + ii != x and j2 + jj != y:
                    if value in self.domain[i2 + ii][j2 + jj]:
                        inference[(i2 + ii, j2 + jj)] = value
                        self.domain[i2 + ii][j2 + jj].discard(value)
                        if len(self.domain[i2 + ii][j2 + jj]) == 0:
                            infer_failure = True

        return (inference, infer_failure)
    
    def backtrack_search(self):
        x, y = self.select_unassigned_var()
        if x == -1:
            # no unassigned variable left
            return True
        for value in self.domain[x][y]:
            self.puzzle[x][y] = value
            inference, infer_failure = self.inference(value, x, y)
            if infer_failure is False:
                result = self.backtrack_search()
                if result != False:
                    return result
            self.puzzle[x][y] = 0
            for i, j in inference:
                # set the domain back
                if i == x and j == y:
                    self.domain[i][j] = inference[(i, j)]
                else:
                    self.domain[i][j].add(inference[(i, j)])
        
        return False
    
    def solve(self):
        # TODO: Write your code here
        self.obtain_init_domain()
        self.backtrack_search()
        return self.puzzle

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

    # start = time.time()
    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()
    # print time.time()-start

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
