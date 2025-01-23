from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="black")
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color, width=2)

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        line = Line(Point(x1, y1), Point(x1, y2))
        if self.has_left_wall:
            self._win.draw_line(line, 'white')
        else: 
            self._win.draw_line(line, 'black')

        line = Line(Point(x1, y1), Point(x2, y1))
        if self.has_top_wall: 
            self._win.draw_line(line, 'white')
        else:
            self._win.draw_line(line, 'black')

        line = Line(Point(x2, y1), Point(x2, y2))   
        if self.has_right_wall:
            self._win.draw_line(line, 'white')
        else:
            self._win.draw_line(line, 'black')

        line = Line(Point(x1, y2), Point(x2, y2))
        if self.has_bottom_wall:
            self._win.draw_line(line, 'white')
        else:
            self._win.draw_line(line, 'black')


    def draw_move(self, to_cell, undo=False):
        p1 = Point(int((self._x1 + self._x2) / 2), int((self._y1 + self._y2) / 2))
        p2 = Point(int((to_cell._x1 + to_cell._x2) / 2), int((to_cell._y1 + to_cell._y2) / 2))
        if undo:
            self._win.draw_line(Line(p1, p2), 'blue')
        else:
            self._win.draw_line(Line(p1, p2), 'red')
