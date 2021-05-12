from JanggiGame import JanggiGame

game = JanggiGame()

while game.get_game_state() == 'UNFINISHED':
    game.print_board()
    print("Current turn:", game.get_current_color())
    start = input("Move from: ")
    end = input("Move to: ")
    move = game.make_move(start, end)
    if not move:
        print("Invalid move, please try again.")
    if game.get_game_state() != 'UNFINISHED':
        print(game.get_game_state())
        print("Game over. Thanks for playing!")