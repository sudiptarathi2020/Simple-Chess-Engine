"""
This file is our engine file. It will be responsible for user engine and displaying game state
"""
class GameState:
    def __init__(self):
        # Board is 8*8 2-dimensional list and each element of the list have two char
        # First char represent color
        # second char represent type
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wB", "bB", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_functions = {'P': self.get_pawn_move, 'R': self.get_rook_move,
                               'N': self.get_knight_move, 'B': self.get_bishop_move,
                               'Q': self.get_queen_move, 'K': self.get_king_move
                               }

        self.whiteToMove = True
        self.moveLog = []
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
    def undo_move(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not self.whiteToMove
    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        return self.get_all_possible_moves()


    '''
    All moves without considering checks
    '''
    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w'and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r,c, moves)

        return moves

    '''
    Get the pawn moves for all the pawns
    '''
    def get_pawn_move(self, row, col, moves):
        if self.whiteToMove:
            if self.board[row-1][col] == "--":
                moves.append(Move((row,col),(row-1,col),self.board))
                if row == 6 and self.board[row-2][col] == "--":
                    moves.append(Move((row,col),(row-2,col),self.board))

            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row,col),(row-1,col-1),self.board))
            if col+1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row,col),(row-1,col+1),self.board))
        else:
            if self.board[row+1][col] == "--":
                moves.append(Move((row,col),(row+1,col),self.board))
                if row == 1 and self.board[row+2][col] == "--":
                    moves.append(Move((row,col),(row+2,col),self.board))

            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row,col),(row+1,col-1),self.board))
            if col+1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row,col),(row+1,col+1),self.board))



    def get_rook_move(self, r, c, moves):

        directions = {(1,0),(-1,0),(0,1),(0,-1)}
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break
                    else:
                        break
                else:
                    break
    def get_knight_move(self, r, c, moves):
        d_row = [1,1,-1,-1,2,2,-2,-2]
        d_col = [2,-2,2,-2,1,-1,1,-1]

        for i in range(8):
            temp_r = r + d_row[i]
            temp_c = c + d_col[i]
            if 0 <= temp_r < 8 and 0 <= temp_c < 8:
                if self.board[r][c][0] != self.board[temp_r][temp_c][0]:
                    moves.append(Move((r,c),(temp_r,temp_c),self.board))

    def get_bishop_move(self, r, c, moves):
        directions = {(1,1),(1,-1),(-1,1),(-1,-1)}
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_move(self, r, c, moves):
        self.get_rook_move(r, c, moves)
        self.get_bishop_move(r, c, moves)

    def get_king_move(self, r, c, moves):
        directions = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1))
        enemy_color = "b" if self.whiteToMove else "w"
        for i in range(8):
            end_row = r + directions[i][0]
            end_col = c + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                elif end_piece[0] == enemy_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                    break
                else:
                    break







class Move:

    ranks_to_rows = {"1": 7, "2": 6, "3": 5,
                     "4": 4, "5":3, "6":2, "7":1, "8":0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a":0, "b":1, "c":2, "d":3,"e":4, "f":5, "g":6,"h":7,}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    '''
        Overriding the equals move
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col)+ self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self,row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
