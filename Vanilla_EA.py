import random
from sys import argv

import numpy as np
import matplotlib.pyplot as plt

from Validation import random_bulb_placement, fitness_check
from mating import mate
from reading import config_reader, board_reader
from writing import write_solution


def main():
    if len(argv) == 3:
        print('The problem file passed is: {argv[1]}')
        print('The config file passed is: {argv[2]}')
        problem_file = argv[1]
        config_file = argv[2]
    elif len(argv) == 2:
        # print('oj')
        print('The problem file passed is: {argv[1]}')
        print('Using the default config file since none was specified!')
        problem_file = argv[1]
        config_file = 'Config.yaml'
    else:
        print('An inappropriate number of arguments were passed!')

    d = open(config_file)
    black_cell_constraint, logs, evals, solution_file_pathname, l, mu, lambdaa, generations, sbc, stp, runs, penalty, mutation_probability, parent_selection = config_reader(
        d)
    print(runs)
    # solution file
    o = open(solution_file_pathname, "w+")
    # input file
    f = open(problem_file)

    frl = f.readline()
    x = int(frl)
    o.write(frl)

    frl = f.readline()
    y = int(frl)
    o.write(frl)

    print(int(x))
    print(y)

    board, bc_board, black_list, bc, wc = board_reader(x, y, f, o)
    print('Maximum fitness possible+\t' + str(wc))
    conf = open(config_file)

    best_fitness_of_each_run=[]
    for r in range(1, runs + 1):

        evaualations_so_far = 0

        average_list = []
        fittest_list = []
        initial_pool = []
        # mulan=mu+lambdaa

        for i in range(mu):
            valid, fitness, lightened, r_b = random_bulb_placement(black_cell_constraint,
                                                                   bc_board, board, x, y, black_list, wc)
            if evaualations_so_far<evals:
                initial_pool.append([r_b, fitness])
                evaualations_so_far+=1
        #print(evaualations_so_far)
        pool = initial_pool.copy()

        l.write('\n' + 'run ' + str(r))
        #print('run: ' + str(r))
        for h in range(1,generations+1):
            if evaualations_so_far<evals:
                #print('generation:', h)

                for num in range(lambdaa):
                    if parent_selection == 'uniform_random':
                        p1 = random.randint(0, len(pool) - 1)
                        p2 = random.randint(0, len(pool) - 1)
                        # print(p1,'p1')
                        # print(len(pool))
                        parent1 = pool[p1]
                        # print(parent1)
                        parent2 = pool[p2]
                    else:
                        if parent_selection == 'Fitness_Proportional_Selection':
                            elements = [f[0] for f in pool]
                            fitnesses = [f[1] for f in pool]
                            #print(len(fitnesses))
                            if np.sum(fitnesses)!=0:
                                probabilities = fitnesses / np.sum(fitnesses)
                            else:
                                probabilities=np.ones(len(fitnesses)) / len(fitnesses)
                            #print(len(probabilities))
                            #p1 = np.random.choice(elements, 1, p=probabilities)
                            #p2 = np.random.choice(elements, 1, p=probabilities)

                            parent1=random.choices(elements, weights=fitnesses, k=1)
                            parent2=random.choices(elements, weights=fitnesses, k=1)
                            #parent1 = elements[p1]
                            #parent2 = elements[p2]

                    child = mate(parent1, parent2, mutation_probability)
                    fitness = fitness_check(child, black_cell_constraint, bc_board, black_list, not sbc, penalty)[1]
                    evaualations_so_far+=1
                    # print(fitness)
                    pool.append([child, fitness])


                pool = sorted(pool, key=lambda x: x[1])[-mu:]
                #print(pool[-1][1])
                # print('average fitness:', (pool, lambda x: x[1][:]))
                sum = 0
                for t in range(len(pool)):
                    # print(pool[t][1])
                    sum += pool[t][1]
                # print('average:',sum/len(pool))
                avg = sum / len(pool)
                average_list.append(avg)
                fittest_list.append(pool[-1][1])
                l.write('\n' + str(mu + lambdaa * h) + '\t' + str(avg) + '\t' + str(pool[-1][1]))

        best_fitness_of_each_run.append(pool[-1][1])
        print('run'+str(r)+'\t'+str(pool[-1][1]))
        #print(evaualations_so_far)
    write_solution(o, pool[-1][0], pool[-1][1], x, y)
    print('runs fitnesses',best_fitness_of_each_run)
    plt.plot(average_list)
    ## plt.show()
    plt.plot(fittest_list)
    plt.ylabel('fitness')
    plt.xlabel('evaluation')
    plt.title('mu:' + str(mu) + '\t' + 'lambda:' + str(lambdaa) + '\n' + 'black constraint considered:'
    + str(black_cell_constraint) + '\n' + 'generations: ' + str(
    generations) + '\t' + 'black constraint penalty in fitness:' + str(sbc))
    ## plt.figtext('figtext')
    plt.show()
    plt.close()


if __name__ == '__main__':
    main()
