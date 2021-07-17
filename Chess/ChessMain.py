"""
file responsible for handling user input and displaying the current game state
"""

import ChessEngine
import pygame as p

WIDTH = HEIGHT = 512
DIMENSIONS = 8 #dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15 #for future animations
IMAGE = {}

'''
Initialize a globa dictionary of images. will be called only one
'''

def loadImage():
    pieces= ['P','R','N','B','K','Q','p','r','n','b','q','k']
    for piece in pieces:
        if(piece.isupper()):
            IMAGE[piece] = p.transform.scale(p.image.load("pieces_img/white/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
        elif(piece.islower()):
            IMAGE[piece] = p.transform.scale(p.image.load("pieces_img/black/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))


'''
main driver for the code
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImage()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handles
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(playerClicks)
                    #verifica se o movimento que quer ser realizado e valido
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            #keyboard engine
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z ins pressed
                    gs.undoMove()
                    moveMade = True
        #obtem novamente os movimentos validos e atualiza novamente a flag( para poupar processamento)
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors = [p.Color("tan4"),p.Color("burlywood")]
    for row in range(DIMENSIONS):
        for colum in range(DIMENSIONS):
            color= colors[(colum+row)%2]
            p.draw.rect(screen,color,p.Rect(colum*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSIONS):
        for colum in range(DIMENSIONS):
            piece = board[row][colum]
            if piece != ".":
                screen.blit(IMAGE[piece],p.Rect(colum*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))




if __name__ =="__main__":
    main()