import random
import json
import time


class Bear:
    lines = {
        "corner": "+",
        "vert": "|",
        "line": "-"
    }

    def __init__(self):
        self.map = self.get_map()
        self.inv = {}
        self.gold = 0

    @staticmethod
    def get_map() -> str:
        """
        Provides map from the text file to the instance of the class
        :return: String representation of the map
        """
        final = ""
        with open("map.txt") as f:
            for line in f:
                final += line
        return final

    def show_map(self) -> None:
        """
        Prints map
        :return: None
        """
        print(self.map)

    def change_map(self, pos: int, char: str) -> None:
        """
        Changes a character on the map
        :param pos: New position for the provided character
        :param char: The character you want use to replace
        :return: None
        """
        map_list = list(self.map)
        map_list[pos] = char
        self.map = "".join(map_list)

    def end_map(self) -> None:
        """
        Prints end map animation
        :return: None
        """
        for i in enumerate(self.map):
            map_list = list(self.map)
            map_list[i[0]] = "#" if i[1] != "\n" else i[1]
            self.map = "".join(map_list)
            print(self.map)
            print("\n" * 7)
            time.sleep(0.01)

    def show_inv(self) -> None:
        """
        Prints inventory showing the contents
        :return: None
        """
        inv = self.inv
        inv["gold"] = self.gold
        items = [" x".join((k, str(v))) for k, v in list(zip(inv.keys(), inv.values()))]
        line = "+"
        mid = "|"
        for item in items:
            line += ("-" * len(item)) + "+"
            mid += item + "|"
        print(line)
        print(mid)
        print(line)

    def add_inv(self, obj: str) -> None:
        """
        Adds an object to the inventory
        :param obj: The object to be added to the inventory
        :return: None
        """
        try:
            self.inv[obj] += 1
        except KeyError:
            self.inv[obj] = 1

    @staticmethod
    def hangman() -> bool:
        """
        Hangman challenge game
        :return: True if you win, False if not
        """
        words = ["computer science", "bear game", "hangman"]
        rand_word = random.choice(words)

        def space_or_line(char):
            if char == " ":
                return " "
            else:
                return "_"

        word = list(rand_word)
        guessed = [space_or_line(i) for i in word]
        letters = []
        lives = 5
        while lives != 0:
            print(" ".join(guessed))
            if "_" in guessed:
                user_letter = input("Enter the letter: ")[:1]
                if user_letter not in letters:
                    if user_letter in word:
                        for pos, let in enumerate(word):
                            if let == user_letter:
                                guessed[pos] = let
                    else:
                        print(f"{user_letter} is not in the word")
                        lives -= 1
                else:
                    print(f"You have already entered that letter {user_letter}")

                letters.append(user_letter)
            else:
                print(f"You have won with {lives} lives left")
                return True

        if lives == 0:
            print(f"\nYou lost with {lives} lives left\nThe word/phrase was {''.join(word)}")
            return False

    @staticmethod
    def tic_tac_toe() -> bool:
        """
        Tic tac toe challenge game
        :return: True if you win, False if not
        """
        game = TicTacToe()
        playing = True
        print("Coords are 1-3")
        while playing:
            try:
                place = int(input("Enter X coord: ")) - 1, int(input("Enter Y coord: ")) - 1
                print("--Players insert--")
                finish = game.insert_piece(place, game.p1)
                if not finish[0]:
                    playing = finish[0]
                else:
                    print("--Computer insert")
                    game.computer_insert()
            except ValueError:
                print("Make sure you enter a number")
                continue

        return True

    @staticmethod
    def hex_to_denary(hex_str: str) -> int:
        """
        Converts hexidecimal to decimal, used as a challenge
        :param hex_str: Hexidecimal string you want to convert
        :return: Decimal total
        """
        hex_dict = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
        hex_str = list(hex_str)
        col = len(hex_str) - 1
        multiplier = 16 ** col
        total = 0
        for num in hex_str:
            try:
                num = int(num)
                total += multiplier * num
            except ValueError:
                num = hex_dict[num]
                total += multiplier * num
            col -= 1
            multiplier = 16 ** col

        return total

    def hex_to_binary(self, hex_str: str) -> str:
        """
        Converts hexidecimal to binary, used as a challenge
        :param hex_str: Hexidecimal string you want to convert
        :return: Binary total
        """
        denary = self.hex_to_denary(hex_str)
        cols = sorted([2 ** i for i in range(8)], reverse=True)
        binary = []
        for num in cols:
            if denary - num >= 0:
                binary.append("1")
                denary -= num
            else:
                binary.append("0")

        return "".join(binary)

    @staticmethod
    def bin_to_dec(num: str) -> int:
        """
        Converts binary to decimal, used as a challenge
        :param num: Binary string to convert to decimal
        :return: Decimal total
        """
        col = len(num.split(".")[0]) - 1
        multiplier, total, num = 2 ** col, 0, num.replace(".", "")
        for dec in num:
            total += multiplier if dec == "1" else 0
            col -= 1
            multiplier = 2 ** col
        return total

    def random_event(self) -> bool:
        """
        Called after each move to initiate random event
        :return: true if survived, false if not
        """
        chance = random.randint(1, 10)
        if chance == 10:
            print("-----Random Event-----")
            print("You a snake appears out of nowhere")
            print("You can use your [h]ands, [g]un, [p]ickaxe, [r]ope, [f]lare or [m]onkey to save yourself")
            choice = input(">>> ")
            if choice[0].lower() == "g" and "gun" in self.inv:
                del self.inv["gun"]
                print("You used the gun to save yourself")
                return True
            elif choice[0].lower() == "p" and "pickaxe" in self.inv:
                del self.inv["pickaxe"]
                print("You used the pickaxe to save yourself")
                return True
            elif choice[0].lower() == "r" and "rope" in self.inv:
                del self.inv["rope"]
                print("You used the rope to save yourself")
                return True
            elif choice[0].lower() == "f" and "flare" in self.inv:
                del self.inv["flare"]
                print("You used the flare to save yourself")
                return True
            elif choice[0].lower() == "m" and "monkey" in self.inv:
                del self.inv["monkey"]
                print("You used the monkey to save yourself")
                return True
            else:
                chance_2 = random.randint(1, 2)
                if chance_2 == 2:
                    return False
                else:
                    print("You fought off the snake with your hands and survived")
                    return True

    def dead(self, reason: str) -> None:
        """
        Prints the the players contents and the reason they died
        :param reason: The reason the player died
        :return: None
        """
        print("-----You Died-----")
        print(f"You died because {reason}")
        print("Inventory: ")
        self.show_inv()
        print(self.map)


