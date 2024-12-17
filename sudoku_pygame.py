import pygame
import numpy as np

# Inicijalizacija Pygame-a
pygame.init()

# Konstante za igru
WINDOW_SIZE = 540  # Veličina prozora
CELL_SIZE = WINDOW_SIZE // 9  # Veličina pojedinačne ćelije
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class SudokuGameGUI:
    def __init__(self):
        # Kreiranje prozora igre
        self.window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Sudoku Solver koji koristi Backtracking algoritam")
        
        # Inicijalizacija početne table
        self.board = np.array([
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
        self.original = self.board.copy()  # Čuvamo originalne brojeve
        self.selected = None  # Trenutno selektovano polje
        self.hint_cell = None  # Polje za koje je dat prijedlog
        
    def is_complete(self):
        # Provjera da li su sva polja popunjena
        if 0 in self.board:
            return False
            
        # Provjera da li su svi redovi i kolone validni
        for i in range(9):
            if not (sorted(self.board[i]) == list(range(1, 10)) and 
                    sorted(self.board[:, i]) == list(range(1, 10))):
                return False
                
        # Provjera 3x3 kvadrata
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        box.append(self.board[i][j])
                if sorted(box) != list(range(1, 10)):
                    return False
                    
        return True

    def draw_grid(self):
        # Crtanje osnovne mreže
        self.window.fill(WHITE)
        
        # Crtanje ćelija i brojeva
        for i in range(9):
            for j in range(9):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                
                pygame.draw.rect(self.window, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
                
                if self.board[i][j] != 0:
                    color = BLUE if self.original[i][j] != 0 else BLACK
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(self.board[i][j]), True, color)
                    text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                    self.window.blit(text, text_rect)
        
        # Crtanje debljih linija za 3x3 kvadrate
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.window, BLACK, (i * CELL_SIZE, 0), 
                           (i * CELL_SIZE, WINDOW_SIZE), thickness)
            pygame.draw.line(self.window, BLACK, (0, i * CELL_SIZE), 
                           (WINDOW_SIZE, i * CELL_SIZE), thickness)
        
        # Označavanje selektovanog polja
        if self.selected:
            x, y = self.selected
            pygame.draw.rect(self.window, GRAY, 
                           (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        
        # Označavanje polja sa predlogom
        if self.hint_cell:
            x, y, _ = self.hint_cell
            pygame.draw.rect(self.window, GREEN, 
                           (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    def is_valid_move(self, row, col, num):
        # Provjera validnosti poteza
        if num in self.board[row] or num in self.board[:, col]:
            return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve_with_backtracking(self, board):
        # Implementacija backtracking algoritma
        empty = self.find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                board[row, col] = num
                if self.solve_with_backtracking(board):
                    return True
                board[row, col] = 0
        return False

    def find_empty(self, board):
        # Pronalaženje prvog praznog polja
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    return (i, j)
        return None

    def get_hint(self):
        # Generisanje prijedloga za sljedeći potez
        temp_board = self.board.copy()
        if self.solve_with_backtracking(temp_board):
            for i in range(9):
                for j in range(9):
                    if self.board[i, j] == 0:
                        return (i, j, temp_board[i, j])
        return None

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                    self.selected = (x, y)
                    self.hint_cell = None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        hint = self.get_hint()
                        if hint:
                            self.hint_cell = hint
                    
                    elif self.selected and self.original[self.selected[0]][self.selected[1]] == 0:
                        x, y = self.selected
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                       pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                            num = int(event.unicode)
                            if self.is_valid_move(x, y, num):
                                self.board[x][y] = num
                                self.hint_cell = None
                        elif event.key == pygame.K_BACKSPACE:
                            self.board[x][y] = 0
                            self.hint_cell = None
            
            self.draw_grid()
            
            # Provjera i prikaz pobjede
            if self.is_complete():
                font = pygame.font.Font(None, 74)
                text = font.render('Pobjeda!', True, GREEN)
                text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
                self.window.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = SudokuGameGUI()
    game.play()
