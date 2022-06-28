import numpy as np

def optimal_res(matrix, step):
    rows, columns = matrix.shape[0], matrix.shape[1]

    # f - промежуточная матрица текущей целевой функции
    f = np.empty(rows)

    # g - матрица состояний
    g = np.zeros((rows,columns))
    g[0,:] = 0
    g[:,columns-1] = range(0,rows)

    # c - шаг для множества состояний
    c = 10 if (int(rows/10) == 0) else 100

    for j in range(columns-2, -1, -1):
        f[0:rows] = 0
        for i in range(rows):
            dec = i
            opt_step = c
            for inc in range(i+1):
                # уравнение Беллмана
                val = matrix[inc, j] + matrix[dec, j+1]
                if(val==f[i] and val!=0):
                    g[i,j] = inc*opt_step+g[i,j]
                    opt_step=opt_step*c
                if(val>f[i]):
                    f[i] = val
                    g[i,j] = inc
                    opt_step = c
                dec=dec-1
        matrix[:, j] = f[:]

    print("---matrix of objective functions---\n")
    print(np.fliplr(matrix), "\n")
    print("\n-----------state matrix------------\n")
    print(np.fliplr(g),"\n")

    print("\n-----optimal options to invest-----\n")
    opt_func(0, rows - 1, [], g, c, step, columns)
    print("\n-----------------------------------")

def opt_func(n, inext, invest, g, c, step, columns):
    for i in range(n, columns):
        imax = g[inext,i]
        while(int(imax/c)!=0):
            r = int(imax%c)
            i_next = int(inext - r)
            imax = int(imax/c)
            opt_func(i+1, i_next, invest+[step*r], g, c, step, columns)
        invest.append(int(step*imax))
        inext = int(inext - imax)
    print(invest)
