#!/usr/bin/env python

__author__ = "Dastan"

# Minesweeper in Python using Tkinter.



from tkinter import *
import random

GRID_SIZE = 20 #  Field size
SQUARE_SIZE = 20 # Cell size
MINES_NUM = 40 # Number of mines on the field
mines = set(random.sample(range(1, GRID_SIZE**2+1), MINES_NUM)) # We randomly place mines on the field
clicked = set() # A set that holds all the cells we clicked on


def check_mines(neighbors):
    """ A function that returns the number of mines around neighbors """
    return len(mines.intersection(neighbors))


def generate_neighbors(square):
    """ Returns the cells adjacent to square """
    # Left top cell
    if square == 1:
        data = {GRID_SIZE + 1, 2, GRID_SIZE + 2}
    # Right lower
    elif square == GRID_SIZE ** 2:
        data = {square - GRID_SIZE, square - 1, square - GRID_SIZE - 1}
    # Left lower
    elif square == GRID_SIZE:
        data = {GRID_SIZE - 1, GRID_SIZE * 2, GRID_SIZE * 2 - 1}
    # Upper right
    elif square == GRID_SIZE ** 2 - GRID_SIZE + 1:
        data = {square + 1, square - GRID_SIZE, square - GRID_SIZE + 1}
    # Cell in the left row
    elif square < GRID_SIZE:
        data = {square + 1, square - 1, square + GRID_SIZE,
                square + GRID_SIZE - 1, square + GRID_SIZE + 1}
    # Cell in the right row
    elif square > GRID_SIZE ** 2 - GRID_SIZE:
        data = {square + 1, square - 1, square - GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1}
    # Cell in the bottom row
    elif square % GRID_SIZE == 0:
        data = {square + GRID_SIZE, square - GRID_SIZE, square - 1,
                square + GRID_SIZE - 1, square - GRID_SIZE - 1}
    # Cell in the upper row
    elif square % GRID_SIZE == 1:
        data = {square + GRID_SIZE, square - GRID_SIZE, square + 1,
                square + GRID_SIZE + 1, square - GRID_SIZE + 1}
    # Any other cell
    else:
        data = {square - 1, square + 1, square - GRID_SIZE, square + GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1,
                square + GRID_SIZE + 1, square + GRID_SIZE - 1}
    return data


def clearance(ids):
    """ Iterative (efficient) field clearing function """
    clicked.add(ids) # add the clicked cell to the set of clicked
    ids_neigh = generate_neighbors(ids) # Get all neighboring cells
    around = check_mines(ids_neigh)
    c.itemconfig(ids, fill="green")


    if around == 0:

        neigh_list = list(ids_neigh)

        while len(neigh_list) > 0:

            item = neigh_list.pop()

            c.itemconfig(item, fill="green")

            item_neigh = generate_neighbors(item)

            item_around = check_mines(item_neigh)

            if item_around > 0:

                if item not in clicked:

                    x1, y1, x2, y2 = c.coords(item)

                    c.create_text(x1 + SQUARE_SIZE / 2,
                                  y1 + SQUARE_SIZE / 2,
                                  text=str(item_around),
                                  font="Arial {}".format(int(SQUARE_SIZE / 2)),
                                  fill='yellow')

            else:

                neigh_list.extend(set(item_neigh).difference(clicked))

                neigh_list = list(set(neigh_list))

            clicked.add(item)

    else:

        x1, y1, x2, y2 = c.coords(ids)

        c.create_text(x1 + SQUARE_SIZE / 2,
                      y1 + SQUARE_SIZE / 2,
                      text=str(around),
                      font="Arial {}".format(int(SQUARE_SIZE / 2)),
                      fill='yellow')


def rec_clearance(ids):

    clicked.add(ids)
    neighbors = generate_neighbors(ids)
    around = check_mines(neighbors)
    if around:
        x1, y1, x2, y2 = c.coords(ids)
        c.itemconfig(ids, fill="green")
        c.create_text(x1 + SQUARE_SIZE / 2,
                      y1 + SQUARE_SIZE / 2,
                      text=str(around),
                      font="Arial {}".format(int(SQUARE_SIZE / 2)),
                      fill='yellow')
    else:
        for item in set(neighbors).difference(clicked):
            c.itemconfig(item, fill="green")
            rec_clearance(item)


def click(event):
    ids = c.find_withtag(CURRENT)[0]
    if ids in mines:
        c.itemconfig(CURRENT, fill="red")
    elif ids not in clicked:
        clearance(ids)
        c.itemconfig(CURRENT, fill="green")
    c.update()


def mark_mine(event):
    ids = c.find_withtag(CURRENT)[0]
    if ids not in clicked:
        clicked.add(ids)
        x1, y1, x2, y2 = c.coords(ids)
        c.itemconfig(CURRENT, fill="yellow")
    else:
        clicked.remove(ids)
        c.itemconfig(CURRENT, fill="gray")


root = Tk()
root.title("Minesweeper")
c = Canvas(root, width=GRID_SIZE * SQUARE_SIZE, height=GRID_SIZE * SQUARE_SIZE)
c.bind("<Button-1>", click)
c.bind("<Button-3>", mark_mine)
c.pack()
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
      c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                         i * SQUARE_SIZE + SQUARE_SIZE,
                         j * SQUARE_SIZE + SQUARE_SIZE, fill='gray')
root.mainloop()