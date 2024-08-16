import itertools as it
import collections as col
import ast
import copy
import time
def Solved():
    # Gives the solved state in the notation that uses the rest of functions
    return([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18],[19,20,21],[22,23,24]])

def s2sList(st):
    # This function gets a state as an argument and returns a equivalent list of integers (instead of the list of lists that we use as states)
    s = copy.deepcopy(st)
    slist = []
    for i in s:
        for j in i:
            slist.append(j)
    return(slist)

def sList2s(slist1):
    # This function gets a list of integers and transforms it to a state (this function is the inverse of s2sList())
    slist = copy.deepcopy(slist1)
    s = []
    for i in [0,3,6,9,12,15,18,21]:
        s.append([slist[i],slist[i+1],slist[i+2]])
    return(s)

def Sol2Scr(sol):
    spSol = sol.split(' ')
    spSol.reverse()
    scr = [0]*len(spSol)
    k = 0
    for i in spSol:
        if "2" in i:
            scr[k] = i
        elif "'" in i:
            scr[k] = i.replace("'",'')
        else:
            i = i + "3"
            scr[k] = i
        k = k + 1
    return(scr)
