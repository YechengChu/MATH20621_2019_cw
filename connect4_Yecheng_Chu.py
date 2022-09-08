"""
A simple connect4 game with a 7x6 game board.
The game can be played either by two humans, a human against a computer,
or by the computer against itself.
The module also allows the current game to be saved, and a previously
saved game to be loaded and continued.

Yecheng Chu
Last update: 01/12/2019
"""

from copy import deepcopy # you may use this for copying a board

def newGame(player1,player2):
    """
    set the player with the input string given
    make player1 to do the first move
    Initialize all the positions in the board to zero

    Parameters:
    player1 (string): the name of the first player
    player2 (string): the name of the second player

    Returns:
    game (dictionary): containing information of the two player names,
                       whose turn to player the game next,
                       and the current game board
    """
    # TODO: Initialize dictionary for a new game
    game = {
        'player1' : player1,
        'player2' : player2,
        'who' : 1,
        'board' : [ [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0] ]
    }
    return game
# TODO: All the other functions of Tasks 2-11 go here.
# USE EXACTLY THE PROVIDED FUNCTION NAMES AND VARIABLES!
def printBoard(board):
    """
    print out the game 7x6 board according to the supplied board
    palyer1 is represented by "X"
    player2 is represented by "O"

    Parameters:
    board (list): a list of lists representing the game board

    Returns:
    No returned value
    """
    # print first row "|1|2|3|4|5|6|7|"
    for i in range (1, 8):
        print("|" + str(i), end = '')
    print("|")
    # print second row "+-+-+-+-+-+-+-+"
    for i in range (7):
        print("+-", end = '')
    print("+")
    # print the board row by row
    # " " for 0, "X" for player1, "O" for player2
    for x in range (6):
        for y in range (7):
            if (board[x][y] == 0):
                position = " "
            elif (board[x][y] == 1):
                position = "X"
            else:
                position = "O"
            print("|" + position, end = '')
        print("|")
def getValidMoves(board):
    """
    Check if there is empty space at the top of every columns.
    If no valid move is possible, returns an empty list.

    Parameters:
    board (list): a list of lists representing the game board

    Returns:
    validMoves (list): a list containing indices of the board columns
                       which are not completely filled
    """
    validColumns = []
    # Only check the top row
    # if the top of a column is empty, then the column is valid to select
    for y in range (7):
        if (board[0][y] == 0):
            validColumns.append(y)
    return validColumns
def makeMove(board,move,who):
    """
    Make a move on the game board according to the input.

    Parameters:
    board (list): a list of lists representing the game board
    move (int): indice of the board column to insert the "disc"
    who (int): the player who take the move

    Returns:
    board (list): a list of lists representing the game board after the player
                  have inserted the "disc"
    """
    # if the end of the selected column is empty, place the disc there
    if (board[5][move] == 0):
        board[5][move] = who
        return board
    # else from top to buttom, find the position which is now empty
    # but there is a disc below the current position
    # (find the empty position above the piled discs)
    for x in range (5):
        if (board[x][move] == 0 and board[x+1][move] != 0):
            board[x][move] = who
    return board
def hasWon(board,who):
    """
    Check whether a player has won the game.
    The program loops around the whole board. For every position the given
    player has a "disc", check whether the player has another success three
    same "discs" in a line in 8 direction(above, below, left, right, top left,
    top right, bottom right and bottom left)

    Parameters:
    board (list): a list of lists representing the game board
    who (int): the player who need to be checked  whether has won

    Returns:
    True or False (boolean): depend on whether the given player has won.
    """
    # for every posiion in the board
    for x in range (6):
        for y in range (7):
            # for every  position in the board which equals the winner
            if (board[x][y] == who):
                # check if there are furhter 3 same discs below
                if ((x + 3) < 6):
                    if (board[x][y] == board[x+1][y] == board[x+2][y]
                        == board[x+3][y]):
                        return True
                # check if there are further 3 same discs in the right
                if ((y + 3) <= 6):
                    if (board[x][y] == board[x][y+1] == board[x][y+2]
                        == board[x][y+3]):
                        return True
                # check if there are further 3 same discs in the bottom left
                if ((x + 3) < 6 and (y - 3) >= 0):
                    if (board[x][y] == board[x+1][y-1] == board[x+2][y-2]
                        == board[x+3][y-3]):
                        return True
                # check if there are further 3 same discs in the bottom right
                if ((x + 3) < 6 and (y + 3) <= 6):
                    if (board[x][y] == board[x+1][y+1] == board[x+2][y+2]
                        == board[x+3][y+3]):
                        return True
    return False
