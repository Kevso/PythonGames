#!/usr/bin/env python
from Tkinter import *
import random

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    if (event.keysym == "r"):
        init()

    elif canvas.data.isGameOver == False:
        if (event.keysym == "Left"):
            moveFallingPiece(0,-1)
        elif (event.keysym == "Right"):
            moveFallingPiece(0,+1)
        elif (event.keysym == "Down"):
            moveFallingPiece(+1,0)
        elif (event.keysym == "Up"):
            rotateFallingPiece()
    redrawAll()

#############Rotating Piece
def fallingPieceCenter():
    row = len(canvas.data.fallingPiece) / 2
    col = len(canvas.data.fallingPiece[0]) /2
    return (row, col)

def rotateFallingPiece():
    newPiece = [] # Make a temporary new matrix for rotated falling Piece
    canvas.data.currentRow = len(canvas.data.fallingPiece)
    canvas.data.currentCol = len(canvas.data.fallingPiece[0])
    currentFallingPiece = canvas.data.fallingPiece
    (oldRow,oldCol) = fallingPieceCenter()
    # Switch Rows and Cols into into temporary rows and cols of pieces position
    canvas.data.currentRow = len(canvas.data.fallingPiece[0]) 
    canvas.data.currentCol = len(canvas.data.fallingPiece)
    (newRow,newCol) = fallingPieceCenter()
    canvas.data.fallingPieceRow -= (newRow - oldRow)
    canvas.data.fallingPieceCol -= (newCol - oldCol)
    
    for row in range(canvas.data.currentRow):
        newPiece += [[True]*canvas.data.currentCol]
        
    for col in range(len(canvas.data.fallingPiece[0])):
        for row in range(len(canvas.data.fallingPiece)):
            newPiece[col][row] = canvas.data.fallingPiece[row]\
                                 [len(canvas.data.fallingPiece[0])-1-col]
    canvas.data.fallingPiece = newPiece
    # Test whether the rotated Piece is in a legal place
    if (fallingPieceIsLegal(canvas.data.fallingPieceRow,
                           canvas.data.fallingPieceCol) == False):
        canvas.data.fallingPiece = currentFallingPiece
        canvas.data.fallingPieceRow += (newRow - oldRow)
        canvas.data.fallingPieceCol += (newCol - oldCol)

############Falling Piece

def moveFallingPiece(drow, dcol):
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if(fallingPieceIsLegal(canvas.data.fallingPieceRow, canvas.data.fallingPieceCol)):
        return True
    else:
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False

def placeFallingPiece():
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if canvas.data.fallingPiece[row][col] == True:
                canvas.data.board[canvas.data.fallingPieceRow + row][canvas.data.fallingPieceCol + col] = canvas.data.fallingPieceColor

def fallingPieceIsLegal(pieceRow, pieceCol):
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if canvas.data.fallingPiece[row][col] == True:
                 if ((pieceRow+row < 0) or (pieceRow+row >= canvas.data.rows) or\
                     (pieceCol+col < 0) or (pieceCol+col >= canvas.data.cols)):
                     return False
                 elif (canvas.data.board[pieceRow+row][pieceCol+col] !=
                       canvas.data.emptyColor):
                     return False       
    return True
    

#############New Piece

def newFallingPiece():
    index = random.randint(0,6)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[index]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[index]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - len(canvas.data.fallingPiece[0])/2

