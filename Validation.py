import random

import numpy as np


def random_bulb_placement(black_cell_constraint, bc_board,
                          board, x, y, black_list, wc):
    bc_board_random = np.zeros_like(board)
    random_board = board.copy() * 2
    bc_board_random = np.zeros_like(board)
    lightened = board.copy() * 2
    random_lamps = random.randint(0, wc)
    # print('bulb placement called')
    j = 0
    fitness = 0
    valid = 1
    while j < random_lamps and valid == 1:

        # print(random_board)
        # print('j',j)
        # print(black_list)
        r1 = random.randint(0, x - 1)
        r2 = random.randint(0, y - 1)

        if random_board[r1, r2] == 0:

            # print('New lamp at:', r1, r2)
            # bulb cells are marked with 7
            random_board[r1, r2] = 7
            j += 1
            # updating the lightened area
            s = r1 + 1
            t = r2
            # print('J increased')
            if black_cell_constraint:

                oi = max(0, r1 - 1)
                io = min(x - 1, r1 + 1)

                oj = max(0, r2 - 1)
                jo = min(y - 1, r2 + 1)

                bc_board_random[r1, oj] += 1
                bc_board_random[r1, jo] += 1
                bc_board_random[io, r2] += 1
                bc_board_random[oi, r2] += 1

                for blk in black_list:
                    # print('this')
                    if valid > 0:
                        if bc_board[blk[0], blk[1]] < bc_board_random[blk[0], blk[1]]:
                            valid = 0
                            fitness = 0
                            # print(random_board)
                            # print(bc_board_random)
                            # print('invalid!!! at:',blk[0],blk[1],bc_board[blk[0],blk[1]],bc_board_random[blk[0],blk[1]])
                            j = random_lamps
                            # print('j reached')

                # print(r1,r2,oi,io,oj,jo)

            valid, fitness, lightened = light_validity_check_and_fill(fitness, s, x, y, random_lamps, random_board,
                                                                      lightened,
                                                                      r1, r2, board)
            t = r2
            # marking the lamps with 7 in
            # lightened matrix
            lightened[r1][r2] = 7
            fitness += 1

    if black_cell_constraint:

        for blk in black_list:

            if valid > 0:
                if bc_board[blk[0], blk[1]] != bc_board_random[blk[0], blk[1]]:
                    valid = 0
                    fitness = 0
                    # print(random_board)
                    # print(bc_board_random)
                    # print('invalid!!! at:',blk[0],blk[1],bc_board[blk[0],blk[1]],bc_board_random[blk[0],blk[1]])
                    # j = random_lamps
    if valid == 0:
        fitness = 0
    return valid, fitness, lightened,random_board


def light_validity_check_and_fill(fitness, s, x, y, random_lamps, random_board, lightened, r1, r2, board):
    # print('light val called')
    valid = 1


    while s < x and board[s][r2] != 1:

        if random_board[s][r2] == 7:

            valid = 0
            fitness = 0
            # print('The new lamp lightens cell:', s, r2)
            j = random_lamps

        else:
            if lightened[s][r2] == 0:
                fitness += 1
            lightened[s][r2] = 1
        s += 1

    s = r1 - 1

    while s > -1 and board[s][r2] != 1:

        if random_board[s][r2] == 7:

            valid = 0
            fitness = 0
            # print('The new lamp lightens cell:', s, r2)
            j = random_lamps
        else:
            if lightened[s][r2] == 0:
                fitness += 1
            lightened[s][r2] = 1

        s -= 1

    s = r1
    t = r2 + 1

    while t < y and board[r1][t] != 1:

        if random_board[r1][t] == 7:

            valid = 0
            fitness = 0
            # print('The new lamp lightens cell:', r1, t)
            # break
            j = random_lamps
        else:
            if lightened[r1][t] == 0:
                fitness += 1
            lightened[r1][t] = 1

        t += 1

    t = r2 - 1

    while t > -1 and board[r1][t] != 1:

        if random_board[r1][t] == 7:

            valid = 0
            fitness = 0
            # print('The new lamp lightens cell:', r1, t)
            j = random_lamps
        else:
            if lightened[r1][t] == 0:
                fitness += 1
            lightened[r1][t] = 1

        t -= 1

    return valid, fitness, lightened


def fitness_check(random_board,black_cell_constraint,bc_board,black_list, classic_fitness,penalty):
    valid = 1
    fitness = 0
    lightened = random_board.copy()
    #bc_board_random=random_board.copy()
    bc_board_random=np.zeros_like(random_board)
    x = random_board.shape[0]
    y = random_board.shape[0]

                    # print(random_board)
                    # print(bc_board_random)
                    #

    # print('light val called')
    #print(random_boa)
    #print('b',board)


    for r1 in range(x):
        for r2 in range(y):
            if random_board[r1][r2] == 7:
                fitness+=1
                s=r1+1
                while s < x and random_board[s][r2] != 2:

                    if random_board[s][r2] == 7:

                        valid = 0
                        fitness -= penalty
                        if black_cell_constraint:
                            fitness=0


                    else:
                        if lightened[s][r2] == 0:
                            fitness += 1
                        lightened[s][r2]=1
                    s += 1

                s = r1 - 1

                while s > -1 and random_board[s][r2] != 2:

                    if random_board[s][r2] == 7:

                        valid = 0
                        fitness -= penalty
                        if black_cell_constraint:
                            fitness=0

                    else:
                        if lightened[s][r2] == 0:
                            fitness += 1
                        lightened[s][r2]=1
                    s -= 1

                s = r1
                t = r2 + 1

                while t < y and random_board[r1][t] != 2:

                    if random_board[r1][t] == 7:

                        valid = 0
                        fitness -= penalty
                        if black_cell_constraint:
                            fitness=0

                    else:
                        if lightened[r1][t] == 0:
                            fitness += 1
                        lightened[r1][t]=1
                    t += 1

                t = r2 - 1

                while t > -1 and random_board[r1][t] != 2:

                    if random_board[r1][t] == 7:

                        valid = 0
                        fitness -= penalty
                        if black_cell_constraint:
                            fitness=0

                    else:
                        if lightened[r1][t] == 0:
                            fitness += 1
                        lightened[r1][t]=1
                    t -= 1

    if black_cell_constraint and valid >0:
        for r1 in range(x):
            for r2 in range(y):
                if random_board[r1][r2]==7:
                    oi = max(0, r1 - 1)
                    io = min(x - 1, r1 + 1)

                    oj = max(0, r2 - 1)
                    jo = min(y - 1, r2 + 1)

                    bc_board_random[r1, oj] += 1
                    bc_board_random[r1, jo] += 1
                    bc_board_random[io, r2] += 1
                    bc_board_random[oi, r2] += 1



        for blk in black_list:
            # print('this')
            bcv=0 #black constraint violation
            if bc_board[blk[0], blk[1]] != bc_board_random[blk[0], blk[1]]:
                if bc_board[blk[0],blk[1]]!=5:

                    if classic_fitness:
                        valid=0
                        fitness=0
                    else:
                    #bcv+=1
                    #valid = 0
                        fitness -= penalty
                    #print(blk[0], blk[1], bc_board[blk[0],blk[1]],'!=',bc_board_random[blk[0],blk[1]])
                    #print(bc_board)
                    #print(bc_board_random)
                    #print(lightened)
    if valid==0 and penalty ==0:
        fitness=0

    #print('valid',valid)
    #print('fitness',fitness)

    #print('lightened)fitness check')
    #print(lightened)
    return valid, fitness, lightened
