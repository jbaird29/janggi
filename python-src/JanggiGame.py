# Author: Jon Baird
# Date: 02/22/2021
# Description: A program for playing the board game Janggi (Korean chess)


class JanggiBoard:
    """
    Represents the board within the game Janggi (Korean chess);
    Its main purpose is containing a representation of the board (which pieces are where on the board)
    This board will contain each of the individual PieceType Objects (using composition)
    This class also contains helpful additional information, such as the squares of the palace, as well as
      a helper method to print a representation of the board to the console window
    This class will be contained within a JanggiGame class object
    """
    def __init__(self, board=None):
        """
        Initializes a JanggiBoard object
        :param board: implemented as dictionary of key: algebraic notation, value: None if empty, PieceObject if piece
            if None is passed in as the argument, then the board is initialized with all empty squares
        :palace: a tuple of the various squares that are located in either blue or red palace
        """
        self._palace = ('d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3',
                        'd8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10')
        self._red_palace = ('d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3')
        self._blue_palace = ('d8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10')
        self._palace_corners = ('d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10')
        self._red_palace_corners = ('d1', 'f1', 'd3', 'f3')
        self._blue_palace_corners = ('d8', 'f8', 'd10', 'f10')
        if board is None:
            self._board = self.empty()
        else:
            self._board = board

    @staticmethod
    def empty():
        """Initializes a board where all the squares are empty (None); used as helper for debugging"""
        empty_board = {}
        for letter, i in [(chr(letter_ord), i) for letter_ord in (range(97, 106)) for i in range(1, 11)]:
            square = letter + str(i)
            empty_board[square] = None
        return empty_board

    def get_board(self):
        """Returns the board, implemented as a dictionary"""
        return self._board

    def get_palace(self, color=None):
        """Given a color, returns a tuple of all palace squares for that color; if None returns all palace squares"""
        assert color in ('red', 'blue', None), 'Invalid color'
        if color == 'red':
            return self._red_palace
        if color == 'blue':
            return self._blue_palace
        if color is None:
            return self._palace

    def get_palace_corners(self, color=None):
        """Given a color, returns a tuple of all palace corners for that color; if None returns all corners"""
        assert color in ('red', 'blue', None), 'Invalid color'
        if color == 'red':
            return self._red_palace_corners
        if color == 'blue':
            return self._blue_palace_corners
        if color is None:
            return self._palace_corners

    def get_palace_centers(self, color=None):
        """Given a color, returns the palace center for that color; if None, returns a tuple of both corners"""
        assert color in ('red', 'blue', None), 'Invalid color'
        if color == 'red':
            return 'e2'
        if color == 'blue':
            return 'e9'
        if color is None:
            return 'e2', 'e9'

    def get_general_square(self, color):
        """Given a color, gets the square of that color's general; return as string in algebraic notation"""
        for square in self.get_palace(color):
            if self._board[square] is not None and isinstance(self._board[square], General):
                return square
        # if General not found, raise an error
        no_general = True
        assert no_general, 'No general found'

    def is_in_check(self, color):
        """
        Given a color, returns True if the color is in check based on the current board; otherwise False
        :param color: the color of the player to determine if they're in-check; either 'red' or 'blue'
        :return: True or False
        """
        general_square = self.get_general_square(color)
        opposing_color = 'red' if color == 'blue' else 'blue'
        # iterate through the board; see if any opposing color’s pieces could validly capture the given color's general
        for (square, piece) in self._board.items():
            if piece is not None and piece.get_color() == opposing_color:
                can_capture_general = general_square in piece.valid_squares(square, self)
                if can_capture_general:
                    return True
        # if loop had ended with no True condition, return False
        return False

    def is_in_checkmate(self, color):
        """
        Given a color, returns True if the color is in checkmate based on the current board; otherwise False
        :param color: the color of the player to determine if they're in-checkmate; either 'red' or 'blue'
        :return: True or False
        """
        # first get the given color's general and see if the general can move to get out of check
        general_square = self.get_general_square(color)
        general = self._board[general_square]
        # get a list of the color's pieces / square locations
        options = [(square, piece) for (square, piece) in self._board.items()
                   if piece is not None and piece.get_color() == color and piece is not general]
        # insert the general piece (in order to check that first - for performance benefits
        options.insert(0, (general_square, general))
        # iterate through each of those pieces
        for (start, piece) in options:
            if piece is not None and piece.get_color() == color:
                # iterate through each of that piece's valid moves
                for end in piece.valid_squares(start, self):
                    copyJanggiBoard = JanggiBoard(self._board.copy())
                    copyJanggiBoard.get_board()[start] = None
                    copyJanggiBoard.get_board()[end] = piece
                    # if the move would NOT leave the player in-check, then no checkmate occurred
                    if not copyJanggiBoard.is_in_check(color):
                        return False
                    del copyJanggiBoard
        # if the loops have completed and no valid move has been found, then it is checkmate
        return True

    def print_board(self):
        """Helper method to print a representation of the board"""
        print('    '+(' '*2)+'a'+(' '*5)+'b'+(' '*5)+'c'+(' '*5)+'d'+(' '*5)+'e'+
              (' '*5)+'f'+(' '*5)+'g'+(' '*5)+'h'+(' '*5)+'i'+(' '*3))
        print('   ' + '-' * (6*9))
        for num in range(1, 11):
            row_output = str(num).ljust(2) + ' |'
            for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
                square = letter + str(num)
                piece = self._board[square]
                if piece is not None:
                    output = str(piece)
                elif square in self._palace:
                    output = (' ' * 2) + '*' + (' ' * 2)
                else:
                    output = (' ' * 5)
                row_output += output + '|'
            print(row_output)
            print('   ' + '-' * (6*9))


