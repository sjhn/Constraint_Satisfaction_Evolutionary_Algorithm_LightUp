import random
import numpy as np

from Validation import random_bulb_placement


def evaluations_runner(max_fit, best_fitness,l,x,y, evals, wc, board, fitness_hist, sol_hist, bc_board, black_list, black_cell_constraint):
    k=0
    #max_sol=board.copy()*2
    while k < evals:

        # generating a uniform number for the number of lamps
        random_lamps = random.randint(0, wc)
        # for random bulb placement
        random_board = board.copy() * 2
        # the lightened area
        lightened = board.copy()
        lightened *= 2
        bc_board_random = np.zeros_like(board)

        valid, fitness,lightened = random_bulb_placement(random_lamps, random_board, black_cell_constraint, bc_board_random, lightened,
                                        bc_board,
                                        board, x, y, black_list)
        #max_sol=random_board.copy()

        if fitness > best_fitness:
            #print(fitness,best_fitness)

            best_fitness = fitness
            fitness_hist[k] = fitness
            sol_hist.append(lightened)
            #c += 1
            l.writelines(['\n' + str(k) + '\t' + str(fitness), ' '])
            #print(fitness,max_fit)
            #if fitness > max_fit:
                #print(fitness,lightened)
                #max_fit = fitness
                #max_sol = lightened.copy()
                #print(max_sol)

        if valid != 0:
            k += 1


    return sol_hist, best_fitness, max_fit