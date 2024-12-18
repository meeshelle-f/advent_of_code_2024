# -*- coding: utf-8 -*-
"""Advent Challenge D6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lvQ4d_LemQqZLwTSWYJoQC2gxtwtJIK3

#Day 6 Part 1
inputs = d6_input.txt

--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:
"""

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

"""The map shows the current position of the **guard** with **^** (to indicate the guard is currently facing up from the perspective of the map). Any **obstructions** - crates, desks, alchemical reactors, etc. - are shown as **#**.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):
"""

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

"""Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:"""

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

"""Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:"""

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

"""This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):"""

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

"""By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:"""

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

"""In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
"""

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/MyDrive/Advent 2024/day6/d6_input.txt'

import numpy as np
import pandas as pd

"""##example data"""

data_str = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

data_lists = [list(x) for x in data_str.split('\n')]

num_rows = len(data_lists)
num_cols = len(data_lists[0])

print("Number of rows:", num_rows)
print("Number of columns:", num_cols)

"""identify the guard and obstacles"""

guard_keys = {'^':'up', 'v':'down', '<':'left','>':'right'}
row = 0
obstacles= []
for data_list in data_lists:
  row +=1
  for key in guard_keys:
    if key in data_list:
      print(f"guard {key} found at row, col", row, data_list.index(key))
      guard = (row, data_list.index(key))
      direction = guard_keys[key]
  if '#' in data_list:
    obstacles.append((row, data_list.index('#')))


row, len(data_list), guard, direction, obstacles
max_row = num_rows #10
max_col = num_cols - 1 #10 to 9 since index is 0-9.

def guard_path(guard, direction, obstacles):
  row, index = guard
  track_positions = [guard]
  # print('obstacles', obstacles)

  while True:

    if row == max_row and direction == 'down' or row == 1 and direction == 'up' or index == 0 and direction == 'left' or index == max_col and direction == 'right':
      print('BREAK', row, index, direction)
      break


    elif direction == 'up': # add 1+ y until obstacle is hit
      row -= 1
    elif direction == 'right':
      index += 1
    elif direction == 'down':
      row +=1
    elif direction == 'left':
      index = index - 1

    new_position = (row, index)

    if 1 <= row <= max_row and 0 <= index <= max_col and new_position not in obstacles:
      track_positions.append(new_position)
      print(new_position)


    else:
      # Reached an obstacle or boundary, change direction
      if direction == 'up':
          row+=1
          print(row,index, direction)
          direction = 'right'
      elif direction == 'right':
          index-=1
          print(row,index, direction)
          direction = 'down'
      elif direction == 'down':
          row-=1
          print(row,index, direction)
          direction = 'left'

      elif direction == 'left':
          index= index + 1
          print(row,index, direction)
          direction = 'up'


      # If new direction leads to obstacle or boundary, stop
      if (direction == 'up' and row == 1) or \
          (direction == 'right' and index == max_col) or \
          (direction == 'down' and row == max_row) or \
          (direction == 'left' and index == 0):
          break

  return track_positions

track_positions = guard_path(guard, direction, obstacles)
print(len(set(track_positions))) #41

"""##part 1 real"""

guard_keys = {'^':'up', 'v':'down', '<':'left','>':'right'}
row = 0
obstacles= []
lines = []
for line in open(file_path):
    line = line.strip()
    lines.append(line)

    row +=1
    print(row, line)

    for key in guard_keys:
      if key in line:
        print(f"guard {key} found at row, col", row, line.index(key))
        guard = (row, line.index(key))
        direction = guard_keys[key]
    if '#' in line:
      hash_indices = [i for i, char in enumerate(line) if char == '#']
      print(hash_indices)
      for hash in hash_indices: #incorrectly assumed we only had 1 hash per line. Count and store them all!
        obstacles.append((row, hash))

row, len(line), guard, direction #, obstacles

num_rows = len(lines)
num_cols = len(lines[0])

row, len(lines), guard, direction #(130, 10, (7, 4), 'up')
# obstacles

max_row = num_rows
max_index = num_cols -1

