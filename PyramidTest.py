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

img = cv2.imread('1.jpg')
g_list, l_list = get_my_gauss_laplace_list(img)

# <codecell>

for i,g in enumerate(g_list):
    print 'gauss: ',i,g.shape
    
for i,l in enumerate(l_list):
    print 'laplace: ',i,l.shape

# <codecell>

r_list = reconstruct_image(g_list, l_list)

# <codecell>

for i,r in enumerate(r_list):
    print 'recons: ',i,r.shape
    
print np.max(r_list[0] - g_list[0])
cv2.imwrite('1_copy.jpg', np.uint8( r_list[0]*255) )

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
    
    cv2.imwrite('r1.jpg',np.uint8(r_list1[0]*255/np.max(r_list1[0])) )
    cv2.imwrite('r2.jpg', np.uint8(r_list2[0]*255/np.max(r_list2[0])) )

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

main()

# <codecell>


