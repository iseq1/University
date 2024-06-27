import numpy as np
import matplotlib.pyplot as plt

# a = np.array([[1,2,3],[4,-5,8],[3,6,8]]) # Матрица
# b = np.array([1,2,3], dtype=np.float32) # Массив  с плавающей точкой
# print('shape', a.shape) #размеры
# print('size', a.size) #кол-во элементов
# print('type', a.dtype) #тип данных
#
# z=np.zeros((2,3))
# o=np.ones((3,4))
# print(z,'\n',o)

# ar=np.arange(10)
# print(ar)
#
# ar2=np.arange(10,20)
# print(ar2)
#
# ar3=np.arange(10,20,2)
# print(ar3)

# t=np.linspace(0,1,11)
# print(t)

# r=np.random.rand(2,2) #рамномерное распределение
# print(r)
# r2=np.random.randn(2,2) #нормальное распределение
# print(r2)

# a=np.arange(5)
# b=np.ones((5))
# print(a+b)
#
# r=np.random.rand(2,2) #рамномерное распределение
# print(r)
#
# r2=np.random.randn(2,2) #нормальное распределение
# m=np.dot(r,r2) #перемножение
# print(m)

# r=np.random.rand(2,2) #рамномерное распределение
# print(np.mean(r))

# r=np.random.rand(10,10)
# print(r[2:7, 3:9])
# print(r[2:7:2, 3:9:3])

# r2=np.random.randn(10,10)
# inds = r2>0
# print(inds)
#
# d=np.arange(9)
# f=np.reshape(d,(3,3)) #из массива в матрицу
# print(f)
#
# h=np.hstack((f,f)) #конкатенация двух массивов то и сё
# print(h)
# v=np.vstack((f,f))
# print(v)

# x=np.linspace(-3,3,100)
# y=x**2
# plt.figure()
# plt.plot(x,y)
# plt.show()

# img=np.zeros((1024,1024,3), dtype=np.uint8) #пустой черный холст
# img[300:700,300:700,1] = 100
# plt.figure()
# plt.imshow(img)
# plt.show()
# plt.imsave('simple_image.png', img)


img=np.zeros((1024,1024,3), dtype=np.uint8) #пустой черный холст
r=85
x_centre=500
y_centre=500
img[300:700,300:700, 0] = 255
img[300:700,300:700, 1] = 255
img[300:700,300:700, 2] = 255
for i in range(300,700+1):
    for j in range(300,700+1):
        if ((x_centre-i)**2 + (y_centre-j)**2 <= r**2):
            img[i,j,0] = 255
            img[i, j, 2] = 0
            img[i, j, 1] = 0

# dim=200
# x_centre = 500
# y_centre = 500
# img=np.zeros((1024,1024,3), dtype=np.uint8) #пустой черный холст
#
# for i in range(200):
#     img[400+i:600-i,500+i,0]=255
#     img[400 + i:600 - i, 500 - i, 0] = 255

# img[400:600, 500, 0]=255
# img[450:550, 450, 0]=255
# img[450:550, 550, 0]=255
# img[499:501, 401, 0]=255
# img[499:501, 599, 0]=255

# for k in range(radius):
#     x=x_centre+k
#     for j in range(radius):
#         y=y_centre-j
#         for i in range(radius+1):
#             y=i
#             x=radius-y
#             img[x_centre+x,y_centre,0]=255





plt.figure()
plt.imshow(img)
plt.show()
plt.imsave('simple_image.png', img)
