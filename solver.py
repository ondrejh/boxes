from play import rotate, test_collision, merge_field

ROW_WEIGHT = 1
HOLLOW_WEIGHT = 5
FULL_ROW_WEIGHT = 3


def measure(field):

    width = len(field[0])
    height = len(field)

    weight: int = 0 # total weight of field (will be calculated)

    for y in range(height):

        row = 0 # how many boxes in row
        hollows = 0 # how many hollows in row
        filled = True # is the row filled?

        for x in range(width):
            if field[y][x] != 0:
                row += 1
            else:
                filled = False

                #  find hoolows
                for yy in range(y):
                    if field[yy][x] != 0:
                        hollows += 1

        if filled: # if filled subtract weight
            row_weight = -(row * FULL_ROW_WEIGHT)
        else: # if not filled add weight plus hollows
            row_weight = (height - y) * row * ROW_WEIGHT + (height - y) * hollows * HOLLOW_WEIGHT

        # print(y, cnt, row_weight)
        weight += row_weight # add row weight to total weight

    return weight


def solve(field, piece, px, py, show=None):

    # print(px, py)

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

    # if show is not None:
    #    field = merge_field(ground, original, orx, ory)
    #    show(field, wait=500)

    for rot in range(4):

        test_piece = []
        for y in range(len(original)):
            test_piece.append([])
            for x in range(len(original[0])):
                test_piece[-1].append(original[y][x])

        if test_collision(ground, test_piece, orx, ory):
            return None

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
                # print('Rot {}, Shift {} NO'.format(rot, shift))
                continue  # cant use this shift (of the rotation)

            # if show is not None:
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
            # if show is not None:
            #    field = merge_field(ground, test_piece, test_x, test_y + down)
            #    show(field, wait=200)

    index = weights.index(min(weights))
    result = possiblities[index]
    print('Res: {} .. Rot {}x, Shift {}x, Down {}x, Weight {}'.format(index, result[0], result[1], result[2],
                                                                      weights[index]))
    if show is not None:
        for i in range(result[0]):
            original = rotate(original)
        x = orx + result[1]
        y = ory + result[2]
        print(x, y)
        field = merge_field(ground, original, x, y, bg=7, fg=2)
        print('measure', measure(field))
        show(field, wait=1000)

    # print()
    # for p in possibilities:
    #    print(p)

    return result