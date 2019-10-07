import random
import sys
import os
import time

class osTools():

    def __init__(self):
        pass

    def clearConsole(self):
        pass
        os.system("CLS")

class board():

    def __init__(self):
        self.boardScale = 6
        self.boardDefault = '-'
        self.mineChar = 'M'
        self.flagChar = 'F'
        self.mineFlag = 'U'
        self.explodeChar = 'X'
        self.searchArea = 3
        

    def createBoard(self):
        self.board = [[self.boardDefault for x in range(self.boardScale)] for y in range(self.boardScale)]

    # Sets board cell to specified value
    def setBoard(self,xCord,yCord,value):
        self.board[xCord][yCord] = value

    # Reset board to default #
    def initialiseBoard(self):
        for x in range(self.boardScale):
            for y in range(self.boardScale):
                self.board[x][y] = self.boardDefault

    # Sets random mines
    def setMines(self,mineCount):
        while(mineCount > 0):
            randx = random.randint(0,self.boardScale-1)
            randy = random.randint(0,self.boardScale-1)
            mineCount = mineCount - 1
            if(self.board[randx][randy] == self.mineChar):
                mineCount = mineCount + 1
            else:
                self.setBoard(randx,randy,self.mineChar)
            
class menu():

    def __init__(self):

        self.difficultySettings = {
            "Easy" : 2,
            "Medium" : 16,
            "Hard" : 32,
            "Extreme" : 64,
            "Super duper extreme" : 128
        }

    def printMenu(self):
        x = 0
        print("Welcome to PyMines, please choose your difficulty below")
        print("")
        for key in self.difficultySettings:
            x = x + 1
            print(x,".",key, '=', self.difficultySettings[key],"Mines")
        print("")
        validInput = False
        while(validInput == False):
            try:
                choice = int(input("Choice: "))
                if (isinstance(choice, int) == False) or (choice > x):
                    print("")
                    choice = int(input("Error, invalid option please try again: "))
                else:
                    validInput = True
                    c = 0
                    for key in self.difficultySettings:
                        c = c + 1
                        if(choice == c):
                            return self.difficultySettings[key]
            except(ValueError):
                print("")
                print("Please enter a value")


            
        