class TicTacToe:
    def __init__(self):
        self.board = self.create_board()
        self.p1 = self.get_char()
        self.p2 = "O" if self.p1 == "X" else "X"

    @staticmethod
    def get_char() -> str:
        """
        Chooses what character player 1 will have
        :return: The character for player 1
        """
        check = True
        while check:
            char = input("Do you want to be X or O: ")
            if char[0].upper() in ["X", "O"]:
                return char[0].upper()
            else:
                continue

    @staticmethod
    def create_board() -> list:
        """
        Creates tic tac toe board
        :return: tic tac toe board
        """
        return [["_", "_", "_"] for i in range(3)]

    def show_board(self) -> str:
        """
        Concatenates board list
        :return: String representation of the board
        """
        return "\n".join([" ".join(i) for i in self.board])

    def check_solve(self, piece: str) -> tuple:
        """
        Checks to see if anyone won through checking each possible direction
        :param piece: Character of the player on the board
        :return: Tuple of whether someone won, the way they won and the character
        """
        for line in self.board:
            if line == [piece, piece, piece]:
                return True, "Horizontal", piece

        for pos in range(3):
            if [self.board[0][pos], self.board[1][pos], self.board[2][pos]] == [piece, piece, piece]:
                return True, "Vertical", piece

        pattern_1 = []
        pattern_2 = []
        x = 2
        for i in range(3):
            pattern_1.append(self.board[i][i])
            pattern_2.append(self.board[i][x])
            x -= 1

        if pattern_1 == [piece, piece, piece] or pattern_2 == [piece, piece, piece]:
            return True, "Diagonal", piece

        return False, "No solve", piece

    def insert_piece(self, coord: tuple, piece: str) -> tuple:
        """
        Insters the players character on the board
        :param coord: The (x, y) coord of where the player want to place the piece
        :param piece: The character of the player
        :return: Tuple of a boolean to determine whether the game loop is broken and why
        """
        x, y = coord
        if self.board[y][x] != "_":
            return True, "taken"
        else:
            self.board[y][x] = piece
            print(self.show_board())
            won = self.check_solve(self.p1)
            if won[0]:
                self.finish(won[2], won[1])
                return False, "won"
            else:
                return True, "not won"

    def computer_insert(self) -> None:
        """
        Determines where the computer place its piece through randomly generated positions
        :return: None
        """
        trying = True
        while trying:
            x, y = random.randint(0, 2), random.randint(0, 2)
            place = self.insert_piece((x, y), self.p2)
            if place[1] == "not won" or place[1] == "won":
                trying = False
            elif place[1] == "taken":
                continue

    @staticmethod
    def finish(winner: str, reason: str) -> None:
        """
        Prints who and why the person won
        :param winner: Winning players character
        :param reason: The reason the player won
        :return: None
        """
        print(f"The winner was {winner} winning by {reason}")


