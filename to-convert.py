this = False

def valid_squares(start, board):
  # establish helper variables
  squares = [start]
  # add left and right squares
  for direction in ('right', 'left'):
      square = shift_dir(start, direction)
      if square and (board[square] is None or board[square].get_color() != this.get_color()):
          squares.append(square)
  # if blue add up, if red add down
  square = shift_dir(start, 'up') if this.get_color() == 'blue' else shift_dir(start, 'down')
  if square and (board[square] is None or board[square].get_color() != this.get_color()):
      squares.append(square)
  # add palace-specific moves
  if start in ('d3', 'f3') and (board['e2'] is None or board['e2'].get_color() != this.get_color()):
      yield 'e2'
  if start in ('d8', 'f8') and (board['e9'] is None or board['e9'].get_color() != this.get_color()):
      yield 'e9'
  if start == 'e2':
      for square in ('d1', 'f1'):
          if board[square] is None or board[square].get_color() != this.get_color():
              squares.append(square)
  if start == 'e9':
      for square in ('d10', 'f10'):
          if board[square] is None or board[square].get_color() != this.get_color():
              squares.append(square)