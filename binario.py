import time
import numpy as np
import collections

def printSukodu(sudoku):
    n = sudoku.shape[0]
    for i in range(0, n):
        for j in range(0, n):
            if sudoku[i, j] == -1:
                print(' ', end='')
            else:
                print(sudoku[i, j], end='')
        print()
    print('-----------')

def readPuzzle(sudoku, filename):
    with open(filename, 'r', encoding='utf-8') as file:
        puzzle = file.readlines()
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i].strip())):
            try:
                sudoku[i, j] = int(puzzle[i][j])
            except:
                sudoku[i, j] = -1

def getNextIndex(sudoku, i, j):
    n = sudoku.shape[0]
    for row in range(i, n):
        for col in range(j, n):
            if sudoku[row, col] == -1:
                return row, col
    for row in range(0, n):
        for col in range(0, n):
            if sudoku[row, col] == -1:
                return row, col
    return None, None

def isValid01Number(sudoku, i, j):
    n = sudoku.shape[0]
    if j == None:
        cnt = collections.Counter(sudoku[i, :])
    else:
        cnt = collections.Counter(sudoku[:, j])
    for key in cnt:
        if key != -1 and cnt[key] > (n // 2):
            return False
    return True

def isValidRow(sudoku, i):
    if -1 in sudoku[i, :]:
        return True
    n = sudoku.shape[0]
    target = sudoku[i, :]
    for r in range(0, n):
        if r == i:
            continue
        row = sudoku[r, :]
        if np.array_equal(target, row):
            return False
    return True

def isValidCol(sudoku, j):
    if -1 in sudoku[:, j]:
        return True
    n = sudoku.shape[0]
    target = sudoku[:, j]
    for c in range(0, n):
        if c == j:
            continue
        col = sudoku[:, c]
        if np.array_equal(target, col):
            return False
    return True

def isValidTriple(sudoku, i, j):
    n = sudoku.shape[0]
    if j-2 >= 0:
        triple = set(sudoku[i, j-2:j+1])
        if len(triple) == 1:
            return False
    if j-1 >= 0 and j+2 <= n:
        triple = set(sudoku[i, j-1:j+2])
        if len(triple) == 1:
            return False
    if j+3 <= n:
        triple = set(sudoku[i, j:j+3])
        if len(triple) == 1:
            return False
    if i-2 >= 0:
        triple = set(sudoku[i-2:i+1, j].T)
        if len(triple) == 1:
            return False
    if i-1 >= 0 and i+2 <= n:
        triple = set(sudoku[i-1:i+2, j].T)
        if len(triple) == 1:
            return False
    if i+3 <= n:
        triple = set(sudoku[i:i+3, j].T)
        if len(triple) == 1:
            return False
    
    return True

def isValid(sudoku, i, j):
    if not isValidTriple(sudoku, i, j):
        return False
    if not isValid01Number(sudoku, i, None):
        return False
    if not isValid01Number(sudoku, None, j):
        return False
    if not isValidRow(sudoku, i):
        return False
    if not isValidCol(sudoku, j):
        return False
    return True

def solve(sudoku, i, j):
    i, j = getNextIndex(sudoku, i, j)
    if i == None:
        return True
    for num in [0, 1]:
        old = sudoku[i, j]
        sudoku[i, j] = num
        if isValid(sudoku, i, j):
            if solve(sudoku, i, j):
                return True
            sudoku[i, j] = old
        else:
            sudoku[i, j] = old
    return False

if __name__ == '__main__':
    for n in [6, 8, 12]:
        START = time.time()
        sudoku = np.ones((n, n), dtype=np.int32) * -1
        readPuzzle(sudoku, f'puzzle_{n}x{n}.txt')
        printSukodu(sudoku)
        solve(sudoku, 0, 0)
        printSukodu(sudoku)
        print(f'{time.time() - START}(s)')
