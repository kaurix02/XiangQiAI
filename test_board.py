from board import *

default_board = [
    [Piece('R', 0, 0, 0), Piece('H', 0, 1, 0), Piece('E', 0, 2, 0), Piece('A', 0, 3, 0), Piece('G', 0, 4, 0),
     Piece('A', 0, 5, 0), Piece('E', 0, 6, 0), Piece('H', 0, 7, 0), Piece('R', 0, 8, 0)],
    [None, None, None, None, None, None, None, None, None],
    [None, Piece('C', 2, 1, 0), None, None, None, None, None, Piece('C', 2, 7, 0), None],
    [Piece('S', 3, 0, 0), None, Piece('S', 3, 2, 0), None, Piece('S', 3, 4, 0),
     None, Piece('S', 3, 6, 0), None, Piece('S', 3, 8, 0)],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [Piece('S', 6, 0, 1), None, Piece('S', 6, 2, 1), None, Piece('S', 6, 4, 1),
     None, Piece('S', 6, 6, 1), None, Piece('S', 6, 8, 1)],
    [None, Piece('C', 7, 1, 1), None, None, None, None, None, Piece('C', 7, 7, 1), None],
    [None, None, None, None, None, None, None, None, None],
    [Piece('R', 9, 0, 1), Piece('H', 9, 1, 1), Piece('E', 9, 2, 1), Piece('A', 9, 3, 1), Piece('G', 9, 4, 1),
     Piece('A', 9, 5, 1), Piece('E', 9, 6, 1), Piece('H', 9, 7, 1), Piece('R', 9, 8, 1)]
]


def switch_places(matrix, x1, y1, x2, y2):
    a = deepcopy(matrix[x1][y1])
    matrix[x1][y1] = matrix[x2][y2]
    matrix[x2][y2] = a
    if matrix[x1][y1] is not None:
        matrix[x1][y1].x = x1
        matrix[x1][y1].y = y1
    if matrix[x2][y2] is not None:
        matrix[x2][y2].x = x2
        matrix[x2][y2].y = y2
    return matrix


def test_init_default():
    b = Board()
    assert b.board == default_board, "Default board is not correct."
    print("Passed: Default board is correct!")


def test_init_custom():
    str_board = """
R0|  |  |A0|G0|A0|E0|H0|  
  |  |  |  |E0|  |  |  |
  |C0|  |  |S0|  |  |C1| 
S1|  |S1|  |  |  |  |  |S1
  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |
S1|  |S0|  |  |  |S0|  |S0
  |C1|  |  |  |  |  |C0| 
S1|  |  |  |  |A1|  |  | 
R0|  |  |A1|G1|  |E1|H1|R1
"""

    custom_board = [
        [Piece('R', 0, 0, 0), None, None, Piece('A', 0, 3, 0), Piece('G', 0, 4, 0),
         Piece('A', 0, 5, 0), Piece('E', 0, 6, 0), Piece('H', 0, 7, 0), None],
        [None, None, None, None, Piece('E', 1, 4, 0), None, None, None, None],
        [None, Piece('C', 2, 1, 0), None, None, Piece('S', 2, 4, 0), None, None, Piece('C', 2, 7, 1), None],
        [Piece('S', 3, 0, 1), None, Piece('S', 3, 2, 1), None, None,
         None, None, None, Piece('S', 3, 8, 1)],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [Piece('S', 6, 0, 1), None, Piece('S', 6, 2, 0), None, None,
         None, Piece('S', 6, 6, 0), None, Piece('S', 6, 8, 0)],
        [None, Piece('C', 7, 1, 1), None, None, None, None, None, Piece('C', 7, 7, 0), None],
        [Piece('S', 8, 0, 1), None, None, None, None, Piece('A', 8, 5, 1), None, None, None],
        [Piece('R', 9, 0, 0), None, None, Piece('A', 9, 3, 1), Piece('G', 9, 4, 1),
         None, Piece('E', 9, 6, 1), Piece('H', 9, 7, 1), Piece('R', 9, 8, 1)]
    ]

    b = Board(strboard=str_board)
    assert b.board == custom_board, "Custom board is not correct."
    print("Passed: Custom board is correct!")


def test_make_move():
    b = Board()
    b.make_move(0, 2, 2, 4)
    move_1 = switch_places(default_board, 0, 2, 2, 4)
    assert b.board == move_1, "Move (0,2) -> (2,4) executed incorrectly!"

    b.make_move(9, 7, 7, 6)
    move_2 = switch_places(move_1, 9, 7, 7, 6)
    assert b.board == move_2, "Move (9,7) -> (7,6) executed incorrectly!"

    b.make_move(3, 2, 4, 2)
    move_3 = switch_places(move_2, 3, 2, 4, 2)
    assert b.board == move_3, "Move (3,2) -> (4,2) executed incorrectly!"

    b.make_move(6, 8, 5, 8)
    move_4 = switch_places(move_3, 6, 8, 5, 8)
    assert b.board == move_4, "Move (6,8) -> (5,8) executed incorrectly!"

    b.make_move(Piece('R', 9, 0, 1), 8, 0)
    move_5 = switch_places(move_4, 9, 0, 8, 0)
    assert b.board == move_5, "Move (9,0) -> (8,0) executed incorrectly!"

    print("Passed: make_move!")


