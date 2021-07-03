"""
Main driver file. 
Handling user input 
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]

    # On crée juste un dict pour store les images 
    # {"wp": "images/wp.png"}
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    
def main():
    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT))

    # A quoi sert clock ?
    clock = p.time.Clock()

    # Background
    screen.fill(p.Color("white"))

    # On instancie dans gs tout l'état du jeu
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable pour quand un move est fait

    loadImages() #Only once, before while loop

    running = True

    sqSelected = () # le carré est cliqué - on le garde en mémoire ici
    playerClicks = [] # les deux cliques : prendre et déplacer - two tuples: [(7,4), (4,4)]


    while running:
        # Pour chaque évènement pygame, si le type de l'évènement vaut p.QUIT
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                # col c'est par exemple 485 // 64 = 7
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
               
                if sqSelected == (row, col): # si select deux fois le même carré
                    sqSelected = () # on cancel
                    playerClicks = [] # on cancel
                else:
                    sqSelected = (row, col) # On pose dans ce tuple là ou le joueur a cliqué
                    playerClicks.append(sqSelected) # on append que ce soit le 1er ou 2e click
                
                if len(playerClicks) == 2: # donc là c'est le 2e move : on bouge le pion puis on reset playersClicks pour repasser la length à 0

                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True

                        sqSelected = () # reset user clicks
                        playerClicks = []
                    else: 
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # quand on clique sur z
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        # A quoi ça sert ?
        p.display.flip()


def drawGameState(screen, gs):
    # Le draw se fait en deux temps : pour le highlight notamment
    drawBoard(screen) # draw squares on board
    drawPieces(screen, gs.board) # draw pieces on top of squares

def drawBoard(screen):
    colors = [p.Color("dark green"), p.Color("dark red")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()