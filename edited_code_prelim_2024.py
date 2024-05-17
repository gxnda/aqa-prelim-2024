#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

import random
import os

def Main():
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()

class Puzzle():
    def __init__(self, *args):
        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []

            self.__AllowedSymbols.append("B")  # Bomb

            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

            # Custom
            LPattern = Pattern("L", "L****LLL*")
            self.__AllowedPatterns.append(LPattern)
            self.__AllowedSymbols.append("L")

            OPattern = Pattern("O", "OOOOOOOO*")
            self.__AllowedPatterns.append(OPattern)
            self.__AllowedSymbols.append("O")

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
                


    def __LoadPuzzle(self, Filename):
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())
                for Count in range(1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                self.__GridSize = int(f.readline().rstrip())
                for Count in range(1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except Exception as e:
            print(e)
            print("Invalid puzzle provided, loading empty puzzle instead.")
            self.__dict__ = Puzzle(8, int(8 * 8 * 0.6)).__dict__  # This is so scuffed but it works :D


    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = input("Enter row number (\"S\" to save game): ")
                    if Row == "S":
                        filename = input("File to save to (.txt):") + ".txt"
                        print("Saving game...")
                        self.__SavePuzzle(filename)
                    else:
                        Row = int(Row)
                    Valid = True
                except Exception as e:
                    print(e)
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)

            if CurrentCell.CheckSymbolAllowed(Symbol):
                if Symbol == "B":  # If it's a bomb:
                    Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
                    self.__Grid[Index] = Cell()
                    self.__Score -= 3

                else:  # If not a bomb, do normal
                    CurrentCell.ChangeSymbolInCell(Symbol)

                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def __RotatePatternCCW(self, ToBeRotated):
        # ONLY WORKS FOR 3X3 PATTERNS
        
        PatternSeq = [i for i in ToBeRotated.GetPatternSequence()]
        # indices: 0,1,2,5,8,7,6,3,4 -> 2,5,8,7,6,3,0,1,4
        #
        # 0 1 2    2 5 8
        # 3 4 5 -> 1 4 7 (Spiral from top left)
        # 6 7 8    0 3 6
        #
        OriginalIndices = [0,1,2,5,8,7,6,3,4]
        RotatedIndices = [2,5,8,7,6,3,0,1,4]
        RotatedSeq = ["-" for i in range(9)]
        
        for i in range(len(OriginalIndices)):
            RotatedSeq[RotatedIndices[i]] = PatternSeq[OriginalIndices[i]]
        ret = Pattern(ToBeRotated.GetSymbol(), "".join(RotatedSeq))
        print(ToBeRotated.GetPatternSequence(), ret.GetPatternSequence())
        return ret
        
        
    
    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10

                    # Check rotated after normal checks
                    for P in self.__AllowedPatterns:
                        rotated = self.__RotatePatternCCW(P)
                        while rotated.GetPatternSequence() != P.GetPatternSequence():
                            CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                            if rotated.MatchesPattern(PatternString, CurrentSymbol):
                                self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                                return 5 ## Reduced because rotated match.
                            rotated = self.__RotatePatternCCW(rotated)
                            
                except Exception as e:
                    print(e)
        return 0

    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ").upper()
        return Symbol
    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def MatchesPattern(self, PatternString, SymbolPlaced):
        if SymbolPlaced != self.__Symbol:
            return False
        print("len", len(self.__PatternSequence))
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
        return self.__PatternSequence

    def GetSymbol(self):
        return self.__Symbol

class Cell():
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = ["B"]

    def GetBannedSymbols(self):
        res = ""
        for symbol in self.__SymbolsNotAllowed:
            res += symbol
        return res
    
    def GetSymbol(self):
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol
    
    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass

class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        return SymbolToCheck == "B"

if __name__ == "__main__":
    Main()