class Piece:
    """
    Represents a piece on the board.
    This class is used as base class, from which the individual Piece Type classes inherit.
    The main reason for this inheritance is to share common logic (e.g. share helper methods) and avoid
      repetition of code for similar methods (e.g. each class has the same __repr__ method)
    """

    def __init__(self, color):
        """
        Initializes a piece with the given color
        :param color: either 'red' or 'blue'
        :is_captured: either True or False depending on if piece is captured; initialized to False
        """
        self._color = color
        self._is_captured = False

    def get_color(self):
        """Returns the color of the piece, either 'red' or 'blue'"""
        return self._color

    def get_is_captured(self):
        """Returns whether the piece is captured (out of play), either True or False"""
        return self._is_captured

    def set_is_captured(self, is_captured):
        """Given either True or False, sets whether this piece is captured"""
        self._is_captured = is_captured

    @staticmethod
    def mirror(square):
        """
        Helper method; given a square within the 4 corners of a palace, returns the square's diagonal 'mirror'
        d1 returns f3, f1 returns d3, d8 returns f10, f8 returns d10, and vice versa
        """
        assert square in ('d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10'), 'Mirror: square not in palace corners'
        letter = square[0]
        num = int(square[1:])
        mirror = ''
        mirror += 'd' if letter == 'f' else 'f'
        mirror += str(num + 2) if num in (1, 8) else str(num - 2)
        return mirror

    @staticmethod
    def shift(square, vertical, horizontal):
        """
        Helper method; given a square, returns the square shifted by the number of horizontal and vertical spaces;
          positive vertical values: indicate moving up the board (lower numerical values)
          positive horizontal values: indicate moving to the right (higher alphabetically)
          e.g. shift('e5', 2, -3) returns 'b3'
        If the starting square if off the range of the board, returns False
        :param square: the starting square, as a string in algebraic notation
        :param vertical: the number of spaces to shift vertically
        :param horizontal: the number of spaces to shift horizontally
        :return: the shifted square (as a string in algebraic notation) or False
        """
        start_let = square[0]
        start_ord = ord(square[0])
        start_num = int(square[1:])
        if not ('a' <= start_let <= 'i' and 1 <= start_num <= 10):
            return False
        end_num = start_num - vertical
        end_ord = start_ord + horizontal
        end_let = chr(end_ord)
        if not ('a' <= end_let <= 'i' and 1 <= end_num <= 10):
            return False
        end_square = end_let + str(end_num)
        return end_square

    def shift_dir(self, square, direction):
        """
        Helper method; given a square and direction, returns the square shifted by the one in the specified
          direction; e.g. shift_dir('e5', 'right') returns 'f5'
        If the starting square if off the range of the board, returns False
        If the shifted square is off the range of the board, returns False
        :param square: the starting square, as a string in algebraic notation
        :param direction: 'right' 'left' 'up' or 'down' as strings
        :return: the shifted square (as a string in algebraic notation) or False
        """
        if direction == 'right':
            return self.shift(square, 0, 1)
        if direction == 'left':
            return self.shift(square, 0, -1)
        if direction == 'up':
            return self.shift(square, 1, 0)
        if direction == 'down':
            return self.shift(square, -1, 0)

    def __repr__(self):
        """
        Used so that when a representation of the board is printed, the individual piece types
        are printed in a friendly manner
        """
        color = 'R' if self.get_color() == 'red' else 'B'
        class_name = self.__class__.__name__
        return class_name[0:3] + color + ' '

    def _valid_squares_guard_general(self, start, janggiBoard):
        """
        Since both the guard and general share the same movement logic, this method is held at the base Piece class
          in order to be shared across both sub-classes
        Generator function; given a start position and JanggiBoard object, returns a sequence of all valid end
          positions to which this piece could move
        DOES NOT check whether the move would leave this color's general in check - that is left to make_move() method
        :param start: the start square; as a string in algebraic notation
        :param janggiBoard: a JanggiBoard object
        :return: a sequence of valid end positions
        """
        # initialize helper variables
        board = janggiBoard.get_board()
        yield start
        palace = janggiBoard.get_palace(self.get_color())
        corners = janggiBoard.get_palace_corners(self.get_color())
        center = janggiBoard.get_palace_centers(self.get_color())
        # start the listing the squares - 1 spot up/down/left/right IFF that spot is inside palace
        for direction in ('up', 'right', 'down', 'left'):
            square = self.shift_dir(start, direction)
            if square in palace and (board[square] is None or board[square].get_color() != self.get_color()):
                yield square
        # if start in palace corners, add the center
        if start in corners:
            if board[center] is None or board[center].get_color() != self.get_color():
                yield center
        # if start is center, add the corners
        if start == center:
            for corner in corners:
                if board[corner] is None or board[corner].get_color() != self.get_color():
                    yield corner