def suggestMove1(board,who):
    """
    Suggest the next move for a given player.
    If there is a immediate win return that indice.
    If the other player will have a immediate win, return the indice to
    prevent the other player to win.
    Else, return the first element in the valid move.

    Parameters:
    board (list): a list of lists representing the game board
    who (int): the player who need to be take a move

    Returns:
    An int reperesenting the suggest indice of the board column to place the
    "disc".
    """
    # first get validMoves
    validMoves = getValidMoves(board)
    # calculate the opponent
    opponent = 3 - who
    # check each valid column
    for i in validMoves:
        board2 = deepcopy(board)
        testBoard = makeMove(board2,i,who)
        # If I can have an immediate win when choose this column, select this column
        if (hasWon(testBoard,who)):
            return i
        board3 = deepcopy(board)
        testBoardOpponent = makeMove(board3, i, opponent)
        # If my opponent can have an immediate win when choose this column,
        # select this column to prevent the opponent from wining
        if (hasWon(testBoardOpponent, opponent)):
            return i
    # Otherwise, return the first element in the validMoves
    return validMoves[0]
def loadGame(filename = "game.txt"):
    """
    Load a game from a saved file. Raise exception when the file is not found or
    format of the saved file is incorrect.

    Parameters(optional):
    filename (string): name of the file to load (default: "game.txt")

    Returns:
    game (dictionary): containing information of the two player names,
                       whose turn to player the game next,
                       and the current game board
    """
    # open the file for read
    with open(filename, mode="rt", encoding="utf8") as f:
        # read the whole file and split the lines according to “\n” in the file
        # text is a list containing each line of the file
        # the following 1 line follow a similar code on
        # https://stackoverflow.com/questions/15233340/getting-rid-of-n-when-using-readlines
        # as retrieved on 06/11/2019
        text = f.read().splitlines()
        # the first line is the player1 name, if empty raise ValueError
        player1 = text[0]
        # the following 1 line follow a similar code on
        # https://www.tutorialspoint.com/What-is-the-most-elegant-way-to-check-if-the-string-is-empty-in-Python
        # as retrieved on 06/11/2019
        if (not player1.strip()):
            raise ValueError("The player 1 is not found!")
        # the second line is the player2 name, if empty raise ValueError
        player2 = text[1]
        # the following 1 line follow a similar code on
        # https://www.tutorialspoint.com/What-is-the-most-elegant-way-to-check-if-the-string-is-empty-in-Python
        # as retrieved on 06/11/2019
        if (not player2.strip()):
            raise ValueError("The player 2 is not found!")
        # the third line should determine whose turn to play, if it is not 1
        # or 2 raise ValueError
        who = int(text[2]);
        if (who != 1 and who != 2):
            raise ValueError("Whose turn is not defined properly!")
        # check each line in the board
        board = []
        for i in range(3, 9):
            # split a line according to "," and add them into a list then into a
            # new int list check if the number is 0, 1 or 2, if not raise ValueError
            # if no error, add them to board
            list = (text[i]).split(",")
            # if the number of elements in a row is less than 7, raise ValueError
            if(len(list) != 7):
                raise ValueError("The board has at least one column missing on one row!")
            intList = []
            for x in list:
                intList.append(int(x))
            for x in intList:
                if (x != 0 and x != 1 and x != 2):
                    raise ValueError("Problem with initializing the board!")
            board.append(intList)
        # check whether the discs arrange is ok
        # there should be no disc above the top of the piled discs
        for y in range(7):
            # stands for the current position should be empty
            isEmpty = False
            # from bottom to above, if find a empty space above the piled disc,
            # set isEmpty true, so the above should all be empty
            # if the above is not empty, raise ValueError
            for x in range(5, -1, -1):
                if (board[x][y] != 0 and isEmpty):
                    raise ValueError("Problem with the discs arrange!")
                elif(board[x][y] == 0):
                    isEmpty = True
        game = {
            'player1' : player1.capitalize(),
            'player2' : player2.capitalize(),
            'who' : who,
            'board' : board
        }
        return game