def main() -> tuple:
    """
    Main function, runs game
    :return: tuple of player inventory and gold
    """
    game = Bear()
    game.change_map(344, " ")
    game.change_map(300, "^")
    game.show_map()
    game.show_inv()
    print("There is a Bear standing in the way, monkey behind it with gold\nDo you want to [a]ttack it or [r]un: ")
    choice = input(">>> ")
    if choice[0].lower() == "a":
        chance = random.randint(1, 4)
        if chance == 4:
            game.dead("you were eaten by a bear")
            return game.inv, game.gold if game.inv else None, game.gold
        else:
            print("You killed the bear and took gold from inside it\n+5 gold")
            game.gold += 5
    else:
        print("You evaded the bear but also didin't catch the monkey")

    game.change_map(300, " ")
    game.change_map(256, "^")
    game.show_map()
    game.show_inv()

    rand = game.random_event()
    if rand is False:
        game.dead("The snake bite")
        return game.inv, game.gold if game.inv else None, game.gold
    elif rand is True:
        print("+5 gold")
        game.gold += 5

    print("You have now come up to a T junction\nDo you want to go [l]eft or [r]ight: ")
    choice = input(">>> ")
    if choice[0].lower() == "l":
        game.change_map(256, " ")
        game.change_map(252, "^")
        game.show_map()
        game.show_inv()

        print("A Tribesman confronts you with a challenge,\nYou can [a]ccept the challenge or [l]eave it")
        choice = input(">>> ")
        if choice[0].lower() == "a":
            bin_num = random.choice(["11001011", "00110011", "10101010", "11001111"])
            ans = game.bin_to_dec(bin_num)
            print(f"Convert {bin_num} to decimal")
            still_int = True
            while still_int:
                try:
                    usr_ans = int(input(">>> "))
                    still_int = False
                except ValueError:
                    pass
            if usr_ans == ans:
                print("Your answer is correct\n+5 gold")
                game.gold += 5
            else:
                print(f"Your answer was incorrect, it was {ans}")
        else:
            print("If you took the challenge you could've gained 5 gold")

        game.change_map(252, " ")
        game.change_map(208, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("There is a cave ahead,\nYou can go [i]n or [a]round")
        choice = input(">>> ")
        if choice[0].lower() == "i":
            print("Inside the cave was a pickaxe, it has been added to your inventory")
            game.add_inv("pickaxe")
        else:
            chance = random.randint(1, 5)
            if chance == 5:
                game.dead("You fell down a cliff")
                return game.inv, game.gold if game.inv else None, game.gold
            else:
                print("You made it around the cave without dying")

        game.change_map(208, " ")
        game.change_map(164, "^")
        game.show_map()
        game.show_inv()

        print("There is a tribesman trader next to the path ahead\nDo you want to [t]rade or [i]gnore")
        choice = input(">>> ")
        if choice[0].lower() == "t" and game.gold > 1:
            print("You can buy things with gold, although it will decrease your score:")
            print("[r]ope: 5 gold\n[f]lare: 1 gold\nYou can only buy 1 of them")
            choice = input(">>> ")
            if choice[0].lower() == "r" and game.gold >= 5:
                game.add_inv("rope")
                game.gold -= 5
                print("You bought the rope")
            elif choice[0].lower() == "r" and game.gold < 5:
                print("You don't have enough gold")
            if choice[0].lower() == "f" and game.gold >= 1:
                game.add_inv("flare")
                game.gold -= 1
                print("You bought the flare")
            elif choice[0].lower() == "f" and game.gold < 1:
                print("You don't have enough gold")

        game.change_map(164, " ")
        game.change_map(160, "^")
        game.show_map()
        game.show_inv()

        print("There is a ravine infront of you with a tree trunk across it acting as a bridge")
        print("You can walk [a]cross it or use [r]ope if you have it")
        choice = input(">>> ")
        if choice[0].lower() == "a":
            chance = random.randint(1, 3)
            if chance == 3:
                if "pickaxe" in game.inv:
                    print("You fell off the tree but as you have a pickaxe you can dig your way out")
                    del game.inv["pickaxe"]
                else:
                    game.dead("You fell off the tree down the ravine")
                    return game.inv, game.gold if game.inv else None, game.gold
            else:
                game.gold += 2
                print("You made it across the tree without dying and some gold\n+2 gold")
        if choice[0].lower() == "r" and "rope" in game.inv:
            del game.inv["rope"]
            print("You used the rope to get across the tree, guaranteeing your survival")

        game.change_map(160, " ")
        game.change_map(156, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("A Tribesman confronts you with a challenge,\nYou can [a]ccept the challenge or [l]eave it")
        choice = input(">>> ")
        if choice[0].lower() == "a":
            hex_num = random.choice(["F1", "4A", "3B"])
            bin_str = game.hex_to_binary(hex_num)
            print(f"Convert {hex_num} to binary:")
            answer = input(">>> ")
            if bin_str == answer:
                print("You answered the question correctly\n+5 gold")
                game.gold += 5
            else:
                print(f"You answered incorrectly, the answer was {bin_str}")
        else:
            print("You could've gained 5 gold if you took the challenge")

        game.change_map(156, " ")
        game.change_map(112, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("There is a treasure chest infront of you\nDo you want to [l]oot or [w]alk away")
        choice = input(">>> ")
        if choice[0].lower() == "l":
            chance = random.randint(1, 2)
            if chance == 2:
                game.dead("The treasure chest exploded")
                return game.inv, game.gold if game.inv else None, game.gold
            else:
                game.gold += 10
                print("You looted the treasure chest and found some gold\n+10 gold ")
        else:
            print("If you looted the chest you could've taken 10 gold")

        game.change_map(112, " ")

    else:
        game.change_map(256, " ")
        game.change_map(260, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("A Tribesman confronts you with a challenge\nYou can [a]ccept the challenge or [l]eave it")
        choice = input(">>> ")
        if choice[0].lower() == "a":
            live = game.hangman()
            if live:
                game.gold += 5
                print("You gained some gold from the challenge\n+5 gold")
        else:
            print("If you took the challenge you could've gained 5 gold")

        game.change_map(260, " ")
        game.change_map(216, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("There is a cliff ahead of you with a pool at the bottom\nYou can [j]ump into the pool or [h]ike down")
        choice = input(">>> ")
        if choice[0].lower() == "j":
            chance = random.randint(1, 2)
            if chance == 2:
                game.dead("You hit rock at the bottom of the pool")
                return game.inv, game.gold if game.inv else None, game.gold
            else:
                print("You dived in to the water and found some gold at the bottom\n+5 gold")
                game.gold += 5
        else:
            chance = random.randint(1, 4)
            if chance == 4:
                game.dead("There was a landslide causing you to fall down the clif")
                return game.inv, game.gold if game.inv else None, game.gold
            else:
                print("You survived walking down the cliff")

        game.change_map(216, " ")
        game.change_map(172, "^")
        game.show_map()
        game.show_inv()

        print("There is a tribesman trader next to the path ahead\nDo you want to [t]rade or [i]gnore")
        choice = input(">>> ")
        if choice[0].lower() == "t" and game.gold > 1:
            print("You can buy things with gold, although it will decrease your score:")
            print("[g]un: 5 gold\n[f]lare: 1 gold\nYou can only buy 1 of them")
            choice = input(">>> ")
            if choice[0].lower() == "g" and game.gold >= 5:
                game.add_inv("gun")
                game.gold -= 5
                print("You bought the gun")
            elif choice[0].lower() == "g" and game.gold < 5:
                print("You don't have enough gold")
            if choice[0].lower() == "f" and game.gold >= 1:
                game.add_inv("flare")
                game.gold -= 1
                print("You bought the flare")
            elif choice[0].lower() == "f" and game.gold < 1:
                print("You don't have enough gold")

        game.change_map(172, " ")
        game.change_map(128, "^")
        game.show_map()
        game.show_inv()

        print("A Tribesman confronts you with a challenge\nYou can [a]ccept the challenge or [l]eave it")
        choice = input(">>> ")
        if choice[0].lower() == "a":
            hex_str = random.choice(["EA", "123", "4C"])
            ans = game.hex_to_denary(hex_str)
            print(f"Convert {hex_str} to decimal")
            usr_ans = int(input(">>> "))
            if usr_ans == ans:
                print("You are correct\n+5 gold")
                game.gold += 5
            else:
                print(f"Incorrect, the answer was {ans}")
        else:
            print("If you took the challenge you could've earn't 5 gold")

        game.change_map(128, " ")
        game.change_map(84, "^")
        game.show_map()
        game.show_inv()

        print("There is a treasure chest infront of you\nDo you want to [l]oot or [w]alk away")
        choice = input(">>> ")
        if choice[0].lower() == "l":
            chance = random.randint(1, 3)
            if chance == 3:
                game.dead("You were blown up by the chest")
                return game.inv, game.gold if game.inv else None, game.gold
            else:
                print("You found some gold in the chest\n+10 gold")
                game.gold += 10
        else:
            print("You could've found 10 gold in the chest")

        game.change_map(84, " ")
        game.change_map(80, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("You get ambushed by an angry tribesman\nYou can [s]hoot him if you bought a gun or [b]argin with him")
        choice = input(">>> ")
        if choice[0].lower() == "s" and "gun" in game.inv:
            print("You shoot him with the gun and loot his body, finding some gold\n+5 gold")
            del game.inv["gun"]
            game.gold += 5
        elif choice[0].lower() == "s" and "gun" not in game.inv:
            if game.gold >= 10:
                print("You don't have a gun, so you pay the tribesman 10 gold to let you go")
            else:
                print("You don't have a gun, so you pay the tribesman all of your gold to let you go")
        else:
            if game.gold >= 10:
                print("You pay the tribesman 10 gold to let you go")
            else:
                print("You pay the tribesman all of your gold to let you go")

        game.change_map(80, " ")
        game.change_map(76, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("A monkey approaches you\nDo you want to [k]ill it for gold or keep it as a[p]et")
        choice = input(">>> ")
        if choice[0].lower() == "k":
            print("You killed the monkey and took some gold from it\n+5 gold")
            game.gold += 5
        else:
            print("You keep the monkey as a pet")
            game.add_inv("monkey")

        game.change_map(76, " ")
        game.change_map(72, "^")
        game.show_map()
        game.show_inv()

        rand = game.random_event()
        if rand is False:
            game.dead("The snake bite")
            return game.inv, game.gold if game.inv else None, game.gold
        elif rand is True:
            print("+5 gold")
            game.gold += 5

        print("You fall into a sinkhole\nYour [m]onkey can help you out if ir became your pet or you can [d]ig out")
        choice = input(">>> ")
        if choice[0].lower() == "m" and "monkey" in game.inv:
            print("Your monkey helps you out of the hole but dies in the process")
            del game.inv["monkey"]
        elif choice[0].lower() == "m" and "monkey" not in game.inv:
            print("You killed the monkey")
            chance = random.randint(1, 2)
            if chance == 2:
                game.dead("You suffocated under the debris")
                return game.inv, game.gold if game.inv else None, game.gold
            else:
                print("You dug your way out of the debris without dying")
        else:
            chance = random.randint(1, 2)
            if chance == 2:
                game.dead("You suffocated under the debris")
                return game.inv, game.gold if game.inv else None, game.gold
            else:
                print("You dug your way out of the debris without dying")

        game.change_map(72, " ")

    game.change_map(68, "^")
    game.show_map()
    game.show_inv()

    print("A Tribesman confronts you with a final challenge, if you leave you die\nYou can [a]ccept the challenge or [l]eave it")
    choice = input(">>> ")
    if choice[0].lower() == "a":
        win = game.tic_tac_toe()
        if win:
            print("You won the game against the tribesman\n+10 gold")
            game.gold += 10
        else:
            print("You lost the game against the tribesman")
    else:
        game.dead("The tribesman killed you for rejecting the challenge")
        return game.inv, game.gold if game.inv else None, game.gold

    game.change_map(68, " ")
    game.change_map(24, "^")
    game.show_map()
    game.show_inv()

    print("You are now on the shore, ready to leave the island")
    print("You can use a [f]lare if you have it to attract attention or create [s]moke signals using a fire")
    choice = input(">>> ")
    if choice[0].lower() == "f" and "flare" in game.inv:
        del game.inv["flare"]
        print("A boat arrives to save you from the island")
    elif choice[0].lower() == "f" and "flare" not in game.inv or choice[0].lower() == "s":
        print("You don't have the flare, so you create smoke signals using a fire")
        chance = random.randint(1, 4)
        if chance == 4:
            print("You were saved by a boat that saw the smoke signals but you have to pay them 2 gold do escape")
            game.gold -= 2
        else:
            game.dead("You died of starvation")
            return game.inv, game.gold if game.inv else None, game.gold

    print("-----You Win-----")
    print("You escaped the island with: ")
    game.show_inv()
    time.sleep(3)
    game.end_map()


def file_handler(name: str, info: tuple) -> None:
    """
    Adds the scores of the player to the score file
    :param name: name of the player
    :param info: tuple of inventory and gold, returned by the main function
    :return: None
    """
    with open("score.json") as f:
        file = json.load(f)
    file[name] = {"inv": {**info[0]}, "gold": info[1]} if isinstance(info[0], dict) else {"inv": {}, "gold": info[1]}
    with open("score.json", "w") as f:
        json.dump(file, f, indent=4)


def leaderboard() -> None:
    """
    Prints out the leaderborad of scores
    :return: None
    """
    with open("score.json") as f:
        file = json.load(f)

    scores = sorted([(i, file[i]["gold"]) for i in file], key=lambda x: x[1], reverse=True)
    print("-----Leaderboard-----")
    for place, score in enumerate(scores):
        print(f"{place + 1}. {score[0]} = {score[1]}")


if __name__ == "__main__":
    play = True
    while play:
        info = main()
        file_handler(input("Enter you name: "), info)
        leaderboard()
        again = input("Do you want to play again\n[y]es or [n]o\n>>> ")
        if again[0].lower() == "n":
            play = False