class Soldier(Piece):
    """Represents a Solider. Inherits from the Piece class."""

    def __init__(self, color):
        """Initializes a Solider piece with the given color; color is either 'red' or 'blue'"""
        super().__init__(color)

    def valid_squares(self, start, janggiBoard):
        """
        Generator function; given a start position and JanggiBoard object, returns a sequence of all valid end
          positions to which this piece could move
        DOES NOT check whether the move would leave this color's general in check - that is left to make_move() method
        :param start: the start square; as a string in algebraic notation
        :param janggiBoard: a JanggiBoard object
        :return: a sequence of valid end positions
        """
        # establish helper variables
        board = janggiBoard.get_board()
        yield start
        # add left and right squares
        for direction in ('right', 'left'):
            square = self.shift_dir(start, direction)
            if square and (board[square] is None or board[square].get_color() != self.get_color()):
                yield square
        # if blue add up, if red add down
        square = self.shift_dir(start, 'up') if self.get_color() == 'blue' else self.shift_dir(start, 'down')
        if square and (board[square] is None or board[square].get_color() != self.get_color()):
            yield square
        # add palace-specific moves
        if start in ('d3', 'f3') and (board['e2'] is None or board['e2'].get_color() != self.get_color()):
            yield 'e2'
        if start in ('d8', 'f8') and (board['e9'] is None or board['e9'].get_color() != self.get_color()):
            yield 'e9'
        if start == 'e2':
            for square in ('d1', 'f1'):
                if board[square] is None or board[square].get_color() != self.get_color():
                    yield square
        if start == 'e9':
            for square in ('d10', 'f10'):
                if board[square] is None or board[square].get_color() != self.get_color():
                    yield square

    def _is_valid_movement(self, start, end, janggiBoard):
        """Private helper method used for debugging purposes; given start square, end square, and JanggiBoard object,
        checks whether a end square is contained within this piece's valid movements"""
        return end in self.valid_squares(start, janggiBoard)


