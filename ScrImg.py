import cv2 as cv
import numpy as np
import TranslatedSolver as tr
import _2x2Main as main
import ast
import hashlib

def generate_image_name(state):
    state_str = str(state)
    return hashlib.md5(state_str.encode()).hexdigest() + ".png"


def st2img(statel): # (B,G,R)
    if type(statel) == str:
        state = ast.literal_eval(statel)
    else:
        state = statel

    st = tr.TranslateStList(state)
    ind2col = [(255,255,255), (0,0,255), (0,255,0), (0,255,255),  (0,128,255), (255,0,0)]
    auxl = 501
    scr = np.zeros((auxl, auxl, 3), dtype='uint8')
    scr[:]=255,150,0
    marg = auxl//10
    sep = auxl//20
    lenf = auxl//6
    mid = auxl//2+1
    # Líneas externas de las caras
    cv.rectangle(scr, (marg,mid-lenf//2), (marg+lenf,mid+lenf//2), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+lenf+sep,mid-lenf//2), (marg+2*lenf+sep,mid+lenf//2), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+lenf+sep,mid-lenf//2-sep-lenf), (marg+2*lenf+sep,mid+lenf//2-sep-lenf), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+lenf+sep,mid-lenf//2+sep+lenf), (marg+2*lenf+sep,mid+lenf//2+sep+lenf), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+2*lenf+2*sep,mid-lenf//2), (marg+3*lenf+2*sep,mid+lenf//2), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+3*lenf+3*sep,mid-lenf//2), (marg+4*lenf+3*sep,mid+lenf//2), (0,0,0), thickness=3)


    # Líneas horizontales
    cv.line(scr, (marg,mid), (marg+lenf,mid), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep,mid), (marg+2*lenf+sep,mid), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep,mid+sep+lenf), (marg+2*lenf+sep,mid+sep+lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep,mid-sep-lenf), (marg+2*lenf+sep,mid-sep-lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+2*lenf+2*sep,mid), (marg+3*lenf+2*sep,mid), (0,0,0), thickness=3)
    cv.line(scr, (marg+3*lenf+3*sep,mid), (marg+4*lenf+3*sep,mid), (0,0,0), thickness=3)

    # Líneas verticales
    cv.line(scr, (marg+lenf//2,mid-lenf//2), (marg+lenf//2,mid+lenf//2), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep+lenf//2,mid-lenf//2), (marg+lenf+lenf//2+sep,mid+lenf//2), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep+lenf//2,mid-lenf//2-sep-lenf), (marg+lenf+sep+lenf//2,mid+lenf//2-sep-lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep+lenf//2,mid-lenf//2+sep+lenf), (marg+lenf+sep+lenf//2,mid+lenf//2+sep+lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+2*lenf+2*sep+lenf//2,mid-lenf//2), (marg+2*lenf+2*sep+lenf//2,mid+lenf//2), (0,0,0), thickness=3)
    cv.line(scr, (marg+3*lenf+3*sep+lenf//2,mid-lenf//2), (marg+3*lenf+3*sep+lenf//2,mid+lenf//2), (0,0,0), thickness=3)


    # Stickers
    
    # Cara 0
    cv.rectangle(scr, (marg+lenf+sep+3,mid-sep-lenf-lenf//2+3), (marg+lenf+sep+lenf//2-3,mid-sep-lenf-3), ind2col[st[0]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid-sep-lenf-lenf//2+3), (marg+lenf+sep+2*lenf//2-3,mid-sep-lenf-3), ind2col[st[1]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+3,mid-sep-lenf+lenf//2-3), (marg+lenf+sep+lenf//2-3,mid-sep-lenf+3), ind2col[st[2]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid-sep-lenf+lenf//2-3), (marg+lenf+sep+2*lenf//2-3,mid-sep-lenf+3), ind2col[st[3]], thickness=-1)

    # Cara 1
    cv.rectangle(scr, (marg+2*lenf+2*sep+3,mid-lenf//2+3), (marg+2*lenf+2*sep+lenf//2-3,mid-3), ind2col[st[4]], thickness=-1)
    cv.rectangle(scr, (marg+2*lenf+2*sep+lenf//2+3,mid-lenf//2+3), (marg+2*lenf+2*sep+2*lenf//2-3,mid-3), ind2col[st[5]], thickness=-1)
    cv.rectangle(scr, (marg+2*lenf+2*sep+3,mid+lenf//2-3), (marg+2*lenf+2*sep+lenf//2-3,mid+3), ind2col[st[6]], thickness=-1)
    cv.rectangle(scr, (marg+2*lenf+2*sep+lenf//2+3,mid+lenf//2-3), (marg+2*lenf+2*sep+2*lenf//2-3,mid+3), ind2col[st[7]], thickness=-1)

    # Cara 2
    cv.rectangle(scr, (marg+lenf+sep+3,mid-lenf//2+3), (marg+lenf+sep+lenf//2-3,mid-3), ind2col[st[8]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid-lenf//2+3), (marg+lenf+sep+2*lenf//2-3,mid-3), ind2col[st[9]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+3,mid+lenf//2-3), (marg+lenf+sep+lenf//2-3,mid+3), ind2col[st[10]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid+lenf//2-3), (marg+lenf+sep+2*lenf//2-3,mid+3), ind2col[st[11]], thickness=-1)

    # Cara 3
    cv.rectangle(scr, (marg+lenf+sep+3,mid+sep+lenf-lenf//2+3), (marg+lenf+sep+lenf//2-3,mid+sep+lenf-3), ind2col[st[12]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid+sep+lenf-lenf//2+3), (marg+lenf+sep+2*lenf//2-3,mid+sep+lenf-3), ind2col[st[13]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+3,mid+sep+lenf+lenf//2-3), (marg+lenf+sep+lenf//2-3,mid+sep+lenf+3), ind2col[st[14]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid+sep+lenf+lenf//2-3), (marg+lenf+sep+2*lenf//2-3,mid+sep+lenf+3), ind2col[st[15]], thickness=-1)

    # Cara 4
    cv.rectangle(scr, (marg+3,mid-lenf//2+3), (marg+lenf//2-3,mid-3), ind2col[st[16]], thickness=-1)
    cv.rectangle(scr, (marg+lenf//2+3,mid-lenf//2+3), (marg+2*lenf//2-3,mid-3), ind2col[st[17]], thickness=-1)
    cv.rectangle(scr, (marg+3,mid+lenf//2-3), (marg+lenf//2-3,mid+3), ind2col[st[18]], thickness=-1)
    cv.rectangle(scr, (marg+lenf//2+3,mid+lenf//2-3), (marg+2*lenf//2-3,mid+3), ind2col[st[19]], thickness=-1)

    # Cara 5
    cv.rectangle(scr, (marg+3*lenf+3*sep+3,mid-lenf//2+3), (marg+3*lenf+3*sep+lenf//2-3,mid-3), ind2col[st[20]], thickness=-1)
    cv.rectangle(scr, (marg+3*lenf+3*sep+lenf//2+3,mid-lenf//2+3), (marg+3*lenf+3*sep+2*lenf//2-3,mid-3), ind2col[st[21]], thickness=-1)
    cv.rectangle(scr, (marg+3*lenf+3*sep+3,mid+lenf//2-3), (marg+3*lenf+3*sep+lenf//2-3,mid+3), ind2col[st[22]], thickness=-1)
    cv.rectangle(scr, (marg+3*lenf+3*sep+lenf//2+3,mid+lenf//2-3), (marg+3*lenf+3*sep+2*lenf//2-3,mid+3), ind2col[st[23]], thickness=-1)


    image_filename = generate_image_name(state)
    cv.imwrite('static/Images/'+image_filename,scr)
    # cv.imshow('Dibujo2', scr)
    # cv.waitKey(0)

def sol2img(sol,name): # (B,G,R)
    scr = main.Sol2Scr(sol)
    state = main.Solved()


    for k in scr:
        move = getattr(main,k)
        state = move(state)
    
    state2 = main.s2sList(state)
    # print(state2)
    st = tr.TranslateStList(state2)

    ind2col = [(255,255,255), (0,0,255), (0,255,0), (0,255,255),  (0,128,255), (255,0,0)]
    auxl = 501
    scr = np.zeros((auxl, auxl, 3), dtype='uint8')
    scr[:]=255,150,0
    marg = auxl//10
    sep = auxl//20
    lenf = auxl//6
    mid = auxl//2+1
    # Líneas externas de las caras
    cv.rectangle(scr, (marg,mid-lenf//2), (marg+lenf,mid+lenf//2), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+lenf+sep,mid-lenf//2), (marg+2*lenf+sep,mid+lenf//2), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+lenf+sep,mid-lenf//2-sep-lenf), (marg+2*lenf+sep,mid+lenf//2-sep-lenf), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+lenf+sep,mid-lenf//2+sep+lenf), (marg+2*lenf+sep,mid+lenf//2+sep+lenf), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+2*lenf+2*sep,mid-lenf//2), (marg+3*lenf+2*sep,mid+lenf//2), (0,0,0), thickness=3)
    cv.rectangle(scr, (marg+3*lenf+3*sep,mid-lenf//2), (marg+4*lenf+3*sep,mid+lenf//2), (0,0,0), thickness=3)


    # Líneas horizontales
    cv.line(scr, (marg,mid), (marg+lenf,mid), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep,mid), (marg+2*lenf+sep,mid), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep,mid+sep+lenf), (marg+2*lenf+sep,mid+sep+lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep,mid-sep-lenf), (marg+2*lenf+sep,mid-sep-lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+2*lenf+2*sep,mid), (marg+3*lenf+2*sep,mid), (0,0,0), thickness=3)
    cv.line(scr, (marg+3*lenf+3*sep,mid), (marg+4*lenf+3*sep,mid), (0,0,0), thickness=3)

    # Líneas verticales
    cv.line(scr, (marg+lenf//2,mid-lenf//2), (marg+lenf//2,mid+lenf//2), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep+lenf//2,mid-lenf//2), (marg+lenf+lenf//2+sep,mid+lenf//2), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep+lenf//2,mid-lenf//2-sep-lenf), (marg+lenf+sep+lenf//2,mid+lenf//2-sep-lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+lenf+sep+lenf//2,mid-lenf//2+sep+lenf), (marg+lenf+sep+lenf//2,mid+lenf//2+sep+lenf), (0,0,0), thickness=3)
    cv.line(scr, (marg+2*lenf+2*sep+lenf//2,mid-lenf//2), (marg+2*lenf+2*sep+lenf//2,mid+lenf//2), (0,0,0), thickness=3)
    cv.line(scr, (marg+3*lenf+3*sep+lenf//2,mid-lenf//2), (marg+3*lenf+3*sep+lenf//2,mid+lenf//2), (0,0,0), thickness=3)


    # Stickers
    
    # Cara 0
    cv.rectangle(scr, (marg+lenf+sep+3,mid-sep-lenf-lenf//2+3), (marg+lenf+sep+lenf//2-3,mid-sep-lenf-3), ind2col[st[0]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid-sep-lenf-lenf//2+3), (marg+lenf+sep+2*lenf//2-3,mid-sep-lenf-3), ind2col[st[1]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+3,mid-sep-lenf+lenf//2-3), (marg+lenf+sep+lenf//2-3,mid-sep-lenf+3), ind2col[st[2]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid-sep-lenf+lenf//2-3), (marg+lenf+sep+2*lenf//2-3,mid-sep-lenf+3), ind2col[st[3]], thickness=-1)

    # Cara 1
    cv.rectangle(scr, (marg+2*lenf+2*sep+3,mid-lenf//2+3), (marg+2*lenf+2*sep+lenf//2-3,mid-3), ind2col[st[4]], thickness=-1)
    cv.rectangle(scr, (marg+2*lenf+2*sep+lenf//2+3,mid-lenf//2+3), (marg+2*lenf+2*sep+2*lenf//2-3,mid-3), ind2col[st[5]], thickness=-1)
    cv.rectangle(scr, (marg+2*lenf+2*sep+3,mid+lenf//2-3), (marg+2*lenf+2*sep+lenf//2-3,mid+3), ind2col[st[6]], thickness=-1)
    cv.rectangle(scr, (marg+2*lenf+2*sep+lenf//2+3,mid+lenf//2-3), (marg+2*lenf+2*sep+2*lenf//2-3,mid+3), ind2col[st[7]], thickness=-1)

    # Cara 2
    cv.rectangle(scr, (marg+lenf+sep+3,mid-lenf//2+3), (marg+lenf+sep+lenf//2-3,mid-3), ind2col[st[8]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid-lenf//2+3), (marg+lenf+sep+2*lenf//2-3,mid-3), ind2col[st[9]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+3,mid+lenf//2-3), (marg+lenf+sep+lenf//2-3,mid+3), ind2col[st[10]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid+lenf//2-3), (marg+lenf+sep+2*lenf//2-3,mid+3), ind2col[st[11]], thickness=-1)

    # Cara 3
    cv.rectangle(scr, (marg+lenf+sep+3,mid+sep+lenf-lenf//2+3), (marg+lenf+sep+lenf//2-3,mid+sep+lenf-3), ind2col[st[12]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid+sep+lenf-lenf//2+3), (marg+lenf+sep+2*lenf//2-3,mid+sep+lenf-3), ind2col[st[13]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+3,mid+sep+lenf+lenf//2-3), (marg+lenf+sep+lenf//2-3,mid+sep+lenf+3), ind2col[st[14]], thickness=-1)
    cv.rectangle(scr, (marg+lenf+sep+lenf//2+3,mid+sep+lenf+lenf//2-3), (marg+lenf+sep+2*lenf//2-3,mid+sep+lenf+3), ind2col[st[15]], thickness=-1)

    # Cara 4
    cv.rectangle(scr, (marg+3,mid-lenf//2+3), (marg+lenf//2-3,mid-3), ind2col[st[16]], thickness=-1)
    cv.rectangle(scr, (marg+lenf//2+3,mid-lenf//2+3), (marg+2*lenf//2-3,mid-3), ind2col[st[17]], thickness=-1)
    cv.rectangle(scr, (marg+3,mid+lenf//2-3), (marg+lenf//2-3,mid+3), ind2col[st[18]], thickness=-1)
    cv.rectangle(scr, (marg+lenf//2+3,mid+lenf//2-3), (marg+2*lenf//2-3,mid+3), ind2col[st[19]], thickness=-1)

    # Cara 5
    cv.rectangle(scr, (marg+3*lenf+3*sep+3,mid-lenf//2+3), (marg+3*lenf+3*sep+lenf//2-3,mid-3), ind2col[st[20]], thickness=-1)
    cv.rectangle(scr, (marg+3*lenf+3*sep+lenf//2+3,mid-lenf//2+3), (marg+3*lenf+3*sep+2*lenf//2-3,mid-3), ind2col[st[21]], thickness=-1)
    cv.rectangle(scr, (marg+3*lenf+3*sep+3,mid+lenf//2-3), (marg+3*lenf+3*sep+lenf//2-3,mid+3), ind2col[st[22]], thickness=-1)
    cv.rectangle(scr, (marg+3*lenf+3*sep+lenf//2+3,mid+lenf//2-3), (marg+3*lenf+3*sep+2*lenf//2-3,mid+3), ind2col[st[23]], thickness=-1)



    cv.imwrite(name,scr)
    # cv.imshow('Dibujo2', scr)
    # cv.waitKey(0)

# sol2img("U F' U R U' F' R2 U' F U2")
# st2img([1, 2, 3, 5, 6, 4, 9, 7, 8, 20, 21, 19, 10, 11, 12, 14, 15, 13, 17, 18, 16, 22, 23, 24])