def test_get_all_moves():
    ### SOLDIERS ###
    soldier1 = Piece('S', 4, 5, 0)  # Has not crossed the river (player 1)
    assert soldier1.get_all_moves() == [(5, 5)], "Soldier's moves incorrect!"

    soldier2 = Piece('S', 5, 4, 1)  # Has not crossed the river (player 2)
    assert soldier2.get_all_moves() == [(4, 4)], "Soldier's moves incorrect!"

    soldier3 = Piece('S', 7, 0, 0)  # Has crossed the river (player 1)
    assert set(soldier3.get_all_moves()) == {(7, 1), (8, 0)}, "Soldier's moves incorrect!"

    soldier4 = Piece('S', 6, 5, 0)  # Has crossed the river (player 1)
    assert set(soldier4.get_all_moves()) == {(7, 5), (6, 4), (6, 6)}, "Soldier's moves incorrect!"

    soldier5 = Piece('S', 2, 4, 1)  # Has crossed the river (player 2)
    assert set(soldier5.get_all_moves()) == {(1, 4), (2, 3), (2, 5)}, "Soldier's moves incorrect!"

    ### ADVISORS ###
    advisor1 = Piece('A', 0, 3, 0)  # Player 1
    advisor2 = Piece('A', 0, 5, 0)
    assert advisor1.get_all_moves() == [(1, 4)] and advisor2.get_all_moves() == [(1, 4)], "Advisor's moves incorrect!"

    advisor3 = Piece('A', 9, 3, 1)  # Player 2
    advisor4 = Piece('A', 9, 3, 5)
    assert advisor3.get_all_moves() == [(8, 4)] and advisor4.get_all_moves() == [(8, 4)], "Advisor's moves incorrect!"

    advisor5 = Piece('A', 1, 4, 0)  # Player 1
    assert set(advisor5.get_all_moves()) == {(0, 3), (0, 5), (2, 3), (2, 5)}, "Advisor's moves incorrect!"

    advisor6 = Piece('A', 8, 4, 1)  # Player 2
    assert set(advisor6.get_all_moves()) == {(9, 3), (9, 5), (7, 3), (7, 5)}, "Advisor's moves incorrect!"

    ### GOVERNATORS ###
    governator1 = Piece('G', 1, 4, 0)  # Player 1
    assert set(governator1.get_all_moves()) == {(0, 4), (1, 3), (1, 5), (2, 4)}, "Governator's moves incorrect!"

    governator2 = Piece('G', 9, 4, 1)  # Player 2
    assert set(governator2.get_all_moves()) == {(9, 3), (9, 5), (8, 4)}, "Governator's moves incorrect!"

    governator3 = Piece('G', 7, 3, 1)
    assert set(governator3.get_all_moves()) == {(7, 4), (8, 3)}, "Governator's moves incorrect!"

    ### HORSES ###
    horse1 = Piece('H', 0, 1, 0)  # Player 1
    assert set(horse1.get_all_moves()) == {(2, 2), (2, 0), (1, 3)}, "Horse's moves incorrect!"

    horse2 = Piece('H', 7, 3, 1)  # Player 2
    assert set(horse2.get_all_moves()) == {(9, 4), (9, 2), (5, 4), (5, 2), (6, 5), (8, 5), (6, 1),
                                           (8, 1)}, "Horse's moves incorrect!"

    ### ELEPHANTS ###
    elephant1 = Piece('E', 0, 2, 0)  # Player 1
    assert set(elephant1.get_all_moves()) == {(2, 0), (2, 4)}, "Elephant's moves incorrect!"

    elephant2 = Piece('E', 4, 3, 0)
    assert set(elephant2.get_all_moves()) == {(2, 1), (2, 5)}, "Elephant's moves incorrect!"

    elephant3 = Piece('E', 7, 6, 1)  # Player 2
    assert set(elephant3.get_all_moves()) == {(9, 8), (9, 4), (5, 8), (5, 4)}, "Elephant's moves incorrect!"

    ### ROOKS % CANNONS ###
    rook1 = Piece('R', 0, 0, 0)  # Player 1
    cannon1 = Piece('C', 0, 0, 0)
    assert set(rook1.get_all_moves()) == set(
        [(i, 0) for i in range(1, 10)] + [(0, i) for i in range(1, 9)]), "Rook's moves incorrect!"
    assert set(cannon1.get_all_moves()) == set(
        [(i, 0) for i in range(1, 10)] + [(0, i) for i in range(1, 9)]), "Cannon's moves incorrect!"

    rook2 = Piece('R', 4, 4, 0)
    cannon2 = Piece('C', 4, 4, 0)
    assert set(rook2.get_all_moves()) == {(4, 3), (4, 2), (4, 1), (4, 0), (4, 5), (4, 6), (4, 7), (4, 8), (3, 4),
                                          (2, 4), (1, 4), (0, 4), (5, 4), (6, 4), (7, 4), (8, 4),
                                          (9, 4)}, "Rook's moves incorrect!"
    assert set(cannon2.get_all_moves()) == {(4, 3), (4, 2), (4, 1), (4, 0), (4, 5), (4, 6), (4, 7), (4, 8), (3, 4),
                                            (2, 4), (1, 4), (0, 4), (5, 4), (6, 4), (7, 4), (8, 4),
                                            (9, 4)}, "Cannon's moves incorrect!"

    rook3 = Piece('R', 8, 7, 1)  # Player 2
    cannon3 = Piece('C', 8, 7, 1)
    assert set(rook3.get_all_moves()) == {(9, 7), (8, 8)}.union(
        set([(i, 7) for i in range(8)] + [(8, i) for i in range(7)])), "Rook's moves incorrect!"
    assert set(cannon3.get_all_moves()) == {(9, 7), (8, 8)}.union(
        set([(i, 7) for i in range(8)] + [(8, i) for i in range(7)])), "Cannon's moves incorrect!"

    print("Passed: get_all_moves!")


