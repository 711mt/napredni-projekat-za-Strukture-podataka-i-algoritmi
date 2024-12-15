# Importujem potrebne biblioteke za rad sa matricama i za čišćenje ekrana u Google Colab okruženju
import numpy as np 
from IPython.display import clear_output  
class SudokuGame:
    def __init__(self):

        # Inicijalizacija početne Sudoku table ( gdje 0 predstavlja prazno polje)
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
        # Pravim kopiju početne table da bih znala koja polja ne smiju da se mijenjaju
        self.original = self.board.copy()

    def display(self):
        # Čisti prethodni prikaz
        clear_output(wait=True)
        # Ispisuje naslov igre
        print("\n SUDOKU IGRA")
        # Ispisuje brojeve kolona za lakšu orijentaciju
        print("   0 1 2   3 4 5   6 7 8")
        
        # Prolazi kroz svaki red table
        for i in range(9):
            # Ispisuje horizontalnu liniju na svaka 3 reda
            if i % 3 == 0:
                print("   " + "-" * 25)
            # Započinje red sa brojem reda i vertikalnom linijom
            row = f"{i} |"
            
            # Prolazi kroz svaku kolonu u redu
            for j in range(9):
                # Dodaje vertikalnu liniju na svake 3 kolone
                if j % 3 == 0 and j != 0:
                    row += "|"
                # Prikazuje prazno polje kao "_" ili broj ako postoji
                if self.board[i][j] == 0:
                    row += " _"
                else:
                    row += f" {self.board[i][j]}"
            # Završava red sa vertikalnom linijom
            print(row + " |")
            # Ispisuje donju horizontalnu liniju
            if i == 8:
                print("   " + "-" * 25)

    def is_valid_move(self, row, col, num):
        # Provjerava da li se broj već nalazi u istom redu ili koloni
        if num in self.board[row] or num in self.board[:, col]:
            return False
        
        # Određuje početne koordinate 3x3 kvadrata
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        # Provjerava da li se broj nalazi u 3x3 kvadratu
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True
#backtracking algoritam koji koristim u dvije svrhe za ovu igru
# 1. za provjeru da li je slagalica rješiva
# 2. i za generisanje prijedloga, tj. hints igraču

    def solve_with_backtracking(self, board):
        # Traži prvo prazno polje
        empty = self.find_empty(board)
        # Ako nema praznih polja, slagalica je riješena
        if not empty:
            return True
        
        row, col = empty
        # Pokušava da proba brojeve od 1 do 9
        for num in range(1, 10):
            # Ako je potez validan
            if self.is_valid_move(row, col, num):
                # Postavlja broj
                board[row, col] = num
                
                # Rekurzivno rješava ostatak table
                if self.solve_with_backtracking(board):
                    return True
                
                # Ako riješenje nije moguće, vraća polje na 0 (backtracking)
                board[row, col] = 0
        
        return False

    def find_empty(self, board):
        # Traži prvo prazno polje (označeno sa 0)
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    return (i, j)
        return None

    def get_hint(self):
        # Pravi kopiju trenutne table
        temp_board = self.board.copy()
        # Pokušava da riješi kopiju table
        if self.solve_with_backtracking(temp_board):
            # Traži prvo prazno polje i vraća riješenje za to polje
            for i in range(9):
                for j in range(9):
                    if self.board[i, j] == 0:
                        return (i, j, temp_board[i, j])
        return None

    def play(self):
        while True:
            # Prikazuje trenutno stanje table
            self.display()
            # Prikazuje dostupne komande zbog igrača, kako bi ovo bilo jednostavno
            print("\nKomande:")
            print("1. Unesite broj (format: red kolona broj)")
            print("2. Pomoć (unesite: pomoć)")
            print("3. Prijedlog (unesite: hint)")
            print("4. Izlaz (unesite: kraj)")
            
            # Čita unos korisnika
            choice = input("\nŠta želite da uradite? ").lower().strip()
            
            # Obrada različitih komandi
            if choice == 'kraj':
                print("Hvala na igri!")
                break
                
            elif choice == 'pomoć':
                # Prikazuje uputstva za igru igraču, radi lakšeg snalaženja za funkcionalnosti koje postoje
                print("\nKako igrati:")
                print("1. Unesite tri broja: red (0-8), kolona (0-8) i broj koji želite da stavite (1-9)")
                print("- Primjer kako to izgleda: '2 4 7' će staviti broj 7 u red 2, kolonu 4")
                print("2. Ne možete mijenjati početne brojeve")
                print("3. Koristite 'hint' za prijedlog sljedećeg poteza")
                input("\nPritisnite Enter za nastavak...")

            elif choice == 'hint':
                # Daje igraču prijedlog za sljedeći potez
                hint = self.get_hint()
                if hint:
                    print(f"\nPrijedlog: U red {hint[0]}, kolonu {hint[1]} ide broj {hint[2]}")
                    input("Pritisnite Enter za nastavak...")
                
            else:
                try:
                    row, col, num = map(int, choice.split())
                    # Provjeravamo da li su unijeti brojevi u dozvoljenom opsegu
                    if not (0 <= row <= 8 and 0 <= col <= 8 and 1 <= num <= 9):
                        print("Brojevi moraju biti: red (0-8), kolona (0-8), broj (1-9)")
                        continue
                    
                    # Provjerava da li je polje početno
                    if self.original[row][col] != 0:
                        print("Ne možete mijenjati početne brojeve!")
                        input("Pritisnite Enter za nastavak...")
                        continue
                    
                    # Provjerava validnost poteza i postavlja broj
                    if self.is_valid_move(row, col, num):
                        self.board[row][col] = num
                    else:
                        print("Nevažeći potez! Broj već postoji u redu, koloni ili kvadratu.")
                        input("Pritisnite Enter za nastavak...")
                    
                except ValueError:
                    print("Nevažeći unos! Koristite format: red kolona broj")
                    input("Pritisnite Enter za nastavak...")

# Pokretanje igre kada se skripta izvrši direktno
if __name__ == "__main__":
    game = SudokuGame()
    game.play()