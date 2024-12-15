import numpy as np
import time

class SudokuComparison:
    def __init__(self):
        # Test tabla za poređenje backtracking algoritam vs. dinamičko programiranje
        self.test_board = np.array([
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
        ])

    def backtracking_solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row, col] = num
                if self.backtracking_solve(board):
                    return True
                board[row, col] = 0
        return False

    def dynamic_solve(self, board):
        # Dinamičko programiranje koje koristi memorijsku matricu za praćenje mogućih vrijednosti
        possibilities = {}
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    possibilities[(i, j)] = self.get_possible_values(board, i, j)
        
        return self.solve_dynamic(board, possibilities)

    def solve_dynamic(self, board, possibilities):
        if not possibilities:
            return True
        
        # Biramo polje sa najmanje mogućih vrijednosti
        pos = min(possibilities.items(), key=lambda x: len(x[1]))
        i, j = pos[0]
        possible_values = pos[1]
        
        for num in possible_values:
            if self.is_valid(board, i, j, num):
                board[i, j] = num
                old_possibilities = possibilities.copy()
                possibilities.pop((i, j))
                # Ažuriramo mogućnosti za povezana polja
                self.update_possibilities(board, possibilities, i, j)
                
                if self.solve_dynamic(board, possibilities):
                    return True
                    
                board[i, j] = 0
                possibilities = old_possibilities
                
        return False

    def compare_performance(self):
        # Test za backtracking
        board_backtrack = self.test_board.copy()
        start_time = time.time()
        self.backtracking_solve(board_backtrack)
        backtrack_time = time.time() - start_time
        
        # Test za dinamičko programiranje
        board_dynamic = self.test_board.copy()
        start_time = time.time()
        self.dynamic_solve(board_dynamic)
        dynamic_time = time.time() - start_time
        
        print(f"Rezultati poređenja:")
        print(f"Backtracking vrijeme: {backtrack_time:.6f} sekundi")
        print(f"Dinamičko programiranje vrijeme: {dynamic_time:.6f} sekundi")
        print(f"Razlika (Dinamičko programiranje - Backtracking algoritam): {(dynamic_time - backtrack_time):.6f} sekundi")

    # Pomoćne metode
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, row, col, num):
        # Provjera reda i kolone
        for x in range(9):
            if board[row, x] == num or board[x, col] == num:
                return False
                
        # Provjera 3x3 box-a
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i, j] == num:
                    return False
        return True

    def get_possible_values(self, board, row, col):
        values = set(range(1, 10))
        # Uklanjamo brojeve koji se već nalaze u redu, koloni i box-u
        for i in range(9):
            values.discard(board[row, i])
            values.discard(board[i, col])
            
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                values.discard(board[i, j])
        return values

    def update_possibilities(self, board, possibilities, row, col):
        # Ažurira mogućnosti za sva povezana polja
        for i in range(9):
            if (i, col) in possibilities:
                possibilities[(i, col)] = self.get_possible_values(board, i, col)
            if (row, i) in possibilities:
                possibilities[(row, i)] = self.get_possible_values(board, row, i)
                
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i, j) in possibilities:
                    possibilities[(i, j)] = self.get_possible_values(board, i, j)

# Pokretanje poređenja
if __name__ == "__main__":
    sudoku = SudokuComparison()
    sudoku.compare_performance()