def test_can_move():
    b = Board()

    ### SOLDIERS ###
    soldier1 = Piece('S', 3, 0, 0)  # Not over the river
    assert b.can_move(soldier1, (4, 0))
    assert not b.can_move(soldier1, (2, 0))
    assert not b.can_move(soldier1, (3, 1))

    soldier2 = Piece('S', 5, 4, 0)  # Over the river
    b.make_move(3, 4, 5, 4)
    assert b.can_move(soldier2, (5, 5))
    assert b.can_move(soldier2, (5, 3))
    assert b.can_move(soldier2, (6, 4))  # Can take an opponent's piece

    soldier3 = Piece('S', 6, 0, 1)  # Not over the river
    assert b.can_move(soldier3, (5, 0))
    assert not b.can_move(soldier3, (6, 1))

    soldier4 = Piece('S', 5, 6, 1)  # Not over the river
    b.make_move(6, 6, 5, 6)
    assert not b.can_move(soldier4, (5, 5))
    assert not b.can_move(soldier4, (5, 7))
    assert b.can_move(soldier4, (4, 6))

    ### ADVISORS ###
    advisor1 = Piece('A', 2, 3, 0)  # Player 1
    assert not b.can_move(advisor1, (3, 2))
    assert not b.can_move(advisor1, (2, 4))
    assert not b.can_move(advisor1, (1, 3))
    assert not b.can_move(advisor1, (1, 2))

    advisor2 = Piece('A', 0, 3, 0)
    assert b.can_move(advisor2, (1, 4))
    assert not b.can_move(advisor2, (0, 2))
    assert not b.can_move(advisor2, (1, 3))

    advisor3 = Piece('A', 9, 5, 1)  # Player 2
    assert b.can_move(advisor3, (8, 4))
    assert not b.can_move(advisor3, (8, 5))

    ### GOVERNATORS ###
    governator1 = Piece('G', 1, 4, 0)  # Player 1
    b.make_move(0, 4, 1, 4)
    assert b.can_move(governator1, (0, 4))
    assert b.can_move(governator1, (2, 4))
    assert b.can_move(governator1, (1, 3))
    assert b.can_move(governator1, (1, 5))

    governator2 = Piece('G', 9, 4, 1)  # Player 2
    b.make_move(9, 3, 8, 4)
    assert b.can_move(governator2, (9, 3))
    assert not b.can_move(governator2, (8, 4))  # Blocked by another piece

    ### HORSES ###
    horse1 = Piece('H', 0, 7, 0)
    assert b.can_move(horse1, (2, 6))
    assert b.can_move(horse1, (2, 8))
    # Let's move R0 next to H0
    b.make_move(0, 8, 1, 7)
    assert not b.can_move(horse1, (2, 6))  # R0 is blocking the way
    assert not b.can_move(horse1, (2, 8))
    # Let's move R0 back
    b.make_move(1, 7, 0, 8)

    ### ELEPHANTS ###
    elephant1 = Piece('E', 0, 2, 0)  # Player 1
    assert b.can_move(elephant1, (2, 4))
    b.make_move(1, 4, 2, 4)
    assert not b.can_move(elephant1, (2, 4))  # Blocked by the governator

    assert b.can_move(elephant1, (2, 0))
    b.make_move(2, 1, 1, 1)  # A cannon moves to block the elephant's move
    assert not b.can_move(elephant1, (2, 0))

    elephant2 = Piece('E', 9, 6, 1)  # Player 2
    b.make_move(7, 1, 8, 1)  # A cannon moves to block the elephant's move
    assert not b.can_move(elephant2, (7, 0))

    ### ROOKS ###
    rook1 = Piece('R', 0, 0, 0)  # Player 1
    assert not b.can_move(rook1, (3, 0))  # Own piece already there
    assert not b.can_move(rook1, (6, 0))  # Cannot take the piece, a soldier is in between
    b.make_move(3, 0, 3, 1)  # Move the soldier out of the way
    assert b.can_move(rook1, (6, 0))  # Can take the other player's soldier
    b.make_move(3, 1, 3, 0)  # For the sake of correctness, move the soldier back

    rook2 = Piece('R', 9, 8, 1)  # Player 2
    assert not b.can_move(rook2, (9, 7))  # Own piece already there
    assert b.can_move(rook2, (8, 8))
    b.make_move(9, 8, 8, 8)
    rook2.x, rook2.y = 8, 8
    assert not b.can_move(rook2, (8, 4))  # Own piece already there
    assert not b.can_move(rook2, (8, 0))  # Own piece in between
    assert b.can_move(rook2, (8, 5))

    ### CANNONS ###
    cannon1 = Piece('C', 1, 1, 0)  # Player 1
    assert not b.can_move(cannon1, (8, 1))  # No pieces in between
    assert b.can_move(cannon1, (9, 1))  # Exactly one piece in between

    cannon2 = Piece('C', 8, 1, 1)  # Player 2
    assert not b.can_move(cannon2, (1, 1))  # No pieces in between
    assert b.can_move(cannon2, (0, 1))  # Exactly one piece in between

    ### LINE OF SIGHT ###
    # Let's cheat and move pieces out of the way
    b.make_move(5, 4, 5, 3)
    b.make_move(6, 4, 6, 3)
    advisor4 = Piece('A', 8, 4, 1)
    assert not b.can_move(advisor4, (7, 3))  # Advisor must block the line of sight

    ### KING NOT IN DANGER ###
    # Let's cheat some more and move a S1 in front of G1 in addition to A1
    b.make_move(5, 3, 5, 4)
    # and the G0 out of the way and C0 to its place
    b.make_move(2, 4, 1, 4)
    b.make_move(2, 7, 2, 4)
    assert not b.can_move(advisor4, (7, 3))  # Advisor must stay as a second piece between G1 and CO
    # We'll move R1 beside G0 and an H0 between them
    b.make_move(8, 8, 1, 8)
    b.make_move(0, 7, 1, 5)
    horse3 = Piece('H', 1, 5, 0)
    assert not b.can_move(horse3, (3, 4))

    # Let's put an additional S1 between them
    b.make_move(5, 6, 1, 6)
    assert b.can_move(horse3, (3, 4))

    print("Passed: can_move!")


