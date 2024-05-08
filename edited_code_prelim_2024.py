#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9.4 programming environment

import random


def main():
    again = "y"
    while again == "y":
        filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(filename) > 0:
            my_puzzle = Puzzle(filename + ".txt")
        else:
            my_puzzle = Puzzle(8, int(8 * 8 * 0.6))
        score = my_puzzle.attempt_puzzle()
        print("Puzzle finished. Your score was: " + str(score))
        again = input("Do another puzzle? ").lower()


class Puzzle:
    def __init__(self, *args):
        if len(args) == 1:
            self.__score = 0
            self.__symbols_left = 0
            self.__grid_size = 0
            self.__grid = []
            self.__allowed_patterns = []
            self.__allowed_symbols = []
            self.__load_puzzle(args[0])
        else:
            self.__score = 0
            self.__symbols_left = args[1]
            self.__grid_size = args[0]
            self.__grid = []
            for count in range(1, self.__grid_size * self.__grid_size + 1):
                if random.randrange(1, 101) < 90:
                    cell = Cell()
                else:
                    cell = BlockedCell()
                self.__grid.append(cell)
            self.__allowed_patterns = []
            self.__allowed_symbols = []

            self.__allowed_symbols.append("B")  # Bomb

            q_pattern = Pattern("Q", "QQ**Q**QQ")
            self.__allowed_patterns.append(q_pattern)
            self.__allowed_symbols.append("Q")
            x_pattern = Pattern("X", "X*X*X*X*X")
            self.__allowed_patterns.append(x_pattern)
            self.__allowed_symbols.append("X")
            t_pattern = Pattern("T", "TTT**T**T")
            self.__allowed_patterns.append(t_pattern)
            self.__allowed_symbols.append("T")

            # Custom
            l_pattern = Pattern("L", "L****LLL*")
            self.__allowed_patterns.append(l_pattern)
            self.__allowed_symbols.append("L")

            o_pattern = Pattern("O", "OOOOOOOO*")
            self.__allowed_patterns.append(o_pattern)
            self.__allowed_symbols.append("O")

    def __save_puzzle(self, filename):
        try:
            with open(filename, "wt") as f:
                no_of_symbols = str(len(self.__allowed_symbols))
                f.write(no_of_symbols + "\n")
                symbols = self.__allowed_symbols
                for symbol in symbols:
                    f.write(str(symbol) + "\n")

                no_of_patterns = str(len(self.__allowed_patterns))
                f.write(no_of_patterns + "\n")
                for pattern in self.__allowed_patterns:
                    f.write(f"{pattern.get_symbol()},{pattern.get_pattern_sequence()}" + "\n")

                f.write(str(self.__grid_size))
                for grid_cell in self.__grid:
                    f.write(
                        f"{grid_cell.get_symbol() if grid_cell.get_symbol() != '-' else ''},{grid_cell.get_banned_symbols()}" + "\n")

                f.write(str(self.__score) + "\n")
                f.write(str(self.__symbols_left) + "\n")
        except Exception as e:
            print(e)

    def __load_puzzle(self, filename):
        try:
            with open(filename) as f:
                no_of_symbols = int(f.readline().rstrip())
                for count in range(1, no_of_symbols + 1):
                    self.__allowed_symbols.append(f.readline().rstrip())
                no_of_patterns = int(f.readline().rstrip())
                for count in range(1, no_of_patterns + 1):
                    items = f.readline().rstrip().split(",")
                    pattern = Pattern(items[0], items[1])
                    self.__allowed_patterns.append(pattern)
                self.__grid_size = int(f.readline().rstrip())
                for count in range(1, self.__grid_size * self.__grid_size + 1):
                    items = f.readline().rstrip().split(",")
                    if items[0] == "@":
                        cell = BlockedCell()
                        self.__grid.append(cell)
                    else:
                        cell = Cell()
                        cell.change_symbol_in_cell(items[0])
                        for current_symbol in range(1, len(items)):
                            cell.add_to_not_allowed_symbols(items[current_symbol])
                        self.__grid.append(cell)
                self.__score = int(f.readline().rstrip())
                self.__symbols_left = int(f.readline().rstrip())
        except Exception as e:
            print(e)
            print("Invalid puzzle provided, loading empty puzzle instead.")
            self.__dict__ = Puzzle(8, int(8 * 8 * 0.6)).__dict__  # This is so scuffed but it works :D

    def attempt_puzzle(self):
        finished = False
        while not finished:
            self.display_puzzle()
            print("Current score: " + str(self.__score))
            row = -1
            valid = False
            while not valid:
                try:
                    row = input("Enter row number (\"S\" to save game): ")
                    if row == "S":
                        filename = input("File to save to (.txt):") + ".txt"
                        print("Saving game...")
                        self.__save_puzzle(filename)
                    else:
                        row = int(row)
                    valid = True
                except Exception as e:
                    print(e)
            column = -1
            valid = False
            while not valid:
                try:
                    column = int(input("Enter column number: "))
                    valid = True
                except:
                    pass
            symbol = self.__get_symbol_from_user()
            self.__symbols_left -= 1
            current_cell = self.__get_cell(row, column)

            if current_cell.CheckSymbolAllowed(symbol):
                if symbol == "B":  # If it's a bomb:
                    index = (self.__grid_size - row) * self.__grid_size + column - 1
                    self.__grid[index] = Cell()
                    self.__score -= 3

                else:  # If not a bomb, do normal
                    current_cell.change_symbol_in_cell(symbol)

                amount_to_add_to_score = self.check_for_match_with_pattern(row, column)
                if amount_to_add_to_score > 0:
                    self.__score += amount_to_add_to_score
            if self.__symbols_left == 0:
                finished = True
        print()
        self.display_puzzle()
        print()
        return self.__score

    def __get_cell(self, row, column):
        index = (self.__grid_size - row) * self.__grid_size + column - 1
        if index >= 0:
            return self.__grid[index]
        else:
            raise IndexError()

    @staticmethod
    def __rotate_pattern_ccw(to_be_rotated):
        # ONLY WORKS FOR 3X3 PATTERNS

        PatternSeq = [i for i in to_be_rotated.get_pattern_sequence()]
        # indices: 0,1,2,5,8,7,6,3,4 -> 2,5,8,7,6,3,0,1,4
        #
        # 0 1 2    2 5 8
        # 3 4 5 -> 1 4 7 (Spiral from top left)
        # 6 7 8    0 3 6
        #
        OriginalIndices = [0, 1, 2, 5, 8, 7, 6, 3, 4]
        RotatedIndices = [2, 5, 8, 7, 6, 3, 0, 1, 4]
        RotatedSeq = ["-" for i in range(9)]

        for i in range(len(OriginalIndices)):
            RotatedSeq[RotatedIndices[i]] = PatternSeq[OriginalIndices[i]]
        ret = Pattern(to_be_rotated.get_symbol(), "".join(RotatedSeq))
        print(to_be_rotated.get_pattern_sequence(), ret.get_pattern_sequence())
        return ret

    def check_for_match_with_pattern(self, row, column):
        for start_row in range(row + 2, row - 1, -1):
            for start_column in range(column - 2, column + 1):
                try:
                    pattern_string = ""
                    pattern_string += self.__get_cell(start_row, start_column).get_symbol()
                    pattern_string += self.__get_cell(start_row, start_column + 1).get_symbol()
                    pattern_string += self.__get_cell(start_row, start_column + 2).get_symbol()
                    pattern_string += self.__get_cell(start_row - 1, start_column + 2).get_symbol()
                    pattern_string += self.__get_cell(start_row - 2, start_column + 2).get_symbol()
                    pattern_string += self.__get_cell(start_row - 2, start_column + 1).get_symbol()
                    pattern_string += self.__get_cell(start_row - 2, start_column).get_symbol()
                    pattern_string += self.__get_cell(start_row - 1, start_column).get_symbol()
                    pattern_string += self.__get_cell(start_row - 1, start_column + 1).get_symbol()
                    for P in self.__allowed_patterns:
                        CurrentSymbol = self.__get_cell(row, column).get_symbol()
                        if P.matches_pattern(pattern_string, CurrentSymbol):
                            self.__get_cell(start_row, start_column).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row, start_column + 1).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row, start_column + 2).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row - 1, start_column + 2).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row - 2, start_column + 2).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row - 2, start_column + 1).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row - 2, start_column).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row - 1, start_column).add_to_not_allowed_symbols(CurrentSymbol)
                            self.__get_cell(start_row - 1, start_column + 1).add_to_not_allowed_symbols(CurrentSymbol)
                            return 10

                    # Check rotated after normal checks
                    for P in self.__allowed_patterns:
                        rotated = self.__rotate_pattern_ccw(P)
                        while rotated.get_pattern_sequence() != P.get_pattern_sequence():
                            CurrentSymbol = self.__get_cell(row, column).get_symbol()
                            if rotated.matches_pattern(pattern_string, CurrentSymbol):
                                self.__get_cell(start_row, start_column).add_to_not_allowed_symbols(CurrentSymbol)
                                self.__get_cell(start_row, start_column + 1).add_to_not_allowed_symbols(CurrentSymbol)
                                self.__get_cell(start_row, start_column + 2).add_to_not_allowed_symbols(CurrentSymbol)
                                self.__get_cell(start_row - 1, start_column + 2).add_to_not_allowed_symbols(
                                    CurrentSymbol)
                                self.__get_cell(start_row - 2, start_column + 2).add_to_not_allowed_symbols(
                                    CurrentSymbol)
                                self.__get_cell(start_row - 2, start_column + 1).add_to_not_allowed_symbols(
                                    CurrentSymbol)
                                self.__get_cell(start_row - 2, start_column).add_to_not_allowed_symbols(CurrentSymbol)
                                self.__get_cell(start_row - 1, start_column).add_to_not_allowed_symbols(CurrentSymbol)
                                self.__get_cell(start_row - 1, start_column + 1).add_to_not_allowed_symbols(
                                    CurrentSymbol)
                                return 5  ## Reduced because rotated match.
                            rotated = self.__rotate_pattern_ccw(rotated)

                except Exception as e:
                    print(e)
        return 0

    def __get_symbol_from_user(self):
        symbol = ""
        while symbol not in self.__allowed_symbols:
            symbol = input("Enter symbol: ").upper()
        return symbol

    def __create_horizontal_line(self):
        line = "  "
        for count in range(1, self.__grid_size * 2 + 2):
            line = line + "-"
        return line

    def display_puzzle(self):
        print()
        if self.__grid_size < 10:
            print("  ", end='')
            for count in range(1, self.__grid_size + 1):
                print(" " + str(count), end='')
        print()
        print(self.__create_horizontal_line())
        for count in range(0, len(self.__grid)):
            if count % self.__grid_size == 0 and self.__grid_size < 10:
                print(str(self.__grid_size - ((count + 1) // self.__grid_size)) + " ", end='')
            print("|" + self.__grid[count].get_symbol(), end='')
            if (count + 1) % self.__grid_size == 0:
                print("|")
                print(self.__create_horizontal_line())


class Pattern:
    def __init__(self, symbol_to_use, pattern_string):
        self.__symbol = symbol_to_use
        self.__pattern_sequence = pattern_string

    def matches_pattern(self, pattern_string, symbol_placed):
        if symbol_placed != self.__symbol:
            return False
        print("len", len(self.__pattern_sequence))
        for count in range(0, len(self.__pattern_sequence)):
            try:
                if self.__pattern_sequence[count] == self.__symbol and pattern_string[count] != self.__symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def get_pattern_sequence(self):
        return self.__pattern_sequence

    def get_symbol(self):
        return self.__symbol


class Cell:
    def __init__(self):
        self._symbol = ""
        self.__symbols_not_allowed = ["B"]

    def get_banned_symbols(self):
        res = ""
        for symbol in self.__symbols_not_allowed:
            res += symbol
        return res

    def get_symbol(self):
        if self.is_empty():
            return "-"
        else:
            return self._symbol

    def is_empty(self):
        if len(self._symbol) == 0:
            return True
        else:
            return False

    def change_symbol_in_cell(self, new_symbol):
        self._symbol = new_symbol

    def CheckSymbolAllowed(self, symbol_to_check):
        for Item in self.__symbols_not_allowed:
            if Item == symbol_to_check:
                return False
        return True

    def add_to_not_allowed_symbols(self, symbol_to_add):
        self.__symbols_not_allowed.append(symbol_to_add)

    def update_cell(self):
        pass


class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, symbol_to_check):
        return symbol_to_check == "B"


if __name__ == "__main__":
    main()