class Cannon(Piece):
    """Represents a Cannon. Inherits from the Piece class."""

    def __init__(self, color):
        """Initializes a Cannon piece with the given color; color is either 'red' or 'blue'"""
        super().__init__(color)

    def valid_squares(self, start, janggiBoard):
        """
        Generator function; given a start position and JanggiBoard object, returns a sequence of all valid end
          positions to which this piece could move
        DOES NOT check whether the move would leave this color's general in check - that is left to make_move() method
        :param start: the start square; as a string in algebraic notation
        :param janggiBoard: a JanggiBoard object
        :return: a sequence of valid end positions
        """
        # initialize helper variables
        board = janggiBoard.get_board()
        # start square is a valid end position (a pass)
        yield start
        # add the right, left, up, down axes
        for direction in ('up', 'right', 'down', 'left'):
            piece_count = 0
            contains_cannon = False
            square = self.shift_dir(start, direction)  # shift the square by 1 in the given direction
            while square and piece_count < 2 and not contains_cannon:
                piece = board[square]
                if piece_count == 1 and piece is None:
                    yield square  # append if empty
                elif piece_count == 1 and piece.get_color() != self.get_color() and not isinstance(piece, Cannon):
                    yield square  # append if it contains opposing piece that is not a cannon
                if piece is not None:
                    piece_count += 1
                    contains_cannon = True if isinstance(piece, Cannon) else False
                square = self.shift_dir(square, direction)  # do another shift
        # if in the palace corners, check on adding the 'mirror' across diagonal
        if start in janggiBoard.get_palace_corners():
            square_color = 'red' if start in janggiBoard.get_palace_corners('red') else 'blue'
            center = janggiBoard.get_palace_centers(square_color)
            mirror = self.mirror(start)
            contains_cannon = True if isinstance(board[center], Cannon) or isinstance(board[mirror], Cannon) else False
            if not contains_cannon:
                if board[center] is not None and (board[mirror] is None or board[mirror].get_color() != self._color):
                    yield mirror

    def _is_valid_movement(self, start, end, janggiBoard):
        """Private helper method used for debugging purposes; given start square, end square, and JanggiBoard object,
        checks whether a end square is contained within this piece's valid movements"""
        return end in self.valid_squares(start, janggiBoard)


