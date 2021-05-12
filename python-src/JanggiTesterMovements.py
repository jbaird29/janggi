import unittest
from JanggiGame import JanggiGame, JanggiBoard, Piece, Soldier, Cannon, Chariot, Horse, Elephant, Guard, General


class TestPieceMovements(unittest.TestCase):
    """
    Test cases for the movement of the pieces; tests the _is_valid_movement() method of each piece type
    Diagram: https://docs.google.com/spreadsheets/d/1Hywg5iJgqXUmYXlrbIrT856SbwXKO69yxZd7GSeA1AM/edit#gid=1576536438
    """
    def setUp(self):
        self.janggiBoard = JanggiBoard()
        self.board = self.janggiBoard.get_board()

    def test_cannon1(self):
        cannonBlue = Cannon('blue')
        cannonRed = Cannon('red')
        soldierBlue = Soldier('blue')
        soldierRed = Soldier('red')
        self.board['d8'] = cannonBlue
        self.board['d6'] = soldierBlue
        self.board['d3'] = soldierRed
        self.board['c8'] = soldierBlue
        self.board['b8'] = cannonRed
        self.board['e8'] = soldierBlue
        self.board['g8'] = soldierBlue
        self.board['e9'] = soldierBlue
        self.board['f10'] = soldierRed
        self.assertTrue(cannonBlue._is_valid_movement('d8', 'd8', self.janggiBoard))
        # move upwards along d-file
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'd7', self.janggiBoard))
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'd6', self.janggiBoard))
        self.assertTrue(cannonBlue._is_valid_movement('d8', 'd5', self.janggiBoard))
        self.assertTrue(cannonBlue._is_valid_movement('d8', 'd4', self.janggiBoard))
        self.assertTrue(cannonBlue._is_valid_movement('d8', 'd3', self.janggiBoard))
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'd2', self.janggiBoard))
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'd1', self.janggiBoard))
        # move left - cannot capture cannon
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'c8', self.janggiBoard))
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'b8', self.janggiBoard))
        # move right - cannot jump over 2 pieces of same color
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'e8', self.janggiBoard))
        self.assertTrue(cannonBlue._is_valid_movement('d8', 'f8', self.janggiBoard))
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'g8', self.janggiBoard))
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'h8', self.janggiBoard))
        # move diagonal along palace
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'e9', self.janggiBoard))
        self.assertTrue(cannonBlue._is_valid_movement('d8', 'f10', self.janggiBoard))
        self.board['e9'] = None
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'f10', self.janggiBoard))
        self.board['e9'] = cannonRed
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'f10', self.janggiBoard))
        self.board['e9'] = soldierBlue
        self.board['f10'] = cannonRed
        self.assertFalse(cannonBlue._is_valid_movement('d8', 'f10', self.janggiBoard))
        self.board['f10'] = soldierRed
        self.assertTrue(cannonBlue._is_valid_movement('d8', 'f10', self.janggiBoard))

    def test_cannon2(self):
        # test that cannon cannot jump over cannon (of either color)
        start = 'h5'
        p = Cannon('blue')
        c1 = Cannon('blue')
        c2 = Cannon('red')
        self.board[start] = p
        self.board['h4'] = c1
        self.board['g5'] = c2
        self.assertFalse(p._is_valid_movement(start, 'h3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'f5', self.janggiBoard))

    def test_cannon_edge(self):
        p = Cannon('blue')
        s1 = Soldier('red')
        s2 = Soldier('blue')
        start = 'a1'
        self.board[start] = p
        self.board['a8'] = s1
        self.board['g1'] = s2
        moves_1 = {square for square in p.valid_squares(start, self.janggiBoard)}
        moves_2 = {'a1', 'h1', 'i1', 'a9', 'a10'}
        self.assertEqual(moves_1, moves_2)

    def test_solider1(self):
        start = 'e4'
        s1 = Soldier('blue')
        self.board[start] = s1
        self.assertTrue(s1._is_valid_movement(start, 'e3', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'e3', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'f4', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'd4', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'f3', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'd3', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'd5', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'e5', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'f5', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'e2', self.janggiBoard))

    def test_solider2(self):
        start = 'd1'
        s1 = Soldier('blue')
        self.board[start] = s1
        self.assertTrue(s1._is_valid_movement(start, 'c1', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'e1', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'c2', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'd2', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'e2', self.janggiBoard))

    def test_solider3(self):
        start = 'e2'
        s1 = Soldier('blue')
        self.board[start] = s1
        self.assertTrue(s1._is_valid_movement(start, 'd1', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'e1', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'f1', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'd2', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'f2', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'e3', self.janggiBoard))

    def test_solider4(self):
        start = 'd8'
        s1 = Soldier('red')
        self.board[start] = s1
        self.assertTrue(s1._is_valid_movement(start, 'c8', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'e8', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'd9', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'e9', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'c9', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'c7', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'd7', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'e7', self.janggiBoard))

    def test_solider5(self):
        start = 'e10'
        s1 = Soldier('red')
        self.board[start] = s1
        self.assertTrue(s1._is_valid_movement(start, 'd10', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'e10', self.janggiBoard))
        self.assertTrue(s1._is_valid_movement(start, 'f10', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'e9', self.janggiBoard))

    def test_solider6(self):
        start = 'a10'
        s1 = Soldier('red')
        self.board[start] = s1
        self.assertTrue(s1._is_valid_movement(start, 'b10', self.janggiBoard))
        self.assertFalse(s1._is_valid_movement(start, 'a9', self.janggiBoard))

    def test_horse(self):
        start = 'e6'
        p = Horse('blue')
        s1 = Soldier('red')
        s2 = Soldier('blue')
        s3 = Soldier('blue')
        s4 = Soldier('blue')
        self.board[start] = p
        self.board['f4'] = s1
        self.board['g6'] = s2
        self.board['e7'] = s3
        self.board['c5'] = s4
        self.assertTrue(p._is_valid_movement(start, start, self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'd4', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f4', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'g5', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'g7', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'c7', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c5', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'e5', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'e4', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'd5', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'f5', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'e3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'd8', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'f8', self.janggiBoard))

    def test_horse_edge(self):
        p = Horse('blue')
        start = 'a1'
        self.board[start] = p
        moves_1 = {square for square in p.valid_squares(start, self.janggiBoard)}
        moves_2 = {'a1', 'c2', 'b3'}
        self.assertEqual(moves_1, moves_2)

    def test_elephant(self):
        start = 'e6'
        p = Elephant('blue')
        s1 = Soldier('red')
        s2 = Soldier('red')
        s3 = Soldier('blue')
        s4 = Soldier('blue')
        s5 = Soldier('blue')
        s6 = Soldier('blue')
        s7 = Soldier('blue')
        self.board[start] = p
        self.board['d4'] = s1
        self.board['h4'] = s2
        self.board['f4'] = s3
        self.board['h5'] = s4
        self.board['g6'] = s5
        self.board['h7'] = s6
        self.board['e7'] = s7
        self.assertTrue(p._is_valid_movement(start, start, self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'h4', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'h8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'b4', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'b8', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'd4', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c5', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c6', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c7', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c9', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g9', self.janggiBoard))

    def test_elephant_edge(self):
        p = Elephant('blue')
        start = 'a1'
        self.board[start] = p
        moves_1 = {square for square in p.valid_squares(start, self.janggiBoard)}
        moves_2 = {'a1', 'd3', 'c4'}
        self.assertEqual(moves_1, moves_2)

    def test_guard1(self):
        start = 'f2'
        p = Guard('red')
        s1 = Soldier('blue')
        self.board[start] = p
        self.board['f3'] = s1
        self.assertTrue(p._is_valid_movement(start, start, self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f1', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f3', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e2', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g1', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g2', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'e1', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'e3', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'd2', self.janggiBoard))

    def test_guard2(self):
        start = 'e9'
        p = Guard('blue')
        s1 = Soldier('red')
        self.board[start] = p
        self.board['e8'] = s1
        self.assertTrue(p._is_valid_movement(start, 'd8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'd9', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'd10', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e10', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f9', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f10', self.janggiBoard))

    def test_guard3(self):
        start = 'f8'
        p = Guard('blue')
        self.board[start] = p
        self.assertTrue(p._is_valid_movement(start, 'e8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e9', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f9', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'f7', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g8', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g9', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g7', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'e7', self.janggiBoard))

    def test_chariot(self):
        start = 'b5'
        p = Chariot('red')
        s1 = Soldier('red')
        s2 = Soldier('blue')
        s3 = Soldier('blue')
        self.board[start] = p
        self.board['b8'] = s1
        self.board['b9'] = s2
        self.board['b2'] = s3
        self.assertTrue(p._is_valid_movement(start, start, self.janggiBoard))
        # moving up
        self.assertTrue(p._is_valid_movement(start, 'b4', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'b3', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'b2', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'b1', self.janggiBoard))
        # moving down
        self.assertTrue(p._is_valid_movement(start, 'b6', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'b7', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'b8', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'b9', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'b10', self.janggiBoard))
        # moving diagonal
        self.assertFalse(p._is_valid_movement(start, 'a4', self.janggiBoard))
        # moving sideways
        self.assertTrue(p._is_valid_movement(start, 'a5', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'i5', self.janggiBoard))

    def test_chariot2(self):
        start = 'e9'
        p = Chariot('blue')
        self.board[start] = p
        self.assertTrue(p._is_valid_movement(start, 'd8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'd9', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'd10', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f9', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f10', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e8', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e9', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e10', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g7', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'c7', self.janggiBoard))

    def test_chariot3(self):
        start = 'f3'
        p = Chariot('blue')
        self.board[start] = p
        self.assertTrue(p._is_valid_movement(start, 'f1', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f2', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e2', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'd1', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'e3', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'd3', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'g3', self.janggiBoard))
        self.assertTrue(p._is_valid_movement(start, 'f4', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'e1', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'd2', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g2', self.janggiBoard))
        self.assertFalse(p._is_valid_movement(start, 'g4', self.janggiBoard))

    def test_chariot_edge(self):
        p = Chariot('blue')
        start = 'a1'
        self.board[start] = p
        moves_1 = {square for square in p.valid_squares(start, self.janggiBoard)}
        moves_2 = {'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1',
                   'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10'}
        self.assertEqual(moves_1, moves_2)


if __name__ == '__main__':
    unittest.main()
