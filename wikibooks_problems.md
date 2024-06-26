# Problems from 'WikiBooks' for the AQA Computer Science skeleton code 2024:

# Implemented

- [X]  Question 1 - Symbol Case
- [X]  Question 2 - Game file not existing
- [X]  Question 3 - Blow up a block (blocked cell)
- [X]  Question 4 - Add additional symbols/letters
- [X]  Question 5 - Save current game (status)
- [ ]  Question 6 - Rotated letter/symbol
- [ ]  Question 7 - Game difficulty setting
- [ ]  Question 8 - Fix symbols placed error
- [ ]  Question 9 - Create a new puzzle file to be imported
- [ ]  Question 10 - Be able to undo a move
- [ ]  Question 11 - Validation of Row and Column entries
- [ ]  Question 12 - Fix the GetCell mapping issue
- [ ]  Question 13 - Why is UpdateCell() empty and never called?
- [ ]  Question 14 - Implement a wildcard *
- [ ]  Question 15 - Program allows the user to replace already placed symbols
- [ ]  Question 16 - Program allows the user to create their own patterns and symbols
- [ ]  Question 17 - Making a difficulty rating program
- [ ]  Question 18

## Question 1 - Symbol Case

Lower case symbols are not accepted. E.g. if you enter 'q' it is not recognised as 'Q'. Fix this.

```python
    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ").upper()
        return Symbol
```

## Question 2 - Game file not existing

If a filename is entered that does not exist, the game is unplayable (infinite loop). Amend the program so that in this
case the default game is played, with a suitable message to indicate this.

```python
        except:
            print("Invalid puzzle provided, loading empty puzzle instead.")
            self.__dict__ = Puzzle(8, int(8 * 8 * 0.6)).__dict__
```

## Question 3 - Blow up a block (blocked cell)

Have a 'bomb' that can remove or 'blow-up' a block in a 'blocked cell', but costs you some of your score (minus some points)


```python
class Cell():
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = ["B"]
```

```python
Puzzle.AttemptPuzzle()
            if CurrentCell.CheckSymbolAllowed(Symbol):
                if Symbol == "B":  # If it's a bomb:
                    Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
                    self.__Grid[Index] = Cell()
                    self.__Score -= 3

                else:  # If not a bomb, do normal
                    CurrentCell.ChangeSymbolInCell(Symbol)

```

```python
Puzzle.__init__()
            self.__AllowedSymbols = []

            self.__AllowedSymbols.append("B")  # Bomb

            QPattern = Pattern("Q", "QQ**Q**QQ")
```

## Question 4 - Add additional symbols/letters

Add additional letters/symbols e.g. L or O or U or V or C or H or I.


```python
Puzzle.__init__()
            # Custom
            LPattern = Pattern("L", "L****LLL*")
            self.__AllowedPatterns.append(LPattern)
            self.__AllowedSymbols.append("L")

            OPattern = Pattern("O", "OOOOOOOO*")
            self.__AllowedPatterns.append(OPattern)
            self.__AllowedSymbols.append("O")
```

## Question 5 - Save current game (status)

Save the current status of the game (file-handling)/writing to a text file.

```python
    def __SavePuzzle(self, Filename):
        try:
            with open(Filename, "wt") as f:
                NoOfSymbols = str(len(self.__AllowedSymbols))
                f.write(NoOfSymbols + "\n")
                Symbols = self.__AllowedSymbols
                for Symbol in Symbols:
                    f.write(str(Symbol) + "\n")

                NoOfPatterns = str(len(self.__AllowedPatterns))
                f.write(NoOfPatterns + "\n")
                for Pattern in self.__AllowedPatterns:
                     f.write(f"{Pattern.GetSymbol()},{Pattern.GetPatternSequence()}" + "\n")

                f.write(str(self.__GridSize))
                for GridCell in self.__Grid:
                    f.write(f"{GridCell.GetSymbol() if GridCell.GetSymbol() != '-' else ''},{GridCell.GetBannedSymbols()}" + "\n")

                f.write(str(self.__Score) + "\n")
                f.write(str(self.__SymbolsLeft) + "\n")
        except Exception as e:
            print(e)
```

## Question 6 - Rotated letter/symbol

Score a 'rotated' symbol/letter (lower score?)

## Question 7 - Game difficulty setting

Offer 'game difficulty' setting to change level of game (with greater number of blocked cells = 'more difficult')

## Question 8 - Fix symbols placed error

