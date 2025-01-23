from window import Window, Point, Line, Cell
from maze import Maze


def main():
    win = Window(800,600)

    maze = Maze(50, 50, 10, 14, 50, 50, win)

    maze.solve()

    win.wait_for_close()

    return
    


main()