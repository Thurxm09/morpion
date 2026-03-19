import numpy as np 

class Board:
    def __init__(self, size = 3):
        self.size = size
        self.grid = np.zeros((size, size), dtype = int)
        
    def place_mark(self, ligne, col, joueur):
        if self.grid[ligne][col] == 0:
            self.grid[ligne][col] = joueur
            return True
        return False

    def get_available_moves(self): 
        return [(int(r), int(c)) for r, c in np.argwhere(self.grid == 0)]
    
    def is_full(self): 
        return not np.any(self.grid == 0)
    
    def check_winner(self): 
        # ── Lignes ──────────────────────────────────────
        row_sums = np.sum(self.grid, axis=1)
        col_sums = np.sum(self.grid, axis=0)
        diag_sums = np.trace(self.grid)
        antidiag_sums = np.trace(np.fliplr(self.grid))
        
        # Vérification pour chaque joueur (1 et -1)
        for joueur in [1, -1]:
            # La somme cible correspond à size * joueur (ex: 3 ou -3 pour une grille 3x3)
            target = self.size * joueur
            
            # ── Vérification des lignes ──
            lignes_gagnantes = np.where(row_sums == target)[0]
            if len(lignes_gagnantes) > 0:
                ligne_idx = lignes_gagnantes[0]
                cases_gagnantes = [(ligne_idx, col) for col in range(self.size)]
                return (joueur, cases_gagnantes)
            
            # ── Vérification des colonnes ──
            cols_gagnantes = np.where(col_sums == target)[0]
            if len(cols_gagnantes) > 0:
                col_idx = cols_gagnantes[0]
                cases_gagnantes = [(ligne, col_idx) for ligne in range(self.size)]
                return (joueur, cases_gagnantes)
            
            # ── Vérification de la diagonale principale ──
            if diag_sums == target:
                cases_gagnantes = [(i, i) for i in range(self.size)]
                return (joueur, cases_gagnantes)
            
            # ── Vérification de la diagonale secondaire ──
            if antidiag_sums == target:
                cases_gagnantes = [(i, self.size - 1 - i) for i in range(self.size)]
                return (joueur, cases_gagnantes)

        return (None, [])
    
