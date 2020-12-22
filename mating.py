import numpy as np
import random
def mate (parent_a, parent_b, mutation_probability):

    x=parent_a[0].shape[0]
    ar1=np.array(parent_a)[0][:][:x//2].astype(int)
    ar2=np.array(parent_b)[0][x//2:].astype(int)
    child = np.concatenate((ar1,ar2),axis=0)

    r=random.random()

    if r<mutation_probability:


        placed=False

        while not placed:
            a = random.randint(0, x-1)
            b = random.randint(0, x-1)

            if child[a][b] !=2 :
                child[a][b] =7
                #print(child)
                placed=True
                #print('mutated')

    return child