def drawFallingPiece():
    rows = len(canvas.data.fallingPiece)
    cols = len(canvas.data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if canvas.data.fallingPiece[row][col] == True:
                drawCell(row+canvas.data.fallingPieceRow,
                         col+canvas.data.fallingPieceCol,
                         canvas.data.fallingPieceColor)
 
################Draw

def redrawAll():
    canvas.delete(ALL)
    if canvas.data.isGameOver == True:
        drawGame()
        canvas.create_text(canvas.data.canvasWidth/2,
                           canvas.data.canvasHeight*2/5, text="Game Over!",
                           fill="yellow", font="Helvetica 26 bold")
        canvas.create_text(canvas.data.canvasWidth/2,
                           canvas.data.canvasHeight*3/5,
                           text="Press 'r' to reset", fill="yellow",
                           font="Helvetica 13 bold")
    else:
        drawGame()
        drawFallingPiece()
    canvas.create_text(canvas.data.canvasWidth/2, canvas.data.margin/2,
                       text="Score: " + str(canvas.data.score), fill="black",
                       font="Helvetica 13")

def drawGame():
    # draw the background of board
    canvas.create_rectangle(0,0,
                            canvas.data.canvasWidth,
                            canvas.data.canvasHeight, fill="orange")
    drawBoard()

def drawBoard():
    tetrisBoard = canvas.data.board
    rows = len(tetrisBoard)
    cols = len(tetrisBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawCell(row, col, tetrisBoard[row][col])

def drawCell(row, col, cellColor):
    # Draws each cell black and a smaller cell within it the color of the piece
    # if contained or else, draw the unoccupied place blue
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    gridMargin = 2
    canvas.create_rectangle(left-gridMargin, top-gridMargin,
                            right+gridMargin, bottom+gridMargin, fill="black")
    canvas.create_rectangle(left+gridMargin, top+gridMargin,
                            right-gridMargin, bottom-gridMargin, fill=cellColor)

##############Full Rows

def removeFullRows():
    # If ifFullRow returns False,do not pop, if True, pop the row
    # score is calculated for each row deleted, if more than is deleted at once
    # square the numbers of rows deleted at once
    rows = len(canvas.data.board)
    score = 0
    hadFullRows = False
    for row in range(rows):
        if isFullRow(row):
            canvas.data.board.pop(row)
            canvas.data.board.insert(0, [canvas.data.emptyColor] * canvas.data.cols)
            score += 1
            hadFullRows = True
    if hadFullRows:
        canvas.data.score += score
        adjustSpeed() # Get a little bit faster!

def adjustSpeed():
    currentLevel = canvas.data.score / canvas.data.levelUpScoreInterval
    if currentLevel != canvas.data.level:
        canvas.data.level = currentLevel
        canvas.data.delay = speedCalc(canvas.data.level)

def speedCalc(level):
    return int(canvas.data.delay / level)

def isFullRow(row):
    # Tests each row and see that if it ever contains a blue cell, if it is,
    # it returns False, if it does not, returns Trur
    for col in canvas.data.board[row]:
        if col == canvas.data.emptyColor:
            return False
    return True

def make2dList(rows, cols):
    tetrisBoard = [cols * [columns] for columns in [canvas.data.emptyColor] * rows]
    return tetrisBoard


def timerFired():
    removeFullRows()
    if (canvas.data.isGameOver == True):
        redrawAll()
    else:
        redrawAll()
        if moveFallingPiece(1,0) == False:
            placeFallingPiece()
            removeFullRows()
            newFallingPiece()
            if fallingPieceIsLegal(canvas.data.fallingPieceRow,
                                       canvas.data.fallingPieceCol) == False:
                    canvas.data.isGameOver = True
    canvas.after(canvas.data.delay, timerFired) # pause, then call timerFired again

def init():
    canvas.data.board = make2dList(canvas.data.rows,canvas.data.cols)
    canvas.data.score = 0
    canvas.data.delay = canvas.data.standardDelay = 500 #milliseconds
    canvas.data.level = 0
    canvas.data.levelDelayDelta = .8 # 20% speed increase from level to level
    canvas.data.levelUpScoreInterval = 10
    #Seven "standard" pieces (tetrominoes)
    iPiece = [ [ True,  True,  True,  True] ]
    
    jPiece = [ [ True, False, False ],
               [ True, True,  True] ]
    
    lPiece = [ [ False, False, True],
               [ True,  True,  True] ]
    
    oPiece = [ [ True, True],
               [ True, True] ]
    
    sPiece = [ [ False, True, True],
               [ True,  True, False ] ]
    
    tPiece = [ [ False, True, False ],
               [ True,  True, True] ]
    
    zPiece = [ [ True,  True, False ],
               [ False, True, True] ]
    canvas.data.tetrisPieces = [ iPiece, jPiece, lPiece,
                                 oPiece, sPiece, tPiece, zPiece ]
    canvas.data.tetrisPieceColors = [ "red", "yellow", "magenta",
                                      "pink", "cyan", "green", "orange" ]
    canvas.data.fallingPiece = []
    canvas.data.fallingPieceColor = ""
    canvas.data.isGameOver = False
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = 0
    newFallingPiece()
  
    

########### copy-paste below here ###########

def run(rows, cols):
    # create the root and the canvas
    global canvas
    root = Tk()
    margin = 20
    cellSize = 20
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0,height=0)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.emptyColor = "blue"
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run(15,10)