def test_get_protectors():
    str_board = """
R0|  |E0|A0|G0|A0|E0|R0|
  |  |  |H0|  |  |  |  |
C0|  |  |H0|  |C0|  |  |
  |  |  |C1|  |  |  |  |
  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |
S1|  |S1|  |S1|  |S1|  |S1
C1|  |S0|  |  |  |  |  | 
  |S0|  |  |  |  |  |  |
R1|H1|E1|A1|G1|A1|E1|H1|R1
"""
    b = Board(str_board)
    protectors_pl1 = b.get_protectors(0)
    assert protectors_pl1.keys() == {Piece('C', 7, 0, 1),  # Protects R0 and C0
                                     Piece('C', 2, 0, 0),  # Protects R0
                                     Piece('S', 6, 0, 1),  # Protects R0 and C0
                                     Piece('S', 8, 1, 0),  # Protects S0
                                     Piece('H', 1, 3, 0),  # Protects A0
                                     Piece('H', 2, 3, 0)}  # Protects A0

    assert protectors_pl1[Piece('C', 7, 0, 1)] == {Piece('R', 0, 0, 0), Piece('C', 2, 0, 0)}
    assert protectors_pl1[Piece('S', 6, 0, 1)] == {Piece('R', 0, 0, 0), Piece('C', 2, 0, 0)}
    assert protectors_pl1[Piece('C', 2, 0, 0)] == {Piece('R', 0, 0, 0)}

    print("Passed: get_protectors!")


test_init_default()
test_init_custom()
test_make_move()
test_get_all_moves()
test_can_move()
test_get_protectors()
