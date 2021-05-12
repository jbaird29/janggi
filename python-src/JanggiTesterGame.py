import unittest
from JanggiGame import JanggiGame, JanggiBoard, Piece, Soldier, Cannon, Chariot, Horse, Elephant, Guard, General


class TestPieceMethods(unittest.TestCase):
    """
    Test cases for the JanggiGame methods
    """
    def setUp(self):
        self.piece = Piece('red')

    def testShift(self):
        self.assertEqual(self.piece.shift('h5', 1, 1), 'i4')
        self.assertEqual(self.piece.shift('h5', -1, -1), 'g6')
        self.assertFalse(self.piece.shift('a10', -1, -1))
        self.assertFalse(self.piece.shift('i1', 1, 1))

    def testShiftDir(self):
        self.assertEqual(self.piece.shift_dir('h5', 'right'), 'i5')
        self.assertEqual(self.piece.shift_dir('h5', 'left'), 'g5')
        self.assertEqual(self.piece.shift_dir('h5', 'up'), 'h4')
        self.assertEqual(self.piece.shift_dir('h5', 'down'), 'h6')
        self.assertFalse(self.piece.shift_dir('a10', 'left'))


class TestBoardMethods(unittest.TestCase):
    """
    Test cases for the JanggiGame methods
    """
    def setUp(self):
        self.janggiGame = JanggiGame()
        self.janggiBoard = self.janggiGame._get_janggiBoard()
        self.board = self.janggiBoard.get_board()

    def testGetGeneral(self):
        self.assertEqual(self.janggiBoard.get_general_square('blue'), 'e9')
        self.assertEqual(self.janggiBoard.get_general_square('red'), 'e2')

    def testInCheck1(self):
        # move blue knight to put the red general in check
        blueHorse = self.board['c10']
        self.board['c10'] = None
        self.board['f4'] = blueHorse
        self.assertTrue(self.janggiBoard.is_in_check('red'))


class TestMakeMovesInCheck(unittest.TestCase):
    """
    Test cases in which the player is in check and must make move to get out of check
    """
    def setUp(self):
        self.janggiGame = JanggiGame()
        self.janggiBoard = self.janggiGame._get_janggiBoard()
        self.board = self.janggiBoard.get_board()
        # move chariot1 to put blue general in check
        # move chariot2 to align to row above the general
        redChariot1 = self.board['a1']
        redChariot2 = self.board['i1']
        self.board['a1'] = None
        self.board['i1'] = None
        self.board['f9'] = redChariot1
        self.board['g8'] = redChariot2

    def testInCheck(self):
        self.assertTrue(self.janggiBoard.is_in_check('blue'))

    def test1(self):
        # cannot move another piece if blue general is left in check
        self.assertFalse(self.janggiGame.make_move('a7', 'a6'))

    def test2(self):
        # cannot move general if it would still be left in check by SAME attacking piece
        self.assertFalse(self.janggiGame.make_move('e9', 'd9'))

    def test3(self):
        # cannot move general if it would still be moving into check by DIFFERENT piece
        self.assertFalse(self.janggiGame.make_move('e9', 'e8'))

    def test4(self):
        # CAN move general if it would get out of check
        self.assertTrue(self.janggiGame.make_move('e9', 'e10'))

    def test5(self):
        # CAN capture the attacking piece if it would get out of check
        self.assertTrue(self.janggiGame.make_move('f10', 'f9'))


