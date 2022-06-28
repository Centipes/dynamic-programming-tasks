import numpy as np
import math

def optimal_res(matrix, step, x, y):
    rows, columns = matrix.shape[0], matrix.shape[1]

    # f и g - промежуточная матрица текущей целевой функции
    f = np.zeros((x+1,y+1))
    g = np.zeros((x+1,y+1))
    f[0,:] = matrix[0:y+1,0]
    f[:,0] = matrix[0:x+1,0]

    # c - шаг для множества состояний
    c = 10 if (int(max(x,y)/10)==0) else 100
#-------------------------------------------
    for i in range(1,x+1):
        for j in range(1,y+1):
            f[i,j] = max(f[i,0], f[0,j])

    if(x>y):
        f[y+1:x+1,:] = f[y+1:x+1,0:1]
    elif(x<y):
        f[:,x+1:y+1] = f[0,x+1:y+1]
#--------------------------------------------
    # cond_x и cond_y - матрицы состояний для ресурсов х и y соответсвенно
    cond_x = []
    cond_y = []

    for i in range(1,columns):
        array = np.empty((x+1,y+1))
        array[0,0] = 0
        array[1:,:] = math.inf
        array[:,1:] = math.inf
        cond_y.append(array)
    for i in range(1,columns):
        array = np.empty((x+1,y+1))
        array[0,0] = 0
        array[1:,:] = math.inf
        array[:,1:] = math.inf
        cond_x.append(array)

#--------------------------------------------
    f_y = np.empty(y+1)
    f_x = np.empty(y+1)

    for k in range(1,columns):
        for i in range(x+1):
            f_y[0:y+1] = 0
            f_x[0:y+1] = 0
            for j in range(y+1):
                dec_y = j
                dec_x = i
                opt_step_x = c
                opt_step_y = c
                for inc in range(j+1):
                    val_y = matrix[inc,k] + f[i,dec_y]
                    if(val_y==f_y[j]):
                        cond_y[k-1][i,j] = inc*opt_step_y + cond_y[k-1][i,j]
                        opt_step_y=opt_step_y*c
                    elif(val_y>f_y[j]):
                        f_y[j] = val_y
                        cond_y[k-1][i,j] = inc
                        opt_step_y = c
                    dec_y = dec_y-1
                for inc in range(i+1):
                    val_x = matrix[inc,k] + f[dec_x,j]
                    if(val_x == f_x[j]):
                        cond_x[k-1][i,j] = inc*opt_step_x + cond_x[k-1][i,j]
                        opt_step_x = opt_step_x*c
                    elif(val_x>f_x[j]):
                        f_x[j] = val_x
                        cond_x[k-1][i,j] = inc
                        opt_step_x = c
                    dec_x = dec_x-1

            for z in range(y+1):
                if(f_x[z]>f_y[z]):
                    g[i,z] = f_x[z]
                    cond_y[k-1][i,z] = math.inf
                elif(f_y[z]>f_x[z]):
                    g[i,z] = f_y[z]
                    cond_x[k-1][i,z] = math.inf
                else:
                    g[i,z] = f_y[z]

        f = g.copy()

    print("---matrix of objective functions---\n")
    print(g, "\n")
    print("\n-----------state matrix y------------\n")
    print(cond_y, "\n")
    print("\n-----------state matrix x------------\n")
    print(cond_x, "\n")
    print("\n-----optimal options to invest-----\n")
    opt_func(columns-2, x, y, [], cond_x, cond_y, c, step, columns)

def opt_func(n, inext_x, inext_y, invest, g_x, g_y, c, step, col):
    for i in range(n, -1, -1):
        o_opt = False
        imax_x = g_x[i][inext_x,inext_y]
        imax_y = g_y[i][inext_x,inext_y]

        n_invest_y = invest.copy()
        n_invest_x = invest.copy()

        if(imax_y!=math.inf):
            while(int(imax_y/c)!=0):
                o_opt = True
                r = int(imax_y%c)
                i_next_y = int(inext_y - r)
                imax_y = int(imax_y/c)
                opt_func(i-1, inext_x, i_next_y, n_invest_y+[(0,step*r)], g_x, g_y, c, step, col)
            invest = n_invest_y
            invest.append((0, int(step*imax_y)))
            if(o_opt and len(invest) < col-1):
                o_opt = False
                opt_func(i-1, inext_x, int(inext_y-imax_y), invest, g_x, g_y, c, step, col)

        if(imax_x!=math.inf):
            while(int(imax_x/c)!=0):
                r = int(imax_x%c)
                i_next_x = int(inext_x - r)
                imax_x = int(imax_x/c)
                opt_func(i-1, i_next_x, inext_y, n_invest_x+[(0,step*r)], g_x, g_y, c, step, col)
            invest = n_invest_x
            invest.append((int(step*imax_x), 0))

        if(invest == n_invest_x):
            inext_x = int(inext_x - imax_x)
        elif(invest == n_invest_y):
            inext_y = int(inext_y - imax_y)


    if(inext_x == 0):
        invest.append((0, int(step*inext_y)))
    else:
        invest.append((int(step*inext_x), 0))
    print(invest[::-1])
