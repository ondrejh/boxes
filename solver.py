def rotate(piece, side='L'):

    w = len(piece[0])
    h = len(piece)

    new_piece = []

    for y in range(w):
        new_piece.append([])
        for x in range(h):
            if side != 'L':
                new_piece[-1].append(piece[h - 1 - x][y])
            else:
                new_piece[-1].append(piece[x][w - 1 - y])

    return new_piece


def test_collision(ground, piece, px, py):

    pw = len(piece[0])
    ph = len(piece)

    for x in range(pw):
        for y in range(ph):
            pxx = px + x
            pyy = py + y

            if ((pxx < 0) or (pyy < 0)) and (piece[y][x] != 0):
                return True

            try:
                if (piece[y][x] != 0) and (ground[pyy][pxx] != 0):
                    return True
            except IndexError:
                return True

    return False


def merge_field(ground, piece, px, py):

    gw = len(ground[0])
    gh = len(ground)

    field = []

    for y in range(gh):
        field.append([])
        for x in range(gw):
            field[-1].append(1 if (ground[y][x] != 0) else 0)

    pw = len(piece[0])
    ph = len(piece)

    for y in range(ph):
        for x in range(pw):
            try:
                if piece[y][x]:
                    field[y+py][x+px] = 2
            except IndexError:
                print('Solver merge error: {} {} <- {} {}'.format(y+py, x+px, y, x))

    return field


def solve(field, piece, px, py, show=None):

    width = len(field[0])
    height = len(field)

    original = []
    for y in range(len(piece)):
        original.append([])
        for x in range(len(piece[0])):
            original[-1].append(piece[y][x])

    orx = px
    ory = py

    ground = []
    for y in range(len(field)):
        ground.append([])
        for x in range(len(field[0])):
            ground[-1].append(field[y][x])

    if show is not None:
        field = merge_field(ground, original, orx, ory)
        show(field, wait=500)

    for rot in range(4):

        test_piece = []
        for y in range(len(original)):
            test_piece.append([])
            for x in range(len(original[0])):
                test_piece[-1].append(original[y][x])

        noway = False
        for i in range(rot):
            test_piece = rotate(test_piece)
            if test_collision(ground, test_piece, orx, ory):
                noway = True
                break
        if noway:
            continue  # cant use this rotation

        for shift in range(-width, width):

            test_x = orx + shift
            if test_collision(ground, test_piece, test_x, ory):
                print('Rot {}, Shift {} NO'.format(rot, shift))
                continue  # cant use this shift (of the rotation)

            #if show is not None:
            #    field = merge_field(ground, test_piece, test_x, ory)
            #    show(field, wait=200)

            for i in range(len(field)):
                test_y = ory + i + 1
                if test_collision(ground, test_piece, test_x, test_y):
                    test_y -= 1
                    print('Rot {}x, Shift {}x, Down {}x'.format(rot, shift, i))
                    # test result here

                    if show is not None:
                        field = merge_field(ground, test_piece, test_x, test_y)
                        show(field, wait=200)
                    break  # goto next shift
