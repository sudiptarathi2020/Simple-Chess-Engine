"""
This file is our driver file. It will be responsible for user inputs and displaying game state
"""
import pygame as p
from Chess import ChessEngine
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ["wP","wR","wN","wB","wQ","wK","bP","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("../images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_mode = False
    load_images()
    running = True
    sq_selected = () # tuple
    player_clicked = [] # keep track of player last click
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicked = []
                else:
                    sq_selected = (row, col)
                    player_clicked.append(sq_selected)

                if len(player_clicked) == 2:
                    move = ChessEngine.Move(player_clicked[0], player_clicked[1],gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_mode = True
                    sq_selected = ()
                    player_clicked = []
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undo_move()
                    move_mode = True

        if move_mode:
            valid_moves = gs.get_valid_moves()
            move_mode = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_board(screen):
    colors = [p.Color("white"),p.Color("gray")]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


if __name__ == '__main__':
    main()