def saveGame(game,filename = "game.txt"):
    """
    Save a game to a file. Raise exception when something goes wrong.

    Parameters:
    game (dictionary): containing information of the two player names,
                       whose turn to player the game next,
                       and the current game board
    filename (string) (optinal): name of the file to save (default: "game.txt")

    Returns:
    No returned value
    """
    with open(filename, mode="wt", encoding="utf8") as f:
        # write player1, player2 and who with a "\n" at end of each
        f.write(game['player1'])
        f.write("\n")
        f.write(game['player2'])
        f.write("\n")
        f.write(str(game['who']))
        f.write("\n")
        gameBoard = game['board']
        for x in range (6):
            # go over the first 6 colums write the board element with a "," next to it
            for y in range (6):
                f.write(str(gameBoard[x][y]))
                f.write(",")
            # write the last element in a column with a "\n" at the end
            f.write(str(gameBoard[x][6]))
            f.write("\n")
def suggestMove2(board,who):
    """
    Suggest the next move for a given player.
    First chec the position when I place the disc will lead to immediate win for
    opponent, that is not good.
    If there is a immediate win return that indice.
    If the other player will have a immediate win, return the indice to
    prevent the other player to win.
    If I can form three discs in a line without any further other disc next to the line,
    and the position is not in not good return that indice.
    Prevent opponent form three discs in a line without any further other disc next to the line,
    and the position is not in not good return that indice, return that indice.
    If the cental column (3) is in valid move and is not in not good, return 3.
    Else return the first element in the valid move which is not in not good.
    Else, return the first element in the valid move.

    Parameters:
    board (list): a list of lists representing the game board
    who (int): the player who need to be take a move

    Returns:
    An int reperesenting the suggest indice of the board column to place the
    "disc".
    """
    validMoves = getValidMoves(board)
    opponent = 3 - who
    # first check the postion where I put my disc will lead to an immediate win
    # of my opponent, record those positions in notGood
    notGood = []
    for i in validMoves:
        testBoardOpponent1 = deepcopy(board)
        testBoardOpponent1 = makeMove(testBoardOpponent1, i, who)
        validMovesAfter = getValidMoves(testBoardOpponent1)
        for n in validMovesAfter:
            board2 = deepcopy(testBoardOpponent1)
            testBoardOpponent1Next = makeMove(board2, n, opponent)
            if (hasWon(testBoardOpponent1Next, opponent)):
                notGood.append(i)
                break

    for i in validMoves:
        testBoard = deepcopy(board)
        testBoard = makeMove(testBoard,i,who)
        # If I can have an immediate win when choose this column, select this column
        if (hasWon(testBoard,who)):
            return i
        testBoardOpponent2 = deepcopy(board)
        testBoardOpponent2 = makeMove(testBoardOpponent2, i, opponent)
        # If my opponent can have an immediate win when choose this column,
        # select this column to prevent the opponent from wining
        if (hasWon(testBoardOpponent2, opponent)):
            return i

        # try to make three discs in a line
        board3 = deepcopy(board)
        board3 = makeMove(board3, i, who)
        newPosition = 0
        while (board3[newPosition][i] == 0):
            newPosition += 1
        # check if there are 2 discs in the left and no further disc in the left
        if ((i - 3) >= 0):
            if (board3[newPosition][i] == board3[newPosition][i-1]
                 == board3[newPosition][i-2] and board3[newPosition][i-3] == 0):
                 if i not in notGood:
                     return i
        # check if there are 2 discs in the right and no further disc in the right
        if ((i + 3) <= 6):
            if (board3[newPosition][i] == board3[newPosition][i+1]
                 == board3[newPosition][i+2] and board3[newPosition][i+3] == 0):
                 if i not in notGood:
                     return i
        # check if the inserted one is in the middle with two other same disc
        # on left and right and no further discs on both sides
        if ((i - 2) >= 0 and (i + 2) <= 6):
            if (board3[newPosition][i] == board3[newPosition][i-1] == board3[newPosition][i+1]
                and board3[newPosition][i-2] == board3[newPosition][i-2] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the top left and no further disc in the top left
        if ((newPosition - 3) >= 0 and (i - 3) >= 0):
            if (board3[newPosition][i] == board3[newPosition-1][i-1]
                == board3[newPosition-2][i-2] and board3[newPosition-3][i-3] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the top right and no further disc in the top right
        if ((newPosition - 3) >= 0 and (i + 3) <= 6):
            if (board3[newPosition][i] == board3[newPosition-1][i+1]
                == board3[newPosition-2][i+2] and board3[newPosition-3][i-3] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the bottom left and no further disc in the bottom left
        if ((newPosition + 3) < 6 and (i - 3) >= 0):
            if (board3[newPosition][i] == board3[newPosition+1][i-1]
                == board3[newPosition+2][i-2] and board3[newPosition+3][i-3] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the bottom right and no further disc in the bottom right
        if ((newPosition + 3) < 6 and (i + 3) <= 6):
            if (board3[newPosition][i] == board3[newPosition+1][i+1]
                == board3[newPosition+2][i+2] and board3[newPosition+3][i+3]):
                if i not in notGood:
                    return i

        # try to avoid three discs in a line for opponent
        board3 = deepcopy(board)
        board3 = makeMove(board3, i, opponent)
        newPosition = 0
        while (board3[newPosition][i] == 0):
            newPosition += 1
        # check if there are 2 discs in the left and no further disc in the left
        if ((i - 3) >= 0):
            if (board3[newPosition][i] == board3[newPosition][i-1]
                 == board3[newPosition][i-2] and board3[newPosition][i-3] == 0):
                 if i not in notGood:
                     return i
        # check if there are 2 discs in the right and no further disc in the right
        if ((i + 3) <= 6):
            if (board3[newPosition][i] == board3[newPosition][i+1]
                 == board3[newPosition][i+2] and board3[newPosition][i+3] == 0):
                 if i not in notGood:
                     return i
        # check if the inserted one is in the middle with two other same disc
        # on left and right and no further discs on both sides
        if ((i - 2) >= 0 and (i + 2) <= 6):
            if (board3[newPosition][i] == board3[newPosition][i-1] == board3[newPosition][i+1]
                and board3[newPosition][i-2] == board3[newPosition][i-2] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the top left and no further disc in the top left
        if ((newPosition - 3) >= 0 and (i - 3) >= 0):
            if (board3[newPosition][i] == board3[newPosition-1][i-1]
                == board3[newPosition-2][i-2] and board3[newPosition-3][i-3] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the top right and no further disc in the top right
        if ((newPosition - 3) >= 0 and (i + 3) <= 6):
            if (board3[newPosition][i] == board3[newPosition-1][i+1]
                == board3[newPosition-2][i+2] and board3[newPosition-3][i-3] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the bottom left and no further disc in the bottom left
        if ((newPosition + 3) < 6 and (i - 3) >= 0):
            if (board3[newPosition][i] == board3[newPosition+1][i-1]
                == board3[newPosition+2][i-2] and board3[newPosition+3][i-3] == 0):
                if i not in notGood:
                    return i
        # check if there are 2 discs in the bottom right and no further disc in the bottom right
        if ((newPosition + 3) < 6 and (i + 3) <= 6):
            if (board3[newPosition][i] == board3[newPosition+1][i+1]
                == board3[newPosition+2][i+2] and board3[newPosition+3][i+3]):
                if i not in notGood:
                    return i
    # suggestMove contains indice which is in validMoves and not in notGood
    suggestMove = []
    for i in validMoves:
        if i not in notGood:
            suggestMove.append(i)
    # if have central column, select cental column, else if suggestMove is not
    # empty, return first in the suggestMove, else return the first in the validMoves
    if 3 in suggestMove:
        return 3
    # the following 1 line follow a similar code on
    # https://stackoverflow.com/questions/5086178/how-to-check-if-array-is-not-empty
    # as retrieved on 08/11/2019
    elif suggestMove:
        return suggestMove[0]
    else:
        return validMoves[0]
# ------------------- Main function --------------------
def play():
    """
    The main function of the game. Game can be played either by two humans,
    a human against a computer, or by the computer against itself.
    It allows the current game to be saved, and a previously saved game to be
    loaded and continued.
    The exception is handled in this function.

    Parameters:
    No parameters taken

    Returns:
    No returned value
    """
    print("*"*55)
    print("***"+" "*8+"WELCOME TO STEFAN'S CONNECT FOUR!"+" "*8+"***")
    print("*"*55,"\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")
    # TODO: Game flow control starts here
    # Initially ther is no valid enty for player names, no game and the game is
    # not finished
    validEntry = False
    game = None
    hasFinished = False
    while not validEntry:
        # if a player1 do not give a name, the program keeps asking
        player1 = input("Name of player 1: ")
        # the following 1 line follow a similar code on
        # https://www.tutorialspoint.com/What-is-the-most-elegant-way-to-check-if-the-string-is-empty-in-Python
        # as retrieved on 06/11/2019
        if (not player1.strip()):
            continue
        # if the player1 is "L", ask the player to provide file name of a save game
        # load that game and skip the ask name part. Exception will be handled when
        # there is somthing wrong when read the file
        if (player1 == "L"):
            try:
                gameName = input("Enter the file name where your game is saved: ")
                # the following 1 line follow a similar code on
                # https://www.tutorialspoint.com/What-is-the-most-elegant-way-to-check-if-the-string-is-empty-in-Python
                # as retrieved on 06/11/2019
                if (not gameName.strip()):
                    game = loadGame()
                    print("Game loaded from game.txt")
                else:
                    game = loadGame(gameName)
                    print("Game loaded from " + gameName)
                print("")
                printBoard(game['board'])
                print("")
                break
            except FileNotFoundError:
                print("File not found error!")
                print("Wrong file or file path!")
                hasFinished = True
                break
            except ValueError as e:
                print("Value error!")
                print(e)
                hasFinished = True
                break
            except Exception as e:
                print("Unknown exception happens! See description below!")
                print(e)
                hasFinished = True
                break
        # if a player2 do not give a name, the program keeps asking
        player2 = input("Name of player 2: ")
        # the following 1 line follow a similar code on
        # https://www.tutorialspoint.com/What-is-the-most-elegant-way-to-check-if-the-string-is-empty-in-Python
        # as retrieved on 06/11/2019
        while (not player2.strip()):
            player2 = input("Name of player 2: ")
        validEntry = True
        # capitalize the player names and initializing the game
        game = newGame(player1.capitalize(), player2.capitalize())
        print("Okay,let's play!\n")
        printBoard(game['board'])
        print("")
    while not hasFinished:
        # record whoseTurn, gameBoard from the game
        whoseTurn = game['who']
        gameBoard = game['board']
        player = None
        playerSymbol = None
        nextMove = None
        # set the player and player Symbol
        if (whoseTurn == 1):
            player = game['player1']
            playerSymbol = "X"
        else:
            player = game['player2']
            playerSymbol = "O"

        # if it is computer make auto move
        if (player == "C"):
            nextMove = suggestMove2(gameBoard, whoseTurn)
            print("Computer (" + playerSymbol + ") is thinking... and selected column "
                  +  str(nextMove + 1) + ".")
        # if player ask to provide move
        # if the input is "S", ask the player for saved file name and save file,
        # if exception happens when saving the file, print a warning and continue
        # the game. If the game is saved, exit the game
        # else, check if the input is valid, keep asking until a valid input is given
        else:
            validMoveForPlayer = getValidMoves(gameBoard)
            isValid = False
            isSaved = False
            while not isValid:
                notInt = False
                nextMove = input(player + " (" + playerSymbol + "): Which column to select? ")
                if (nextMove == "S"):
                    try:
                        fileName = input("Enter the name of the file you want to save your game: ")
                        # the following 1 line follow a similar code on
                        # https://www.tutorialspoint.com/What-is-the-most-elegant-way-to-check-if-the-string-is-empty-in-Python
                        # as retrieved on 06/11/2019
                        if (not fileName.strip()):
                            saveGame(game)
                            print("Game saved to game.txt successfully!")
                        else:
                            saveGame(game, fileName)
                            print("Game saved to " + fileName + " successfully!")
                        isSaved = True
                        break
                    except Exception:
                        print("File saving error!")
                        notInt = True
                if notInt:
                    print("Please supply an int as input!")
                else:
                    try:
                        nextMove = int(nextMove) - 1
                        if nextMove in validMoveForPlayer:
                            isValid = True
                        else:
                            print("Invalid input. Try again!")
                    except ValueError as e:
                        print(e)
                        print("Invalid input. Try again!")
                        pass
            if isSaved:
                break
        # make move and print out the board after move
        print("")
        gameBoard = makeMove(gameBoard, nextMove, whoseTurn)
        printBoard(gameBoard)
        print("")
        game['board'] = gameBoard

        # first check if anyone has won, then check if there is a draw
        # if any of the situtaion happens exit the game
        nextValidMoves = getValidMoves(gameBoard)
        if (hasWon(gameBoard,whoseTurn)):
            hasFinished = True
            if (player == "C"):
                print("Computer (" + playerSymbol + ") has won!")
            else:
                print(player + " (" + playerSymbol + ") has won!")
        # the following 1 line follow a similar code on
        # https://stackoverflow.com/questions/53513/how-do-i-check-if-a-list-is-empty
        # as retrieved on 06/11/2019
        elif (not nextValidMoves):
            hasFinished = True
            print("There was a draw!")

        # Update whose turn next if the game is not finished yet
        if not hasFinished:
            game['who'] = 3 - whoseTurn

# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
    play()