class Chariot(Piece):
    """Represents a Chariot. Inherits from the Piece class."""

    def __init__(self, color):
        """Initializes a Chariot piece with the given color; color is either 'red' or 'blue'"""
        super().__init__(color)

    def valid_squares(self, start, janggiBoard):
        """
        Generator function; given a start position and JanggiBoard object, returns a sequence of all valid end
          positions to which this piece could move
        DOES NOT check whether the move would leave this color's general in check - that is left to make_move() method
        :param start: the start square; as a string in algebraic notation
        :param janggiBoard: a JanggiBoard object
        :return: a sequence of valid end positions
        """
        board = janggiBoard.get_board()
        # start square is a valid end position (a pass)
        yield start
        # append the vertical and horizontal axes
        for direction in ('up', 'right', 'down', 'left'):
            piece_count = 0
            square = self.shift_dir(start, direction)  # shift the square by 1 in the given direction
            while square and piece_count == 0:  # square will be False if it is off the range of the board
                if board[square] is None:  # if square is empty, append it as an option
                    yield square
                if board[square] is not None:  # if square is not empty, append only if piece is opposing color
                    piece_count += 1
                    if board[square].get_color() != self.get_color():
                        yield square
                square = self.shift_dir(square, direction)  # do another shift
        # if in the palace corners, check on adding the middle and the 'mirror' across diagonal
        if start in janggiBoard.get_palace_corners():
            square_color = 'red' if start in janggiBoard.get_palace_corners('red') else 'blue'
            center = janggiBoard.get_palace_centers(square_color)
            mirror = self.mirror(start)
            if board[center] is None or board[center].get_color() != self.get_color():
                yield center  # if center is empty or contains opposing color, append it
            if board[center] is None and (board[mirror] is None or board[mirror].get_color() != self.get_color()):
                yield mirror  # if mirror is empty or contains opposing color, append it
        # if in the palace center, check on adding the diagonals
        if start in janggiBoard.get_palace_centers():
            square_color = 'red' if start == janggiBoard.get_palace_centers('red') else 'blue'
            corners = janggiBoard.get_palace_corners(square_color)
            for square in corners:
                if board[square] is None or board[square].get_color() != self.get_color():
                    yield square

    def _is_valid_movement(self, start, end, janggiBoard):
        """Private helper method used for debugging purposes; given start square, end square, and JanggiBoard object,
        checks whether a end square is contained within this piece's valid movements"""
        return end in self.valid_squares(start, janggiBoard)


class Elephant(Piece):
    """Represents a Elephant. Inherits from the Piece class."""

    def __init__(self, color):
        """Initializes a Elephant piece with the given color; color is either 'red' or 'blue'"""
        super().__init__(color)

    def valid_squares(self, start, janggiBoard):
        """
        Generator function; given a start position and JanggiBoard object, returns a sequence of all valid end
          positions to which this piece could move
        DOES NOT check whether the move would leave this color's general in check - that is left to make_move() method
        :param start: the start square; as a string in algebraic notation
        :param janggiBoard: a JanggiBoard object
        :return: a sequence of valid end positions
        """
        # establish helper variables
        board = janggiBoard.get_board()
        yield start  # start square would be considered a pass
        # loop through the squares 1 up, 1 down, 1 left, 1 right
        for vert, horz in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            square = self.shift(start, vert, horz)
            # if square at 1 step up/down/left/right is empty, continue
            if square and board[square] is None:
                # from 1 up/down/left/right, do a positive and negative jump
                pos_jump, neg_jump = (vert * 2 + horz, horz * 2 + vert), (vert * 2 - horz, horz * 2 - vert)
                for vert, horz in (pos_jump, neg_jump):
                    # if square at pos/neg jump is empty, continue
                    square = self.shift(start, vert, horz)
                    if square and board[square] is None:
                        # do another jump of the same type (e.g. +1 more right, +1 more up)
                        final_ver = vert + (1 if vert > 0 else -1)
                        final_horz = horz + (1 if horz > 0 else -1)
                        square = self.shift(start, final_ver, final_horz)
                        if square and (board[square] is None or board[square].get_color() != self.get_color()):
                            yield square

    def _is_valid_movement(self, start, end, janggiBoard):
        """Private helper method used for debugging purposes; given start square, end square, and JanggiBoard object,
        checks whether a end square is contained within this piece's valid movements"""
        return end in self.valid_squares(start, janggiBoard)


