import time
from window import Cell
import random

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.sleep = 0.1

        if seed is not None:
            random.seed(seed)

        self._create_cells()

        self._break_entrance_end_exit()

        self._break_walls_r(0,0)

        self._reset_cells_visited()

        self.solve()

    def _create_cells(self):
        self._cells=[]
        for i in range(self.num_cols):
            liste_col = []
            for j in range(self.num_rows):
                liste_col.append(Cell(self.win))
            self._cells.append(liste_col)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i,j)
                

    def _draw_cell(self, i, j):
        x1 = self.__x1 + self.cell_size_x * i
        x2 = self.__x1 + self.cell_size_x * (i+1)
        y1 = self.__y1 + self.cell_size_y * j
        y2 = self.__y1 + self.cell_size_y * (j+1)
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self, sleep=.002):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(sleep)

    def _break_entrance_end_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[- 1][- 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i < self.num_cols - 1 and self._cells[i + 1][j].visited == False:
                to_visit.append('droite')
            if i > 0 and self._cells[i - 1][j].visited == False:
                to_visit.append('gauche')
            if j < self.num_rows - 1 and self._cells[i][j + 1].visited == False:
                to_visit.append('bas')
            if j > 0 and self._cells[i][j - 1].visited == False:
                to_visit.append('haut')
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            choice = to_visit[random.randint(0, len(to_visit) -1)]

            if choice == 'gauche':
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
                self._draw_cell(i, j)
                self._draw_cell(i-1, j)
                self._break_walls_r(i-1, j)
            elif choice == 'droite':
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
                self._draw_cell(i, j)
                self._draw_cell(i+1, j)
                self._break_walls_r(i+1, j)
            elif choice == 'haut':
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
                self._draw_cell(i, j)
                self._draw_cell(i, j-1)
                self._break_walls_r(i, j-1)
            elif choice == 'bas':
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
                self._draw_cell(i, j)
                self._draw_cell(i, j+1)
                self._break_walls_r(i, j+1)

    def _reset_cells_visited(self):
        for liste in self._cells:
            for cell in liste:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate(0.1)
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        directions = []
        if i < self.num_cols - 1 and self._cells[i + 1][j].visited == False and self._cells[i][j].has_right_wall == False:
            directions.append('droite')
        if i > 0 and self._cells[i - 1][j].visited == False and self._cells[i][j].has_left_wall == False:
            directions.append('gauche')
        if j < self.num_rows - 1 and self._cells[i][j + 1].visited == False and self._cells[i][j].has_bottom_wall == False:
            directions.append('bas')
        if j > 0 and self._cells[i][j - 1].visited == False and self._cells[i][j].has_top_wall == False:
            directions.append('haut')
        return self._follow_direction(directions, i, j)


    def _follow_direction(self, directions, i, j):
        while len(directions) > 0:
            random.shuffle(directions)
            choice = directions.pop()
            if choice == 'gauche':
                self._cells[i][j].draw_move(self._cells[i-1][j])
                recurs = self._solve_r(i-1, j)
                if recurs:
                    return recurs
                self._cells[i][j].draw_move(self._cells[i-1][j], undo=True)
                self._animate(0.1)
                

            elif choice == 'droite':
                self._cells[i][j].draw_move(self._cells[i+1][j])
                recurs = self._solve_r(i+1, j)
                if recurs:
                    return recurs
                self._cells[i][j].draw_move(self._cells[i+1][j], undo=True)
                self._animate(0.1)
                
            elif choice == 'haut':
                self._cells[i][j].draw_move(self._cells[i][j - 1])
                recurs = self._solve_r(i, j-1)
                if recurs:
                    return recurs
                self._cells[i][j].draw_move(self._cells[i][j-1], undo=True)
                self._animate(0.1)

            elif choice == 'bas':
                self._cells[i][j].draw_move(self._cells[i][j + 1])
                recurs = self._solve_r(i, j+1)
                if recurs:
                    return recurs
                self._cells[i][j].draw_move(self._cells[i][j+1], undo=True)
                self._animate(0.1)

        return False