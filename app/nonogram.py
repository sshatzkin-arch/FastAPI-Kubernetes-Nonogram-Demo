import numpy as np

colors = {0:"W", 1:"B"}
class Nonogram:
  # Init method
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols

    self.clues, self.solution = self.random_puzzle(rows, cols)

  # Generates the clues for a randomized nonogram puzzle
  def random_puzzle(self, rows, cols):
    
    percent_ones = 0.5  #Probability that a square will become a 1 

    grid = np.random.rand(rows, cols)

    with np.nditer(grid, op_flags=['readwrite']) as it:
      for cell in it:
        if (cell < percent_ones):
          cell[...] = 1
        else:
          cell[...] = 0
    
    clues = self.generate_clues(grid)

    return clues, grid

  # Takes a 2D array of 0s and 1s (nonogram puzzle), and returns the clues
  def generate_clues(self, grid):
    w, h = grid.shape
    row_clues = [[0 for x in range(1)] for y in range(w)] 
    col_clues = [[0 for x in range(1)] for y in range(h)] 

    # Actives arrays hold values to indicate if we're on a streak in this row/col or not
    row_actives = [0 for x in range(w)]
    row_curr = [0 for x in range(w)]
    col_actives = [0 for x in range(h)]
    col_curr = [0 for x in range(h)]

    # Iterate over all the values in the grid
    with np.nditer(grid, flags=['multi_index'], op_flags=['writeonly']) as it:
      for x in it:
        i, j = it.multi_index
        
        # If value x is a 1
        if (x == 1):

          # If currently on a vertical streak -> stay active / increment
          if (row_actives[i] == 1):
            row_clues[i][row_curr[i]] += 1 # Add 1 to current streak length

          # If not currently on a vertical streak -> activate streak / increment
          else:
            row_actives[i] = 1 # Activate a streak
            row_curr[i] += 1
            row_clues[i].append(1)
          
          # If currently on a horizontal streak -> stay active / increment
          if (col_actives[j] == 1):
            col_clues[j][col_curr[j]] += 1 # Add 1 to current streak length

          # If not currently on a horizontal streak -> activate streak / increment
          else:
            col_actives[j] = 1 # Activate a streak
            col_curr[j] += 1
            col_clues[j].append(1)

        # If value x is a 0
        else:
          # If currently on a vertical streak -> disable streak
          if (row_actives[i] == 1):
            row_actives[i] = 0
          
          # If currently on a horizontal streak -> disable streak
          if (col_actives[j] == 1):
            col_actives[j] = 0
          
    for i in range(w):
      row_clues[i] = row_clues[i][1:]

    for i in range(h):
      col_clues[i] = col_clues[i][1:]
    
    clues = {"row_clues": row_clues, "col_clues": col_clues}

    return clues
  

  def encode(self, name):
    encoded = {"name": name, "width": self.cols, "height": self.rows}
    solution = solution_to_string(self.solution)
    encoded["solution"] = solution
    encoded["col_hints"] = hints_to_string(self.clues["col_clues"])
    encoded["row_hints"] = hints_to_string(self.clues["row_clues"])
    return encoded




def solution_to_string(grid):
  curr_color = grid[0][0]
  run_length = 0
  encoded_string = ""

  for row in grid:
    for val in row:
      if (val == curr_color): # Continue Streak
        run_length += 1
      else:
        encoded_string = encoded_string + str(run_length) + colors[curr_color]
        curr_color = val
        run_length = 1
  encoded_string = encoded_string + str(run_length) + colors[curr_color]
  return encoded_string

def hints_to_string(hints):
  encoded_string = ""
  for row in hints:
    for hint in row:
      if row == []:
        encoded_string = encoded_string + ","
      else:  
        encoded_string = encoded_string + str(hint) + ","
    encoded_string = encoded_string[:-1] + "|"
  return encoded_string[:-1]