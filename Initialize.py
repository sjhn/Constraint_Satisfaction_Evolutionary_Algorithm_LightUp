import numpy as np

# import matplotlib.pyplot as plt
from reading import config_reader, board_reader
from runners import evaluations_runner
from writing import write_solution


def init(config_file,problem_file):

    with open(config_file) as d:
        black_cell_constraint, logs, evals, solution_file_pathname, l = config_reader(d)
    # solution file
    o = open(solution_file_pathname, "w+")
    # input file
    with open(problem_file) as f:

        frl = f.readline()
        x = int(frl)
        o.write(frl)

        frl = f.readline()
        y = int(frl)
        o.write(frl)

        print(int(x))
        print(y)

        board, bc_board, black_list, bc, wc = board_reader(x, y, f, o)

    # counting the number of the black cells

    log_sol = []
    # A list for saving each log's best fitness
    log_fit = np.zeros([logs])
    # the fittest solution of all in an experiment
    max_fit = 0

    for i in range(logs):
        print('log:' + str(i))
        best_fitness = 0
        fitness_hist = np.zeros([evals + 1])  # fitness history for plotting
        sol_hist = []  # for saving the best solutions so far at each run
        # c = 0

        # for k in range(evals):
        k = 0
        l.write('\n' + 'Run' + str(i))

        sol_hist, best_fitness, max_fit = evaluations_runner(max_fit, best_fitness, l, x, y, evals, wc, board,
                                                                      fitness_hist, sol_hist, bc_board, black_list,
                                                                    black_cell_constraint)

        if len(sol_hist) > 0:
            log_sol.append(sol_hist[len(sol_hist) - 1])
        log_fit[i] = best_fitness

    l.write('\n')
    max_sol=sol_hist[len(sol_hist)-1]
    print(max_sol)
    print(max_fit)
    write_solution(o, max_sol, max_fit, x, y)

    return log_sol

    ##plt.plot(fitness_hist,'.')
    ##plt.show()
