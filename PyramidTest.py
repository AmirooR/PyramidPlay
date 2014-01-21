# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import cv,cv2
import numpy as np

# <codecell>

def get_my_gauss_laplace_list(img, layers=5):
    g_list = []
    l_list = []
    g_list.append(img/255.)
    for i in range(layers):
        g_list.append(cv2.pyrDown(g_list[-1]))
        
    for i in range(layers):
        l_list.append( g_list[i] - cv2.pyrUp(g_list[i+1]))
    return g_list, l_list

# <codecell>

def reconstruct_image(g_list, l_list):
    r_list = [cv2.pyrUp(g_list[-1])+l_list[-1]]
    for i in range(len(l_list)-1):
        r_list = [cv2.pyrUp(r_list[0])+l_list[-i-2]] + r_list
        
    return r_list

# <codecell>

def correct_gamma(img, gamma=2.2):
    b = img/255.
    c = b**gamma
    return np.uint8(c*255)

# <codecell>

def main():
    img1 = cv2.imread('1.jpg')
    g_list1, l_list1 = get_my_gauss_laplace_list(img1)
    img2 = cv2.imread('2.jpg')
    g_list2, l_list2 = get_my_gauss_laplace_list(img2)
    m2 = np.zeros_like(img2)
    m2[273:318, 345:430] = 255
    m1 = 255 - m2
    mg_list1, ml_list1 = get_my_gauss_laplace_list(m1)
    mg_list2, ml_list2 = get_my_gauss_laplace_list(m2)
    lg_1 = []
    lg_2 = []
    l_final = []
    g_final = g_list2
    g_final2 = g_list1
    tr = 0.5
    for i in range(len(l_list1)):
        lg_1.append( l_list1[i] * mg_list1[i] )
        lg_2.append( l_list2[i] * mg_list2[i] )
        l_final.append( tr*lg_1[-1] + (1-tr)*lg_2[-1])
        
    r_list1 = reconstruct_image(g_final, l_final)
    r_list2 = reconstruct_image(g_final2, l_final)
    
    a = correct_gamma(np.uint8(r_list2[0]*255/np.max(r_list2[0])))
#    cv2.imwrite('r1.jpg',np.uint8(r_list1[0]*255/np.max(r_list1[0])) )
    cv2.imwrite('rd.jpg', a)

# <codecell>

def main2():
    img1 = cv2.imread('1.jpg')
    g_list1, l_list1 = get_my_gauss_laplace_list(img1)
    img2 = cv2.imread('2.jpg')
    g_list2, l_list2 = get_my_gauss_laplace_list(img2)
    m2 = np.zeros_like(img2)
    m2[273:318, 345:430] = 255
    m1 = 255 - m2
    mg_list1, ml_list1 = get_my_gauss_laplace_list(m1)
    mg_list2, ml_list2 = get_my_gauss_laplace_list(m2)
    lg_1 = []
    lg_2 = []
    l_final = []
    g_final = g_list2
    g_final2 = g_list1
    tr = 0.9
    for i in range(len(l_list1)):
        lg_1.append( l_list1[i] * mg_list1[i] )
        lg_2.append( l_list2[i] * mg_list2[i] )
    
    for i in range(len(l_list1)):
        if i % 2==0:
            l_final.append( tr*lg_2[i] + (1-tr)*lg_1[i])
        else:
            l_final.append( tr*lg_1[i] + (1-tr)*lg_2[i])
#            l_final.append( tr*lg_1[i] + (1-tr)*lg_2[i])
        
#    r_list1 = reconstruct_image(g_final, l_final)
    r_list2 = reconstruct_image(g_final2, l_final)
    
#    cv2.imwrite('s1.jpg',np.uint8(r_list1[0]*255/np.max(r_list1[0])) )
    cv2.imwrite('s222.jpg', np.uint8(r_list2[0]*255/np.max(r_list2[0])) )

# <codecell>

def main3():
    img1 = cv2.imread('a.jpg')
    g_list1, l_list1 = get_my_gauss_laplace_list(img1, layers=4)
    imgTmp = cv2.imread('2.jpg')
    img2 = np.copy(img1)
    #left eye
    img2[630-100:682+100,490-100:561+100] = imgTmp[278-100:330+100, 209-100:280+100]
    #right eye
    img2[660-100:705+100,1090-100:1175+100] = imgTmp[273-100:318+100, 345-100:430+100]
    g_list2, l_list2 = get_my_gauss_laplace_list(img2, layers=4)
    m2 = np.zeros_like(img1)
    m2[630:682,490:561] = 255
    m2[660:705,1090:1175] = 255
    m1 = 255 - m2
    mg_list1, ml_list1 = get_my_gauss_laplace_list(m1, layers=4)
    mg_list2, ml_list2 = get_my_gauss_laplace_list(m2, layers=4)
    lg_1 = []
    lg_2 = []
    l_final = []
    g_final = g_list2
    g_final2 = g_list1
    tr = 0.5
    for i in range(len(l_list1)):
        lg_1.append( l_list1[i] * mg_list1[i] )
        lg_2.append( l_list2[i] * mg_list2[i] )
        l_final.append( tr*lg_1[-1] + (1-tr)*lg_2[-1])
        
    r_list1 = reconstruct_image(g_final, l_final)
    r_list2 = reconstruct_image(g_final2, l_final)
    
#    cv2.imwrite('ar1.jpg',np.uint8(r_list1[0]*255/np.max(r_list1[0])) )
    a = correct_gamma(np.uint8(r_list2[0]*255/np.max(r_list2[0])) )
    cv2.imwrite('d.jpg', a)

# <codecell>

main3()

# <codecell>


