
def write_solution(o,max_sol,max_fit,x,y):
    o.writelines(['\n'])
    o.writelines(str(max_fit))
    for i in range(x):
        for j in range(y):
            if max_sol[i][j] == 7:
                o.writelines(' ')
                o.writelines(['\n' + str(i + 1) + ' ' + str(j + 1), ' '])



