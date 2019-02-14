import random


pieces = {'T': [[1, 1, 1], [0, 1, 0]],
          'S': [[2, 2, 0], [0, 2, 2]],
          'Z': [[0, 3, 3], [3, 3, 0]],
          'O': [[4, 4], [4, 4]],
          'L': [[5, 5, 5], [5, 0, 0]],
          'J': [[6, 6, 6], [0, 0, 6]],
          'I': [[7, 7, 7, 7], ]}


class Play:

    def __init__(self, columns, rows):

        self.field = []
        self.ground = []
        self.x = columns
        self.y = rows

        for y in range(self.y):
            self.field.append([])
            self.ground.append([])
            for x in range(self.x):
                self.field[-1].append(0)
                self.ground[-1].append(0)

        self.piece = None
        self.px = 0
        self.py = 0

    def piece_insert(self, shape='T'):

        self.piece = pieces[shape]
        self.py = 0
        self.px = (self.x - len(self.piece[0])) // 2

        self.merge_field()

    def piece_fall(self, test=False):

        if not test:
            if self.piece is None:
                if self.delete_row(self.test_fullrow()):
                    return

                self.piece_insert(random.choice(list(pieces.keys())))
                return

        new_py = self.py + 1

        if self.test_collision(py=new_py):
            if test:
                return True
            self.piece_ground()
            return

        self.py = new_py
        if test:
            return False

        self.merge_field()

    def piece_move(self, side='L', test=False):

        new_px = (self.px + 1) if (side != 'L') else (self.px - 1)

        if self.test_collision(px=new_px):
            return False

        self.px = new_px
        if test:
            return True

        self.merge_field()

    def piece_rotate(self, side='L', test=False):

        if self.piece is None:
            return

        w = len(self.piece[0])
        h = len(self.piece)

        new_piece = []

        for y in range(w):
            new_piece.append([])
            for x in range(h):
                if side != 'L':
                    new_piece[-1].append(self.piece[h-1-x][y])
                else:
                    new_piece[-1].append(self.piece[x][w-1-y])

        if self.test_collision(new_piece):
            return False

        self.piece = new_piece
        if test:
            return True

        self.merge_field()

    def piece_ground(self):

        w = len(self.piece[0])
        h = len(self.piece)

        for y in range(h):
            for x in range(w):
                if self.piece[y][x] != 0:
                    self.ground[self.py + y][self.px + x] = self.piece[y][x]

        self.piece = None

    def test_fullrow(self):

        for y in range(self.y-1, -1, -1):
            cnt = 0
            for x in range(self.x):
                if self.ground[y][x] != 0:
                    cnt += 1

            if cnt == self.x:
                return y

            if cnt == 0:
                return None

    def delete_row(self, row=None):

        if row is not None:

            for y in range(row, 0, -1):
                for x in range(self.x):
                    self.ground[y][x] = self.ground[y-1][x]
            for x in range(self.x):
                self.ground[0][x] = 0

            self.merge_field()

        return row

    def merge_field(self):

        for x in range(self.x):
            for y in range(self.y):
                self.field[y][x] = self.ground[y][x]

        if self.piece is not None:

            h = len(self.piece)
            w = len(self.piece[0])

            for x in range(w):
                for y in range(h):
                    if (self.piece[y][x] != 0) and (0 <= (x + self.px) < self.x) and (0 <= (y + self.py) < self.y):
                        self.field[y+self.py][x+self.px] = self.piece[y][x]

    def test_collision(self, piece=None, px=None, py=None):

        if piece is None:
            piece = self.piece
        if px is None:
            px = self.px
        if py is None:
            py = self.py

        if piece is None:
            return False

        h = len(piece)
        w = len(piece[0])

        for x in range(w):
            for y in range(h):
                if piece[y][x] != 0:
                    if not (0 <= (px + x) < self.x):
                        return True
                    if not (0 <= (py + y) < self.y):
                        return True
                    if self.ground[py+y][px+x] != 0:
                        return True

        return False