class Horse(Piece):
    """Represents a Horse. Inherits from the Piece class."""

    def __init__(self, color):
        """Initializes a Horse piece with the given color; color is either 'red' or 'blue'"""
        super().__init__(color)

    def valid_squares(self, start, janggiBoard):
        """
        Generator function; given a start position and JanggiBoard object, returns a sequence of all valid end
          positions to which this piece could move
        DOES NOT check whether the move would leave this color's general in check - that is left to make_move() method
        :param start: the start square; as a string in algebraic notation
        :param janggiBoard: a JanggiBoard object
        :return: a sequence of valid end positions
        """
        # establish helper variables
        board = janggiBoard.get_board()
        yield start  # start square would be considered a pass
        # loop through the squares 1 up, 1 down, 1 left, 1 right
        for vert, horz in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            square = self.shift(start, vert, horz)
            # if square at 1 step up/down/left/right is empty, continue
            if square and board[square] is None:
                # from 1 up/down/left/right, do a positive and negative jump
                pos_jump, neg_jump = (vert * 2 + horz, horz * 2 + vert), (vert * 2 - horz, horz * 2 - vert)
                for vert, horz in (pos_jump, neg_jump):
                    # if square at pos/neg jump is empty or contains opposing color, add to valid moves
                    square = self.shift(start, vert, horz)
                    if square and (board[square] is None or board[square].get_color() != self.get_color()):
                        yield square

    def _is_valid_movement(self, start, end, janggiBoard):
        """Private helper method used for debugging purposes; given start square, end square, and JanggiBoard object,
        checks whether a end square is contained within this piece's valid movements"""
        return end in self.valid_squares(start, janggiBoard)


class Guard(Piece):
    """Represents a Guard. Inherits from the Piece class."""

    def __init__(self, color):
        """Initializes a Guard piece with the given color; color is either 'red' or 'blue'"""
        super().__init__(color)

    def valid_squares(self, start, janggiBoard):
        """This piece's logic is held within the base Piece class in order to share between Guard & General"""
        return super()._valid_squares_guard_general(start, janggiBoard)

    def _is_valid_movement(self, start, end, janggiBoard):
        """Private helper method used for debugging purposes; given start square, end square, and JanggiBoard object,
        checks whether a end square is contained within this piece's valid movements"""
        return end in self.valid_squares(start, janggiBoard)


class General(Piece):
    """Represents a General. Inherits from the Piece class."""

    def __init__(self, color):
        """Initializes a General piece with the given color; color is either 'red' or 'blue'"""
        super().__init__(color)

    def valid_squares(self, start, janggiBoard):
        """This piece's logic is held within the base Piece class in order to share between Guard & General"""
        return super()._valid_squares_guard_general(start, janggiBoard)

    def _is_valid_movement(self, start, end, janggiBoard):
        """Private helper method used for debugging purposes; given start square, end square, and JanggiBoard object,
        checks whether a end square is contained within this piece's valid movements"""
        return end in self.valid_squares(start, janggiBoard)


