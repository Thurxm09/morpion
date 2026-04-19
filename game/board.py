"""Modelisation du plateau de jeu pour un morpion de taille variable.

Le plateau est represente par une matrice NumPy d'entiers:
- `0` pour une case vide
- `1` pour le joueur 1
- `-1` pour le joueur 2
"""

import numpy as np


class Board:
    """Encapsule l'etat du plateau et les regles de victoire associees."""

    def __init__(self, size=3):
        """Initialise un plateau carre vide.

        Args:
            size (int, optional): Taille du plateau (nombre de lignes/colonnes).
                La valeur par defaut est 3.
        """
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)

    def place_mark(self, ligne, col, joueur):
        """Place le pion d'un joueur sur une case libre.

        Args:
            ligne (int): Indice de ligne cible.
            col (int): Indice de colonne cible.
            joueur (int): Identifiant du joueur (`1` ou `-1`).

        Returns:
            bool: `True` si le pion a ete place, `False` si la case etait occupee.
        """
        if self.grid[ligne][col] == 0:
            self.grid[ligne][col] = joueur
            return True
        return False

    def get_available_moves(self):
        """Retourne la liste des cases encore jouables.

        Returns:
            list[tuple[int, int]]: Coordonnees `(ligne, colonne)` des cases vides.
        """
        return [(int(r), int(c)) for r, c in np.argwhere(self.grid == 0)]

    def is_full(self):
        """Indique si le plateau est completement rempli.

        Returns:
            bool: `True` si aucune case n'est vide, sinon `False`.
        """
        return not np.any(self.grid == 0)

    def check_winner(self):
        """Detecte un gagnant et retourne ses cases gagnantes.

        La methode verifie les lignes, colonnes et diagonales pour chacun des
        joueurs (`1` puis `-1`).

        Returns:
            tuple[int | None, list[tuple[int, int]]]:
                - Le joueur gagnant (`1` ou `-1`) ou `None` s'il n'y en a pas.
                - La liste des coordonnees des cases formant la combinaison
                  gagnante, ou une liste vide.
        """
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

    def is_game_over(self):
        """Determine si la partie est terminee.

        Une partie est consideree terminee si un joueur a gagne ou si le
        plateau est plein.

        Returns:
            bool: `True` si la partie est terminee, sinon `False`.
        """
        winner, _ = self.check_winner()
        return winner is not None or self.is_full()
