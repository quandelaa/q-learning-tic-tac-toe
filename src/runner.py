from board import TTTGame
from algos import TTTBot

def main():
    bot = train(1000000)

    while True:
        play(bot)

def play(bot):
    game = TTTGame()

    plr = None
    while plr not in ("X", "O"):
        plr = input("You are X/O: ")

    while True:
        show(game.state)

        winner = game.winner()
        if winner is not None:
            break

        if game.terminal():
            winner = None
            break

        cur_plr = game.player(game.state)
        print("Current:", "YOU" if cur_plr == plr else "BOT")

        changed = False

        if cur_plr == plr:
            while not changed:
                row = None
                col = None
                
                while row not in (1, 2, 3):
                    try:
                        row = int(input("What row (1-3): "))
                    except ValueError:
                        continue

                while col not in (1, 2, 3):
                    try:
                        col = int(input("What column (1-3): "))
                    except ValueError:
                        continue
                try:
                    game.result((row, col))
                    changed = True
                except ValueError:
                    print("Spot already played!")
                    continue

        else:
            board = []

            for row in game.state:
                for col in row:
                    board.append(col)

            row, col = bot.choose_action(game.state, board)
            game.result((row, col))

    if winner is not None:
        print(f"GAME OVER {winner} WON!")
    else:
        print(f"TIE!")    

def train(n):
    bot = TTTBot()

    for i in range(n):
        if (i+1)%50000 == 0:
            print(f"Training.. {i+1}")

        cur_game = TTTGame([
            ["?", "?", "?"],
            ["?", "?", "?"],
            ["?", "?", "?"],
        ])

        last = {
            "X": {"state": None, "action": None},
            "O": {"state": None, "action": None}
        }

        while True:            
            state = []

            for row in cur_game.state:
                for col in row:
                    state.append(col)

            action = bot.choose_action(cur_game.state, state, True)

            last[cur_game.player(state)]["state"] = state
            last[cur_game.player(state)]["action"] = action

            cur_game.result(action)

            new_state = []
            for row in cur_game.state:
                for col in row:
                    new_state.append(col)

            if cur_game.winner() is None:
                if cur_game.terminal():
                    bot.update(
                        last[cur_game.next_player(cur_game.player(state))]["state"],
                        last[cur_game.next_player(cur_game.player(state))]["action"],
                        new_state,
                        0
                    )

                    break
                

            if cur_game.winner() is not None:
                bot.update(state, action, new_state, 1)
                
                bot.update(        
                    last[cur_game.next_player(cur_game.player(state))]["state"],
                    last[cur_game.next_player(cur_game.player(state))]["action"],
                    new_state,
                    -1
                )

                break
                
            elif last[cur_game.next_player(cur_game.player(state))]["state"] is not None:
                bot.update(
                    last[cur_game.next_player(cur_game.player(state))]["state"],
                    last[cur_game.next_player(cur_game.player(state))]["action"],
                    new_state,
                    0
                )


    print("Done training.")
    return bot

def show(state):
    for row in state:
        for col in row:
            print(col, end=" ")

        print()

if __name__ == "__main__":
    main()