class game():

    def __init__(self):
        self.boardObj = board()
        self.cheatMode = 1
        self.osTools = osTools()
        self.menuObj = menu()
        self.gameOver = 0
        self.gameWon = 0

    def printHeader(self):
        print("  _____       __  __ _                 ")
        print(" |  __ \\     |  \\/  (_)     ")
        print(" | |__) |   _| \\  / |_ _ __   ___  ___ ")
        print(" |  ___/ | | | |\\/| | | '_ \\ / _ \\/ __|")
        print(" | |   | |_| | |  | | | | | |  __/\\__ \\")
        print(" |_|    \\__, |_|  |_|_|_| |_|\\___||___/")
        print("         __/ |                         ")
        print("        |___/                          ")
        print("")


    # Print the board #
    def printBoard(self):

            # Print the letter headers #
            print("    ",end="")
            for a in range(self.boardObj.boardScale):
                print(chr(65+a), " ", end="")
            print("")

            # Print the numbered rows #
            for x in range(self.boardObj.boardScale):
                if(x < 9):
                    print("",x+1," ",end="")
                else:
                    print(x+1," ",end="")
                for y in range(self.boardObj.boardScale):
                    printValue = self.boardObj.board[x][y]
                    if(printValue == self.boardObj.mineChar and self.cheatMode == 0):
                        printValue = self.boardObj.boardDefault
                    elif(printValue == self.boardObj.mineFlag):
                        printValue = self.boardObj.flagChar

                    print(printValue," ", end="")
                print("")

    def playerChoice(self):

        moveType = 0

        while(moveType < 1  or moveType > 2):
            print("Choose your move type")
            print("1. Reveal")
            print("2. Flag")
            try:
                moveType = int(input("Selection (1-2): "))
                if(moveType < 1 or moveType > 2):
                    print("")
                    print("Invalid input please try again.")
            except(ValueError):
                print("")
                print("Invalid input please try again.")

        rowMsg = "Choose column (" + chr(65) + '-' + chr(65+(self.boardObj.boardScale)-1) + "): "
        colMsg = "Choose row (1-" + str(self.boardObj.boardScale) + "): "

        validateLoop = False
        playerX = str(input(rowMsg))
        while(validateLoop == False):
            if(len(playerX) > 1 or (ord(playerX) > 65+(self.boardObj.boardScale-1))):
                print("Inavlid input")
                playerX = str(input(rowMsg))
            else:
                validateLoop = True

        playerY = int(input(colMsg))
        validateLoop = False
        while(validateLoop == False):
            if(isinstance(playerY, int) == False or playerY > self.boardObj.boardScale):
                print("Invalid Input")
                playerY = int(input(colMsg))
            else:
                validateLoop = True
        
        results = (playerY,playerX,moveType)
        return results


    def flagMine(self,x,y):
        pass

    def revealArea(self,x,y):

        minecount = 0
        xSearch = x - 1
 
        for xS in range(self.boardObj.searchArea):
            ySearch = y - 1
            for yS in range(self.boardObj.searchArea):
                try:
                    if(self.boardObj.board[xSearch][ySearch] == self.boardObj.mineChar or self.boardObj.board[xSearch][ySearch] == self.boardObj.mineFlag):
                        # Bug?? For some reason mines being detected in the negative axis which makes no sense...botch fix
                        if not(xSearch < 0 or ySearch < 0):
                            minecount = minecount + 1
                except (ValueError,IndexError):
                    pass
                ySearch = ySearch + 1

            xSearch = xSearch + 1
        return minecount

    def checkWinStatus(self):

        ContinueGame = False
        # Figure out a way to scan all tiles and change the game won attribute if they dont contain the default board value (currently '-')
        for x in range(self.boardObj.boardScale):
            for y in range(self.boardObj.boardScale):
                if(self.boardObj.board[x][y] == self.boardObj.mineChar):
                    ContinueGame = True

        if(ContinueGame == False):
            self.gameWon = 1
        else:
            self.gameWon = 0

    def devPrintMineCoords(self):
        for x in range(self.boardObj.boardScale):
            for y in range(self.boardObj.boardScale):
                if(self.boardObj.board[x][y] == self.boardObj.mineChar):
                    print(x,y)


    def checkMove(self,x,y,type):

        y = ord(y) - 65
        x = x - 1

        #self.devPrintMineCoords()

        #Type 1 - reveal
        if(type==1):
            if(self.boardObj.board[x][y] == self.boardObj.mineChar or self.boardObj.board[x][y] == self.boardObj.mineFlag):
                self.gameOver = 1
                for x in range(self.boardObj.boardScale):
                    for y in range(self.boardObj.boardScale):
                        if(self.boardObj.board[x][y] == self.boardObj.mineChar or self.boardObj.board[x][y] == self.boardObj.mineFlag):
                            self.boardObj.board[x][y] = self.boardObj.explodeChar
                        else:
                            self.boardObj.board[x][y] = self.boardObj.boardDefault
                    time.sleep(0.05)
                    self.osTools.clearConsole()
                    self.printHeader()
                    self.printBoard()
                    print("BANG!")
                    print("Game over!")
                    
            else:
                mineSearchValue = self.revealArea(x,y)
                self.boardObj.board[x][y] = mineSearchValue
        #Type 2 - flag
        elif(type==2):
            if(self.boardObj.board[x][y] == self.boardObj.mineChar):
                self.boardObj.board[x][y] = self.boardObj.mineFlag
            elif(self.boardObj.board[x][y] == self.boardObj.boardDefault):
                self.boardObj.board[x][y] = self.boardObj.flagChar
            else:
                self.boardObj.board[x][y] = self.boardObj.boardDefault

    def configureBoardScale(self,mineCount):

        if(mineCount == 2):
            self.boardObj.boardScale = 5
        elif(mineCount == 16):
            self.boardObj.boardScale = 8
        elif(mineCount == 32):
            self.boardObj.boardScale = 12
        elif(mineCount == 64):
            self.boardObj.boardScale = 16
        elif(mineCount == 128):
            self.boardObj.boardScale = 24
            


    def playGame(self):
        
        # Display the initial menu #
        self.osTools.clearConsole()
        self.printHeader()
        difficulty = self.menuObj.printMenu()
        self.configureBoardScale(difficulty)
        self.boardObj.createBoard()
        self.boardObj.initialiseBoard() # init the board for safety
        self.boardObj.setMines(difficulty)

        # Start the game loop
        while(self.gameOver == 0):
            self.osTools.clearConsole()
            self.printHeader()
            self.printBoard()
            move = self.playerChoice()
            self.checkMove(move[0],move[1],move[2])
            if(self.gameOver == 0):
                self.checkWinStatus()
            if(self.gameWon == 1):
                self.osTools.clearConsole()
                self.printHeader()
                self.printBoard()
                print("Congratulations you won! (placeholder)")
                self.gameOver = 1

if(__name__ == '__main__'):
    root = game()
    root.playGame()