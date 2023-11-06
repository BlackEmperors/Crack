from random import random

a=[2,5,6,8,9,12,85,87,3]
i=0
title='True'
while i < len(a):
    if a[i]!=0:#往前走最大步长
        next_map=i+a[i]#下一个点的坐标
        if a[next_map]:#下一个点的坐标不为0，则移动
            i=next_map
        else:#如果下一个点坐标为0，则移动至上一个点.
            while not next_map-1:#如果上一个点为0，则继续向上移动
                next_map-=1 #下一个坐标点向上移动，直到不是0为止
            #移动可能是移动到起始点之后，也可能是起始点本身，那如果是起始点本身就是死循环，这个时候起始点往前，进入上一个循环
            if i==next_map:#移动到起始点了，进入上一个循环



















