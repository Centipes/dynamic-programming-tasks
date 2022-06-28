import numpy as np

def optimal_res(matrix, step, per1, per2, years):
    rows, columns = matrix.shape[0], matrix.shape[1]
    f = np.empty(rows)
    s = np.empty((rows, years+1))
    g = np.empty((rows, years))
    g[:,0] = 0
    g[0,:] = 0
    s[:,0] = 0

    # c - шаг для множества состояний
    c = 10 if (int(rows/10) == 0) else 100

    for j in range(1,years+1):
        f[0:rows] = 0
        for i in range(rows):
            dec = i
            opt_step = c
            for inc in range(i+1):
                interpol = int((per1*inc + per2*dec)*step)
                index = interpol/step
                rem = interpol%step
                if(rem!=0):
                    num = s[int(index),j-1]+((s[int(index+1),j-1]-s[int(index),j-1])*(index-int(index)))
                else:
                    num = s[int(index),j-1]
                val = matrix[inc, 0] + matrix[dec, 1] + num
                if(val==f[i]):
                    g[i,j-1] = inc*opt_step+g[i,j-1]
                    opt_step = opt_step*c
                elif(val>f[i]):
                    f[i] = val
                    g[i,j-1] = inc
                    opt_step = c
                dec=dec-1
        s[:,j] = f[:]

    print("---matrix of objective functions---\n")
    print(s, "\n")
    print("\n-----------state matrix------------\n")
    print(g, "\n")
    print("\n-----optimal options to invest-----\n")
    opt_func(0, rows - 1, [], np.fliplr(g), c, step, years, per1, per2)
    print("\n-----------------------------------")

def opt_func(n, inext, invest, g, c, step, columns, per1, per2):
    rem = inext*step
    for i in range(n, columns):
        imax = g[inext,i]
        while(int(imax/c)!=0):
            r = int(imax%c)
            i_next = int(inext - r)
            imax = int(imax/c)
            opt_func(i+1, i_next, invest+[step*r], g, c, step, columns)
        a = step*imax
        b = rem-a
        rem = a*per1 + b*per2
        invest.append((a, b))
        inext = int(rem/step)
    print(invest)
