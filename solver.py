import copy

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
    gw = len(ground[0])
    gh = len(ground)

    for x in range(pw):
        for y in range(ph):
            if (piece != 0):
                pxx = px + x
                pyy = py + y

                if ((pxx < 0) or (pyy < 0) or (pxx >= gw) or (pyy >= gh)):
                    #print(px, py, pw, ph, gw, gh, 'True outbound')
                    return True

                if ground[pyy][pxx] != 0:
                    #print(px, py, pw, ph, gw, gh, 'True')
                    return True

    #print(px, py, pw, ph, gw, gh, 'False')
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


def measure(field):

    width = len(field[0])
    height = len(field)

    weight: int = 0

    for y in range(height):

        cnt = 0
        for x in range(width):
            if field[y][x] != 0:
                cnt += 1
        row_weight = (height - y) * cnt
        print(y, cnt, row_weight)
        weight += row_weight

    return weight


def solve(field, piece, px, py, show=None):

    #print(px, py)

    if piece is None:
        return None

    width = len(field[0])
    height = len(field)

    possiblities = []
    weights = []

    original = []
    for y in range(len(piece)):
        original.append([])
        for x in range(len(piece[0])):
            original[-1].append(piece[y][x])

    orx = px
    ory = py

    ground = []
    for y in range(height):
        ground.append([])
        for x in range(width):
            ground[-1].append(field[y][x])

    #if show is not None:
    #    field = merge_field(ground, original, orx, ory)
    #    show(field, wait=500)

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
                #print('Rot {}, Shift {} NO'.format(rot, shift))
                continue  # cant use this shift (of the rotation)

            #if show is not None:
            #    field = merge_field(ground, test_piece, test_x, ory)
            #    show(field, wait=200)

            test_y = ory
            down = 0
            while test_collision(ground, test_piece, test_x, test_y + 1 + down) is not True:
                down += 1
            field = merge_field(ground, test_piece, test_x, test_y + down)
            weight = measure(field)
            print('Rot {}x, Shift {}x, Down {}x, Weight {}'.format(rot, shift, down, weight))
            possiblities.append([rot, shift, down])
            weights.append(weight)

    index = weights.index(min(weights))
    result = possiblities[index]
    print('Res: {} .. Rot {}x, Shift {}x, Down {}x, Weight {}'.format(index, result[0], result[1], result[2], weights[index]))
    if show is not None:
        for i in range(result[0]):
            original = rotate(original)
        x = orx + result[1]
        y = ory + result[2]
        print(x, y)
        field = merge_field(ground, original, x, y)
        print('measure', measure(field))
        show(field, wait=500)

    #print()
    #for p in possiblities:
    #    print(p)

    return result