class JanggiGame:
    """
    Represents the game Janggi (Korean chess)
    Contains a JanggiBoard object (using composition); that JanggiBoard contain the individual pieces
    This class' main purpose is to hold information about the state of the game, such as whose turn is next,
      whether the game is won or still ongoing
    This class is also the public interface through which moves on the board will be made
    """

    def __init__(self):
        """
        Initializes a JanggiGame object
        :current_color: either 'blue' or 'red' depending on which player's turn is next; initialized as blue
        :game_state: either 'UNFINISHED' 'RED_WON' or 'BLUE_WON'; initialized as 'UNFINISHED'
        :board: a JanggiBoard object; initialized with the correct starting positions; Elephant is
          transposed with the Horse on the right side
        :lost_pieces: keeps track of which pieces have been captured; key: 'blue' / 'red', value: list of pieces
        """
        start_board = {}
        for num in range(1, 11):
            for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
                square = letter + str(num)
                start_board[square] = None
                if square in ['a1', 'i1', 'a10', 'i10']:
                    start_board[square] = Chariot('red') if num == 1 else Chariot('blue')
                if square in ['b1', 'g1', 'b10', 'g10']:
                    start_board[square] = Elephant('red') if num == 1 else Elephant('blue')
                if square in ['c1', 'h1', 'c10', 'h10']:
                    start_board[square] = Horse('red') if num == 1 else Horse('blue')
                if square in ['d1', 'f1', 'd10', 'f10']:
                    start_board[square] = Guard('red') if num == 1 else Guard('blue')
                if square in ['e2', 'e9']:
                    start_board[square] = General('red') if num == 2 else General('blue')
                if square in ['b3', 'h3', 'b8', 'h8']:
                    start_board[square] = Cannon('red') if num == 3 else Cannon('blue')
                if square in ['a4', 'c4', 'e4', 'g4', 'i4', 'a7', 'c7', 'e7', 'g7', 'i7']:
                    start_board[square] = Soldier('red') if num == 4 else Soldier('blue')
        self._janggiBoard = JanggiBoard(start_board)
        self._current_color = 'blue'
        self._game_state = 'UNFINISHED'
        self._lost_pieces = {'red': [], 'blue': []}

    def _get_janggiBoard(self):
        """Returns the JanggiBoard object contained within this game"""
        return self._janggiBoard

    def print_board(self):
        """Prints the board"""
        self._janggiBoard.print_board()

    def get_game_state(self):
        """Returns current game state; either 'UNFINISHED' 'RED_WON' or 'BLUE_WON'"""
        return self._game_state

    def get_current_color(self):
        """Returns the turn of the next player; either 'red' or 'blue'"""
        return self._current_color

    def is_in_check(self, color):
        """
        Given a color, returns True if the color is in check based on the current board state; otherwise False
        The logic for this method lives at the janggiBoard class; the reason for that is so that this method
          can be called on differing board states - i.e. to ensure that a player can not make a move which
          puts or leaves their general in check
        :param color: the color of the player to determine if they're in-check; either 'red' or 'blue'
        """
        return self._janggiBoard.is_in_check(color)

    def make_move(self, start, end):
        """
        If move is valid, moves the piece located on the start square to end square, updates whose turn is next,
          determines if the opposing player is in checkmate (and updates game state if so), and returns True
        If move is invalid, returns False; move is invalid if (1) game is already won
          (2) the start or end squares are not within board range
          (3) the start square is empty or contains a piece color not matching the current turn
          (4) the end square is empty or contains a piece with the same color as start square
          (5) the movement is valid according to the piece type's movement rules
          (6) the move would not put or leave the player's General in check
        This method implements the logic for #1, #2, #3, #6 above (which are dependent on game state / whose turn it is)
          Logic for #4, #5 is held within the Piece object classes (which are not dependent on game state)
          and are called through the is_valid_move() method
        :param start: the starting square, as a string in algebraic notation; e.g. 'a7'
        :param end: the ending square, as a string in algebraic notation; e.g. 'b7'
        :return: True if move is valid, False is move was invalid
        """
        board = self._janggiBoard.get_board()
        # (1) move is invalid if the if game is already won
        if self._game_state != 'UNFINISHED':
            return False
        # (2) move is invalid if the start or end positions are not within range
        if start not in board or end not in board:
            return False
        piece = board[start]
        # (3) move is invalid if the start square is empty or the piece's color does not match the current turn
        if piece is None or piece.get_color() != self._current_color:
            return False
        # (4) / (5) move is invalid if it doesn't pass that piece type’s movement rules (see docstring)
        if end not in piece.valid_squares(start, self._janggiBoard):
            return False
        # (6) move is invalid if it would leave this player in check
        copyJanggiBoard = JanggiBoard(board.copy())
        copyJanggiBoard.get_board()[start] = None
        copyJanggiBoard.get_board()[end] = piece
        if copyJanggiBoard.is_in_check(self._current_color):
            return False
        del copyJanggiBoard
        # if move is valid, update the board
        board[start] = None
        if board[end] is not None:
            captured_piece = board[end]
            captured_piece.set_is_captured(True)
            self._lost_pieces[captured_piece.get_color()].append(captured_piece)
        board[end] = piece
        # if move is valid, update the turn
        self._current_color = 'red' if self._current_color == 'blue' else 'blue'
        # if current player is in check, determine if checkmate occurred, update game state if so
        if self._janggiBoard.is_in_check(self._current_color):
            is_checkmate = self._janggiBoard.is_in_checkmate(self._current_color)
            if is_checkmate:
                self._game_state = 'RED_WON' if self._current_color == 'blue' else 'BLUE_WON'
        return True


if __name__ == '__main__':
    pass


