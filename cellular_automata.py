#!/usr/bin/env python3

"""
cellular_automata.py - Takes user inputs from a gui and uses those inputs to create unique patterns.
"""

import pygame
import random
from datetime import datetime
from tkinter import *
from tkinter.ttk import *


def divide(a, b):
    if a//b < a/b:
        return a//b + 1
    return a//b


def create_gui():
    for item in label_names:
        index = label_names.index(item)
        var = all_vars[index]
        label = Label(master, text='{}:'.format(item), width=25)
        if item in label_options.keys():
            entry = Combobox(master, textvariable=var, values=label_options[item])
        else:
            entry = Entry(master, width=25, textvariable=var)
        label.grid(row=index, sticky=W, pady=5, padx=5)
        entry.grid(row=index, column=1, sticky=N+S+E+W, pady=5, padx=5)


def fetch(ents):
    try:
        all_vars_get = rule, num_of_rows, num_of_cols, f_row, picture = [var.get() for var in ents]
        if 0 <= rule <= 255:
            if num_of_cols >= 3 and num_of_rows > 0:
                if f_row in first_row_options or set(f_row) == {'0', '1'}:
                    return all_vars_get
    except Exception as e:
        print('Error: {}'.format(e))


def first_row(f_row, num_of_cols):
        row = f_row.capitalize()
        if row in first_row_options or set(row) == {'0', '1'}:
            row_len = num_of_cols
            if row == 'Default':
                row = '{}1{}'.format('0'*((row_len-1)//2), '0'*divide(row_len-1, 2))
            elif row == 'Zeros':
                row = '0' * row_len
            elif row == 'Ones':
                row = '1' * row_len
            elif row == 'Random':
                row = ''.join([str(random.randint(0, 1)) for i in range(row_len)])
            return row
        elif set(row) == {'0', '1'}:
            return row


def all_rows(f_row, num_of_rows, num_of_cols, outputs):
    row = first_row(f_row, num_of_cols)
    rows = [row]
    for j in range(num_of_rows-1):
        input_row = '{}{}{}'.format(row[-1], row, row[0])
        row = ''.join([outputs[inputs.index(input_row[i:i+3])] for i in range(len(input_row)-2)])
        rows.append(row)
    return rows


def main(ents):
    try:
        rule, num_of_rows, num_of_cols, f_row, picture = fetch(ents)
    except TypeError:
        return
    outputs = '{0:08b}'.format(rule)
    input_rows = all_rows(f_row, num_of_rows, num_of_cols, outputs)

    pygame.init()

    base_width = base_height = 600
    window_width = int(base_width * min(len(input_rows[0])/num_of_rows, 1))
    window_height = int(base_height * min(1, num_of_rows/len(input_rows[0])))
    window_surface = pygame.display.set_mode((window_width, window_height), 0, 32)
    pygame.display.set_caption('Cellular Automata - Rule {}'.format(rule))
    window_surface.fill(GRAY)

    rect_pos_x, rect_pos_y = 0.5, 0.5
    rect_width = (window_width - rect_pos_x)/len(input_rows[0]) - rect_pos_x
    rect_height = (window_height - rect_pos_y)/num_of_rows - rect_pos_y

    y = rect_pos_y
    for item in input_rows:
        x = rect_pos_x
        for char in item:
            output = int(char)
            rect = pygame.Rect(x, y, rect_width, rect_height)
            pygame.draw.rect(window_surface, cell_states[output], rect)
            x += rect_width + rect_pos_x
        y += rect_height + rect_pos_y

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if picture:
                    rule_str = str(rule).rjust(2, '0')
                    file_name = 'rule{}_{}.jpeg'.format(rule_str, datetime.now().strftime('%Y%m%d%H%M%S'))
                    pygame.image.save(window_surface, file_name)
                pygame.quit()
                return

if __name__ == '__main__':
    inputs = ['111', '110', '101', '100', '011', '010', '001', '000']
    error_msg = 'Invalid input. Try again.'

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    cell_states = {0: WHITE, 1: BLACK}

    # TKINTER OPTIONS
    first_row_options = ['Default', 'Random', 'Zeros', 'Ones']
    label_names = ['Rule', 'Number of rows', 'Number of columns', 'First row']
    label_options = {'Rule': list(range(256)), 'First row': first_row_options + ['Other (type 0s and 1s)']}

    master = Tk()
    master.wm_title('Options')
    master.columnconfigure(1, weight=1)

    rule_var = IntVar()
    row_len_var = IntVar()
    col_len_var = IntVar()
    first_row_var = StringVar()
    check_var = IntVar()

    rule_var.set(random.randint(0, 255))
    row_len_var.set(51)
    col_len_var.set(101)
    first_row_var.set(first_row_options[0])
    check_var.set(0)

    all_vars = [rule_var, row_len_var, col_len_var, first_row_var, check_var]

    create_gui()

    b1 = Checkbutton(master, text='Save screen shot', variable=check_var, onvalue=1, offvalue=0)
    b2 = Button(master, text='Go!', command=(lambda e=all_vars: main(e)))
    b3 = Button(master, text='Quit', command=master.quit)
    b1.grid(row=4, column=0, sticky=W, pady=5, padx=5, columnspan=2)
    b2.grid(row=5, column=0, sticky=W, pady=5, padx=5)
    b3.grid(row=5, column=1, sticky=W, pady=5, padx=5)

    master.mainloop()
