import numpy as np


def TranslateStList(s):
    st = s.copy()
    dic = [9, 6, 0, 3, 4, 8, 17, 19, 1, 5, 14, 16, 12, 15, 21, 18, 10, 2, 23, 13, 7, 11, 20, 22]
    newst = [0]*24
    for i in range(0, 24):
        newst[i] = st[dic[i]]

    newst2 = [0]*24
    for i in [1,4,7,10]:
        ind = newst.index(i)
        newst2[ind] = 0
    for i in [5,9,18,20]:
        ind = newst.index(i)
        newst2[ind] = 1
    for i in [2,6,15,17]:
        ind = newst.index(i)
        newst2[ind] = 2
    for i in [13,16,19,22]:
        ind = newst.index(i)
        newst2[ind] = 3
    for i in [3,11,14,24]:
        ind = newst.index(i)
        newst2[ind] = 4
    for i in [8,12,21,23]:
        ind = newst.index(i)
        newst2[ind] = 5
    newstnp = np.array(newst2)
    return newstnp