When you try place a symbol in a invalid cell it still counts as a placed cell towards the amount of symbols placed.

## Question 9 - Create a new puzzle file to be imported

Create a new puzzle file to be imported into the code for the user to play:

## Question 10 - Be able to undo a move

Alter the attemptPuzzle subroutine such that the user is asked if they wish to undo their last move prior to the place
in the loop where there is a check for symbolsLeft being equal to zero. Warn them that this will lose them 3 points.

If the player chooses to undo:

a. revert the grid back to its original state

b. ensure symbolsLeft has the correct value

c. ensure score reverts to its original value minus the 3 point undo penalty

d. ensure any changes made to a cell’s symbolsNotAllowed list are undone as required

## Question 11 - Validation of Row and Column entries

Description of problem: Validate row and column number entries to only allow numbers within the grid size.

## Question 12 - Fix the GetCell mapping issue

Description of problem: subroutine getCell in the Puzzle class allows for invalid column numbers in some cases, as the
algorithm will incorrectly map to a cell that exists in the grid. This should not happen as there could be a time when a
pattern matches in checkForMatchWithPattern that doesn't really exist or a cell's 'not-allowed' symbol list will be set
wrongly.

## Question 13 - Why is UpdateCell() empty and never called?

Description of problem: Currently, the UpdateCell() method contains 'pass' and is not called anywhere in the program.
This will almost certainly be a ## Question, otherwise why would they include it? This may relate to the bombing idea
where a Blocked Cell is bombed, and the UpdateCell() is then called to modify this Blocked Cell into a normal cell.
Please suggest other ideas of what this method could be used for.

UpdateCell() could be used for unlocking a 3*3 grid if a pattern is broken allowing you to replace the symbol. This
would also need to decrease the score after the pattern is broken.

## Question 14 - Implement a wildcard *

Implement a special character * which is a wildcard. The wildcard can be used to represent any character so that
multiple matches can be made with the same cell. Give the player 3 wildcards in random positions at the start of the
game.

a) Alter the standard Puzzle constructor (not the load game one) to call ChangeSymbolInCell for 3 random cells, passing
in * as the new symbol. Note that blocked cells cannot be changed to wildcard ones so you need to add code to ensure the
randomly selected cell is not a blocked cell.

b) In class Cell alter the method. ChangeSymbolInCell such that wildcard cells will never have their symbol changed
from * once set. In the same class, alter method CheckSymbolAllowed such that wildcard cells always return true.

c) Alter method MatchesPattern in class Pattern to allow correct operation for the new wildcard *

d) Test that a wildcard can successfully match within two different patterns

## Question 15 - Program allows the user to replace already placed symbols

the user can replace already placed symbols, and patterns, and not lose points (can fix either by stopping them
replacing, or make them lose the points from the pattern the replaced):

## Question 16 - Program allows the user to create their own patterns and symbols

Description of problem:

1) requesting users to create their own symbols
2) requesting for the pattern associate with the symbol
3) output an empty grid for user, so user can input any coordinates hence, to create their own pattern
4) make sure new symbols and pattern can be verified by the program

EDIT: this would involve changing a text file or creating a new text file - AQA has never told students to do anything
text file-based

## Question 17- Making a difficulty rating program

Description of problem:

1) this program can save each game in record including their score, number of symbol left, time to complete and the
   original empty grid
2) using these information to make a difficulty rating board, so user can see their rating and select the one they want
   to play

## Question 18

This question refers to the class Puzzle. A new option of a wildcard is to be added to the game.
When the player uses this option, they are given the opportunity to complete a pattern by overriding existing symbols to
make that
pattern. The wildcard can only be used once in a game.

Task 1:

Add a new option for the user that will appear before each turn. The user should be asked "Do you want to use your
wildcard (Y/N)" If the user responds with "Y" then the Row, Column and Symbol will be taken as normal but then the new
method ApplyWildcard should be called and the prompt for using the wildcard should no longer be shown in subsequent
turns. If the user responds with "N" then the puzzle continues as normal.

Task 2:

Create a new method called ApplyWildcard that will take the Row, Column and Symbol as parameters and do the following:

1. Determine if the pattern can be completed in a 3x3 given the Row, Column and Symbol passed to it.

a) If the pattern can be made the cells in the pattern should be updated using the method UpdateCell() in the Cell class
and 5 points added for move.

b) If the pattern cannot be made the user should be given the message "Sorry, the wildcard does not work for this cell –
you have no wildcards left"