class TestTurnTaking(unittest.TestCase):
    """
    Test cases for basic turn taking
    """
    def setUp(self):
        self.game = JanggiGame()

    def test1(self):
        """
        Solder Blue advances up, capturing pieces and causing a checkmate
        """
        SolB = self.game._get_janggiBoard().get_board()['e7']
        SolR = self.game._get_janggiBoard().get_board()['e4']
        EleR = self.game._get_janggiBoard().get_board()['g1']
        GenR = self.game._get_janggiBoard().get_board()['e2']
        self.assertFalse(SolR.get_is_captured())
        self.assertTrue(self.game.make_move('e7', 'e6'))
        self.assertTrue(self.game.make_move('e4', 'e5'))   # SolR moves in position to be captured
        self.assertTrue(self.game.make_move('e6', 'e5'))   # SolB captures SolR
        self.assertTrue(SolR.get_is_captured())
        self.assertFalse(EleR.get_is_captured())
        self.assertTrue(self.game.make_move('g1', 'e4'))   # EleR moves in position to be captured
        self.assertTrue(self.game.make_move('e5', 'e4'))   # SolB captures EleR
        self.assertTrue(EleR.get_is_captured())
        self.assertFalse(self.game.is_in_check('red'))     # red is not yet in check
        self.assertFalse(self.game.make_move('e2', 'e3'))  # GenR cannot move itself into a check position
        self.assertTrue(self.game.make_move('e2', 'f3'))
        self.assertTrue(self.game.make_move('e4', 'e3'))
        self.assertTrue(self.game.is_in_check('red'))      # red is in check now
        self.assertFalse(self.game.make_move('f3', 'e2'))  # GenR cannot make a move which remains in check
        self.assertTrue(self.game.make_move('f3', 'f2'))
        self.assertTrue(self.game.make_move('c10', 'd8'))  # blue moves horse
        self.assertTrue(self.game.make_move('f2', 'f2'))   # red passes
        self.assertTrue(self.game.make_move('d8', 'f7'))   # blue moves horse
        self.assertTrue(self.game.make_move('a1', 'a1'))   # red passes
        self.assertTrue(self.game.make_move('f7', 'e5'))   # blue moves horse
        self.assertTrue(self.game.make_move('d1', 'e1'))   # red moves guard to box in his own general
        self.assertTrue(self.game.make_move('e3', 'f3'))   # blue moves to CHECKMATE
        self.assertEqual(self.game.get_game_state(), 'BLUE_WON')
        self.assertTrue(self.game._get_janggiBoard().is_in_checkmate('red'))

    def test2(self):
        self.assertTrue(self.game.make_move('e7', 'e6'))
        self.assertTrue(self.game.make_move('c4', 'c5'))
        self.assertTrue(self.game.make_move('c10', 'd8'))
        self.assertTrue(self.game.make_move('b1', 'd4'))
        self.assertTrue(self.game.make_move('b8', 'e8'))
        self.assertTrue(self.game.make_move('c5', 'd5'))
        self.assertTrue(self.game.make_move('c7', 'c6'))
        self.assertTrue(self.game.make_move('e4', 'e5'))
        self.assertTrue(self.game.make_move('a7', 'a6'))
        self.assertFalse(self.game.make_move('e5', 'e6'))  # move would PUT general in-check from Cannon
        self.assertTrue(self.game.make_move('d5', 'd6'))
        self.assertTrue(self.game.make_move('c6', 'c5'))
        self.assertTrue(self.game.make_move('d6', 'e6'))
        self.assertTrue(self.game.make_move('e8', 'a8'))
        self.assertTrue(self.game.make_move('e6', 'e7'))
        self.assertTrue(self.game.make_move('a6', 'a5'))
        self.assertTrue(self.game.make_move('e5', 'e6'))
        self.assertTrue(self.game.make_move('a5', 'a4'))
        self.assertTrue(self.game.make_move('e7', 'e8'))
        self.assertTrue(self.game.is_in_check('blue'))
        self.assertFalse(self.game.is_in_check('red'))
        self.assertTrue(self.game.get_game_state(), 'UNFINISHED')
        self.assertFalse(self.game.make_move('f10', 'f9'))  # move would LEAVE general in-check from Solider
        self.assertTrue(self.game.make_move('e9', 'e8'))
        self.assertTrue(self.game.make_move('d4', 'b7'))
        self.assertTrue(self.game.make_move('a8', 'a1'))
        self.assertTrue(self.game.make_move('b7', 'd10'))
        self.assertTrue(self.game.make_move('a10', 'a6'))
        self.assertTrue(self.game.make_move('d1', 'd2'))
        self.assertTrue(self.game.make_move('a1', 'f1'))
        self.assertTrue(self.game.make_move('e2', 'f1'))
        self.assertTrue(self.game.make_move('a6', 'e6'))
        self.assertTrue(self.game.make_move('h1', 'g3'))
        self.assertTrue(self.game.make_move('i10', 'i9'))
        self.assertTrue(self.game.make_move('g4', 'g5'))
        self.assertTrue(self.game.make_move('a4', 'a3'))
        self.assertTrue(self.game.make_move('g3', 'h5'))
        self.assertTrue(self.game.make_move('a3', 'b3'))
        self.assertTrue(self.game.make_move('d2', 'e2'))
        self.assertTrue(self.game.make_move('b3', 'c3'))
        self.assertTrue(self.game.make_move('h5', 'i7'))
        self.assertTrue(self.game.make_move('c3', 'd3'))
        self.assertTrue(self.game.make_move('e2', 'd3'))
        self.assertTrue(self.game.make_move('c5', 'c4'))
        self.assertTrue(self.game.make_move('d3', 'e2'))
        self.assertTrue(self.game.make_move('c4', 'c3'))
        self.assertTrue(self.game.make_move('h3', 'b3'))
        self.assertTrue(self.game.make_move('c3', 'd3'))
        self.assertTrue(self.game.make_move('g5', 'h5'))
        self.assertTrue(self.game.make_move('d3', 'e2'))
        self.assertTrue(self.game.is_in_check('red'))
        self.assertFalse(self.game.is_in_check('blue'))
        self.assertTrue(self.game.get_game_state(), 'UNFINISHED')
        self.assertFalse(self.game.make_move('f1', 'e2'))  # would get general out of check but leave in different check
        self.assertTrue(self.game.make_move('c1', 'e2'))
        self.assertTrue(self.game.make_move('h8', 'h1'))
        self.assertTrue(self.game.is_in_check('red'))
        self.assertFalse(self.game.is_in_check('blue'))
        self.assertTrue(self.game.get_game_state(), 'UNFINISHED')
        self.assertFalse(self.game.make_move('f1', 'e1'))  # leaves general in check by cannon
        self.assertTrue(self.game.make_move('i1', 'h1'))
        self.assertTrue(self.game.make_move('i9', 'f9'))
        self.assertTrue(self.game.is_in_check('red'))
        self.assertFalse(self.game.is_in_check('blue'))
        self.assertTrue(self.game.get_game_state(), 'UNFINISHED')
        self.assertTrue(self.game.make_move('e2', 'f4'))
        self.assertTrue(self.game.make_move('f9', 'f4'))
        self.assertTrue(self.game.is_in_check('red'))
        self.assertFalse(self.game.is_in_check('blue'))
        self.assertTrue(self.game.get_game_state(), 'BLUE_WON')  # checkmate
        self.assertFalse(self.game.make_move('f1', 'f1'))  # can't make a move after checkmate

    def test3(self):
        self.assertTrue(self.game.make_move('e9', 'd8'))
        self.assertTrue(self.game.make_move('e2', 'e1'))
        self.assertEqual(self.game.get_game_state(), 'UNFINISHED')
        self.game._get_janggiBoard().get_board()['e4'] = None
        self.game._get_janggiBoard().get_board()['e7'] = None
        self.game._get_janggiBoard().get_board()['b1'] = None
        self.game._get_janggiBoard().get_board()['c1'] = None
        self.game._get_janggiBoard().get_board()['g1'] = None
        self.game._get_janggiBoard().get_board()['d1'] = Elephant('red')
        self.game._get_janggiBoard().get_board()['f1'] = Elephant('red')
        self.game._get_janggiBoard().get_board()['f9'] = Horse('red')
        self.game._get_janggiBoard().get_board()['f8'] = Soldier('blue')
        self.game._get_janggiBoard().get_board()['e10'] = Chariot('blue')
        self.assertTrue(self.game.make_move('e10', 'e9'))
        self.game.print_board()
        self.assertTrue(self.game.is_in_check('red'))
        self.assertEqual(self.game.get_game_state(), 'BLUE_WON')


if __name__ == '__main__':
    unittest.main()