def guard_path(guard, direction, obstacles):
  row, index = guard
  track_positions = [guard]
  # print('obstacles', obstacles)

  while True:
    print(row, index, direction)
    if row == max_row and direction == 'down' or row == 1 and direction == 'up' or index == 0 and direction == 'left' or index == max_index and direction == 'right':
      print('BREAK', row, index, direction)
      break


    elif direction == 'up': # add 1+ y until obstacle is hit
      row -= 1
    elif direction == 'right':
      index += 1
    elif direction == 'down':
      row +=1
    elif direction == 'left':
      index = index - 1

    new_position = (row, index)

    if 1 <= row <= max_row and 0 <= index <= max_index and new_position not in obstacles:
      track_positions.append(new_position)


    else:
      # Reached an obstacle or boundary, change direction
      if direction == 'up':
          row+=1
          print(row,index, direction)
          direction = 'right'
      elif direction == 'right':
          index-=1
          print(row,index, direction)
          direction = 'down'
      elif direction == 'down':
          row-=1
          print(row,index, direction)
          direction = 'left'

      elif direction == 'left':
          index= index + 1
          print(row,index, direction)
          direction = 'up'


      # If new direction leads to obstacle or boundary, stop
      if (direction == 'up' and row == 1) or \
          (direction == 'right' and index == max_index) or \
          (direction == 'down' and row == max_row) or \
          (direction == 'left' and index == 0):
          break

  return track_positions

track_positions = guard_path(guard, direction, obstacles)
print(len(set(track_positions)))  # 4988

"""##part 2 info

While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use **O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.**

Option one, put a printing press next to the guard's starting position:
"""

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...

"""Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:



"""

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...

"""Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:


"""

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...

"""Option four, put an alchemical retroencabulator near the bottom left corner:


"""

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...

"""Option five, put the alchemical retroencabulator a bit to the right instead:


"""

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...

"""Option six, put a tank of sovereign glue right next to the tank of universal solvent:


"""

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..

"""##part 2 example

It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

**You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?**
"""

def guard_path_loop(guard, direction, obstacles):
  row, index = guard
  track_positions = [guard]
  # print('obstacles', obstacles)
  track_positions_count = {}
  track_positions_dict = {}
  while True:

    print(row, index, direction)
    if row == max_row and direction == 'down' or row == 1 and direction == 'up' or index == 0 and direction == 'left' or index == max_index and direction == 'right': #if escapes
      print('BREAK', row, index, direction)
      break
    #ADD IN
    if sum(value > 3 for value in track_positions_count.values()) >= 4: #AKA 4 keys (positions/coordinates) have been tracked at least 3 times, then we are in a loop.
      print('BREAK in continuous loop', row, index, direction)
      track_positions = []
      break
    elif direction == 'up': # add 1+ y until obstacle is hit
      row -= 1
    elif direction == 'right':
      index += 1
    elif direction == 'down':
      row +=1
    elif direction == 'left':
      index = index - 1

    new_position = (row, index)

    if 1 <= row <= max_row and 0 <= index <= max_index and new_position not in obstacles:
      track_positions.append(new_position)
      track_positions_dict[new_position]=direction
      if new_position not in track_positions_count.keys():
        track_positions_count[new_position] = 1
      else:
        track_positions_count[new_position] += 1


    else:
      # Reached an obstacle or boundary, change direction
      if direction == 'up':
          row+=1
          print(row,index, direction)
          direction = 'right'
      elif direction == 'right':
          index-=1
          print(row,index, direction)
          direction = 'down'
      elif direction == 'down':
          row-=1
          print(row,index, direction)
          direction = 'left'

      elif direction == 'left':
          index= index + 1
          print(row,index, direction)
          direction = 'up'


      # If new direction leads to obstacle or boundary, stop
      if (direction == 'up' and row == 1) or \
          (direction == 'right' and index == max_index) or \
          (direction == 'down' and row == max_row) or \
          (direction == 'left' and index == 0):
          break

  return track_positions, track_positions_dict

data_str = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

data_lists = [x for x in data_str.split('\n')]

