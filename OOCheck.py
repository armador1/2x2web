import ast
from TranslatedSolver import fixCorner, TranslateStList
import _2x2Main as main

file = open('ooc.csv','r')
checked = open('checked.txt','w')
next(file)
for a in file:
    control = 0
    broken = 0
    info = a.split(']",')
    statel = ast.literal_eval(info[0]+']"')
    state = ast.literal_eval(statel)
    oo = info[1]
    sol = oo.split(' ')
    sol = [move.strip() for move in sol]

    # print(state)
    # print(oo)
    states = [0]*24
    states[0] = state
    rots = [None,'z','z','z','x','z','z','z','x','z','z','z'
            ,"x3",'z','z','z',"x3",'z','z','z','x','z','z','z']
    
    for i in range(1,24):
        rot = getattr(main, rots[i])
        # print(type(states[i-1]))
        states[i] = fixCorner(TranslateStList(main.s2sList(rot(main.sList2s(states[i-1])))))
    for i in range(0,24):

        dummy = main.sList2s(states[i])
        # print(dummy)
        # print(dummy)
        for k in range(0,len(sol)):
            sol[k]=sol[k].replace("'",'3')
            try:
                # print(sol[k])
                move = getattr(main, sol[k])
                dummy = move(dummy)
            except Exception as error:
                # print(error)
                broken = 1
                break
        # print(dummy)
        if broken == 1:
            break
        if main.sList2s(fixCorner(TranslateStList(main.s2sList(dummy)))) == main.Solved():
            new_st = states[i]
            try:
                rotf = ''
                rotlist = rots[1:i+1]
                for k in rotlist:    
                    add = k.replace('3','xx')
                    rotf = rotf + add
            except Exception as error:
                rotf = ''
            print(rotf)
            checked.write("%s\t" % str(state))
            checked.write("%s\t" % str(new_st))
            checked.write("%s\t" % rotf)
            checked.write("%s" % oo)
            control=1
            break
    if control == 0:
        # print(broken)
        checked.write("Invalid OO\n")
        # print('OO inválido')

    
