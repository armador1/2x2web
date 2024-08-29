import numpy as np

def OppColors(color):
    opp = [3,4,5,0,1,2]
    return opp[color]

def getCorner(n, st):
    corners = [[0,21,16],[1,5,20],[2,17,8],[3,9,4],[12,10,19],[13,6,11],[14,18,23],[15,7,22]]
    return [st[corners[n][0]],st[corners[n][1]],st[corners[n][2]]]

def fixCorner(st):
    f_corner = [OppColors(getCorner(6,st)[0]),OppColors(getCorner(6,st)[1]),OppColors(getCorner(6,st)[2])] + getCorner(6,st)
    # print(f_corner)
    # for n in [0,1,2,3,4,5,7]:
    #     if len(set(getCorner(n,st)) & set(f_corner)) == 2:
    #         for i in getCorner(6,st):
    #             if i not in getCorner(n,st):
    #                 m1 = OppColors(f_corner.index(i))
    #         for i in getCorner(n,st):
    #             if i not in f_corner:
    #                 m2 = i
    #         f_corner[m1] = m2
    #     else:
    #         continue
    # if None in f_corner:
    #     for i in [0,1,2,3,4,5]:
    #         if i not in f_corner:
    #             f_corner[f_corner.index(None)] = i
    #             break
    # return f_corner
    
    new_st = st.copy()
    for i in range(0,len(new_st)):
        new_st[i] = f_corner.index(st[i])
    print(antiTranslateStList(new_st))
    return antiTranslateStList(new_st)
    




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

def antiTranslateStList(s):
    m0 = [[0,4,5],[0,5,1],[0,2,4],[0,1,2],[3,4,2],[3,2,1],[3,5,4],[3,1,5]]
    m1 = [[0,4,5],[0,1,5],[0,2,4],[0,1,2],[2,3,4],[1,2,3],[3,4,5],[1,3,5]]
    m2 = [[10,11,12],[7,8,9],[1,2,3],[4,5,6],[13,14,15],[16,17,18],[22,23,24],[19,20,21]]
    t_st = [0]*24
    for n in range(0,8):
        corner2sub = m2[n]
        a = getCorner(n,s)
        a.sort()
        pos = m1.index(a)
        if getCorner(n,s)[0] == m0[pos][0]:
            p = 0
        elif getCorner(n,s)[0] == m0[pos][1]:
            p = 1
        elif getCorner(n,s)[0] == m0[pos][2]:
            p = 2
        for k in range(0,3):
            t_st[corner2sub[k]-1] = m2[pos][(k+p)%3]
    return t_st
        
# print(fixCorner(TranslateStList([10, 11, 12, 23, 24, 22, 8, 9, 7, 4, 5, 6, 16, 17, 18, 19, 20, 21, 2, 3, 1, 13, 14, 15])))
# print(antiTranslateStList(TranslateStList([4, 5, 6, 10, 11, 12, 23, 24, 22, 8, 9, 7, 13, 14, 15, 16, 17, 18, 19, 20, 21, 2, 3, 1])))