guard_keys = {'^':'up', 'v':'down', '<':'left','>':'right'}
row = 0
obstacles= []
new_obstructions = [] #potential spots to add obstructions.

for data_list in data_lists:
  row +=1
  x, y, z = 0, 0, 0
  for key in guard_keys:
    if key in data_list:
      print(f"guard {key} found at row, col", row, data_list.index(key))
      guard = (row, data_list.index(key))
      direction = guard_keys[key]
      x = 1

  if '#' in data_list:
    hash_indices = [i for i, char in enumerate(data_list) if char == '#']
    # print(hash_indices)
    for hash in hash_indices: #incorrectly assumed we only had 1 hash per line. Count and store them all!
      obstacles.append((row, hash))
    y = len(hash_indices)

  if '.' in data_list:
    period_indices = [i for i, char in enumerate(data_list) if char == '.']
    for period in period_indices:
      new_obstructions.append((row, period))
    z = len(period_indices)

  print(row, x+y+z)

row, len(data_list), guard, direction
# obstacles

num_rows = len(data_lists)
num_cols = len(data_lists[0])

print("Number of rows:", num_rows)
print("Number of columns:", num_cols)

max_row = num_rows #10
max_col = num_cols - 1 #10 to 9 since index is 0-9.

passing_obstruction = []

for new_obstruction in new_obstructions:
  print(new_obstruction)
  test_obstruction = obstacles.copy()
  test_obstruction.append(new_obstruction)
  track_positions,track_positions_dict = guard_path_loop(guard, direction, test_obstruction)
  print(track_positions)
  if len(track_positions) == 0:
    print('passed!', new_obstruction)
    passing_obstruction.append(new_obstruction)

print(len(set(passing_obstruction))) #6

"""##Part 2 real

##Update previous code

create **guard_path_loop()** do not track where the guard has been but only if the guard moves more than the max number of moves  = (num_rows*num_cols)-num_blocks.
"""

warehouse = []
infinite_count = 0
# Read the file and put into array of strings

with open(file_path, 'r') as file:
    for line in file:
        warehouse.append(line[:-1])

def get_guard_location():
    for i, row in enumerate(warehouse):
        for j, col in enumerate(row):
            if col == '^':
                return (i, j)

def get_obstacles():
  obstacles = []
  for i, row in enumerate(warehouse):
      for j, col in enumerate(row):
          if col == '#':
            obstacles.append((i, j))
  return obstacles

max_moves = (130*130) - len(obstacles)

def guard_path_loop(guard, direction):

  dict_direction = {'up':'right', 'right':'down', 'down':'left', 'left':'up'}
  boundaries = [0, len(warehouse)-1]
  row, index = guard
  num_spots = 0

  while row not in boundaries and index not in boundaries:

    prev_position = (row, index)

    #move the guard
    if direction == 'up': # add 1+ y until obstacle is hit
      row -= 1
    elif direction == 'right':
      index += 1
    elif direction == 'down':
      row +=1
    elif direction == 'left':
      index = index - 1

    new_position = (row, index)

    if num_spots >= max_moves:
      return False

    elif warehouse[row][index] == '#':
    # elif new_position in obstacles:
      row, index = prev_position #revert back to previous position
      direction = dict_direction[direction] #change direction - rotate_clockwise

    else:
      num_spots += 1

  print(num_spots)
  return True

obstacles = get_obstacles()
guard =  get_guard_location()
guard_path_loop(guard, 'up') #4988 ...

def create_blockades():
  inf_loop = 0
  for i, row in enumerate(warehouse):
    row_list = list(row)  # Convert the string to a list of characters

    for j, col in enumerate(row):
      coord = (i,j)
      if warehouse[i][j] == '.':
        row_list[j] = '#'  # Modify the character in the list
        warehouse[i] = ''.join(row_list)  # Convert the modified list back to a string

        if not guard_path_loop(guard, 'up'): #AKA is infinite loop.. 4988 ...
          inf_loop+=1
        #convert back
        row_list[j] = '.'  # Modify the character in the list
        warehouse[i] = ''.join(row_list)  # Convert the modified list back to a string

  print(i, inf_loop)
create_blockades() #1697