import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image
img = Image.open('backgr.jpg')


class BezierCurve:
    def __init__(self, points):
        self.points = np.array(points)

    def get_points(self):
        return self.points

    def factorial(self, n):
        res = 1
        for i in range(1, n + 1):
            res *= i
        return res

    def bernstein_polynomial(self, i, n, t):
        return (self.factorial(n) // (self.factorial(i) * self.factorial(n - i))) * (t ** i) * ((1 - t) ** (n - i))

    def draw_curve(self, color, draw, num_points=265):
        result = np.zeros((num_points, 2))
        step = 1 / (num_points - 1)
        for j, t in enumerate(np.arange(0, 1 + step, step)):
            ytmp, xtmp = 0, 0
            for i in range(len(self.points)):
                b = self.bernstein_polynomial(i, len(self.points) - 1, t)
                xtmp += self.points[i, 0] * b
                ytmp += self.points[i, 1] * b


            result[j] = [xtmp, ytmp]

        if draw:
            # for x, y in result:
            #     image[int(np.round(y,1)*10),int(np.round(x,1)*10)] = 255
            plt.plot(result[:, 0], result[:, 1], color=color)
        return result


r = 1.8  # Радиус зрачка
x_start_left = 37  # Начальная позиция по оси X
y_left = 66.8  # Позиция по оси Y
direction_left = 1  # Направление движения (1 - вправо, -1 - влево)

x_start_right = 50  # Начальная позиция по оси X
y_start_right = 73.8  # Позиция по оси Y
direction_right = -1  # Направление движения (1 - вправо, -1 - влево)

x_start_tail = 90
direction_tail = 1
y_start_tail = 75

def draw_cat(img):
    fig, ax = plt.subplots()
    line, = ax.plot([], [], color='black')
    ax.imshow(img, extent=[0, 100, 0, 100], aspect='auto', alpha=1)
    draw_ears()
    draw_head()
    draw_eyes()
    draw_body()
    draw_paws()
    # plt.ylim(1000, 0)
    # plt.gca().invert_yaxis()
    # plt.imshow(image)



    # Функция инициализации графики
    def init():
        return circle, circle2,

    # Функция обновления анимации
    def update(frame):
        global x_start_left, direction_left, x_start_right, y_start_right, direction_right
        x_start_left += direction_left*0.5
        x_start_right += direction_right*0.5
        y_start_right += direction_right*1.15*0.5
        if x_start_left >= 41 or x_start_left <= 37:
            direction_left *= -1
        if x_start_right >= 50 or x_start_right <= 46:
            direction_right *= -1
        circle.center = (x_start_left, y_left)
        circle2.center = (x_start_right, y_start_right)

        if frame <= 20:
            tail_points = np.array(
                [[72.25, 63.1], [77 + frame/2, 86 - frame/2], [82, 97]])
            tail_curve = BezierCurve(tail_points)
            tail = tail_curve.draw_curve('black', False)
            x = [tail[i][0] for i in range(len(tail))]
            y = [tail[i][1] for i in range(len(tail))]
            line.set_data(x, y)

        elif frame <= 60:
            tail_points = np.array([[72.25, 63.1], [77 + 20/2 - (frame/2 - 20/2), 86 - 20/2 + (frame/2 - 20/2)],
                                    [82, 97]])
            tail_curve = BezierCurve(tail_points)
            tail = tail_curve.draw_curve('black', False)
            x = [tail[i][0] for i in range(len(tail))]
            y = [tail[i][1] for i in range(len(tail))]
            line.set_data(x, y)

        elif frame <= 80:
            tail_points = np.array([[72.25, 63.1], [77 - 20/2 + (frame/2 - 60/2), 86 + 20/2 - (frame/2 - 60/2)],
                                    [82, 97]])
            tail_curve = BezierCurve(tail_points)
            tail = tail_curve.draw_curve('black', False)
            x = [tail[i][0] for i in range(len(tail))]
            y = [tail[i][1] for i in range(len(tail))]

            line.set_data(x, y)


        return circle, circle2, line,

    circle2 = plt.Circle((x_start_right, y_start_right), r, fc='black')
    circle = plt.Circle((x_start_left, y_left), r, fc='black')
    ax.add_patch(circle)
    ax.add_patch(circle2)

    # Создание анимации
    ani = animation.FuncAnimation(fig, update, frames=80, init_func=init, blit=True, interval=100)
    ani.save('animationCat.gif', writer='pillow', fps=30)
    plt.show()



def draw_eyes():
    points1 = np.array([[35.2, 66.8], [39, 71], [42.9, 66.52]])
    points2 = np.array([[35.2, 66.8], [39, 64], [42.9, 66.52]])
    points3 = np.array([[45.98, 68.09], [45, 73], [50.2, 74.66]])
    points4 = np.array([[45.98, 68.09], [50, 68], [50.2, 74.66]])
    eyes = list([points1, points2, points3, points4])

    temp = []
    for item in eyes:
        ear = BezierCurve(item)
        temp.append(ear.draw_curve('yellow', 1))

    for i in range(len(eyes) // 2):
        for start, finish in zip(temp[i * 2], temp[i * 2 + 1]):
            fill = BezierCurve(np.array([start, finish]))
            fill.draw_curve('yellow', 1)


def draw_ears():
    points1 = np.array([[34.3,68.7],[28,72],[27,75.25]])
    points2 = np.array([[36.7,73],[32,73],[27,75.25]])
    points3 = np.array([[44,76.8],[46.5,80],[47.6,86]])
    points4 = np.array([[49.6,76.2],[50.4,81.6],[47.6,86]])
    ears = list([points1,points2,points3,points4])

    temp = []
    for item in ears:
        ear = BezierCurve(item)
        temp.append(ear.draw_curve('black',1))

    for i in range(len(ears)//2):
        for start, finish in zip(temp[i*2], temp[i*2+1]):
            fill = BezierCurve(np.array([start,finish]))
            fill.draw_curve('black', 1)


def draw_head():
    points1 = np.array([[33, 63.5], [42.5, 63.1]])
    points2 = np.array([[54.1, 74.7], [49.1, 66.5]])
    points3 = np.array([[42.5, 63.1], [49, 58], [49.1, 66.5]])
    points4 = np.array([[33, 63.5], [36,82], [54.1, 74.7]])
    points5 = np.array([[45.875, 61.31], [46.257, 51.03]])
    points6 = np.array([[47.922, 61.83], [50.061, 54.57]])

    head = list([points1, points2, points3, points4, points5, points6])
    temp=[]
    for item in head:
        headC = BezierCurve(item)
        temp.append(headC.draw_curve('black', 1))

    for i in range(len(head) // 2):
        for start, finish in zip(temp[i * 2], temp[i * 2 + 1]):
            fill = BezierCurve(np.array([start, finish]))
            fill.draw_curve('black', 1)



def draw_body():
    points1 = np.array([[46.257, 51.03], [40, 45],[54.090, 7.71]]) # 1 лапа снаружи
    points2 = np.array([[51.478, 37.3], [48, 34],[52.329, 17.2]])   # 1 лапа внутри
    points3 = np.array([[51.478, 37.3], [56,35],[52.329, 17.2]])    # 2 лапа внутри
    points4 = np.array([[58.345, 42.04], [57,26], [53.235, 13.11]]) # 2 лапа снаружи
    points5 = np.array([[53.235, 13.11], [54.747, 7.94]]) # 1 лапа остаток снизу
    points6 = np.array([[58.345, 42.04], [64.12, 45.47]]) # пузо
    points7 = np.array([[50.061, 54.57], [55, 58], [70, 60], [72.23, 63.55]]) # спина
    points8 = np.array([[74, 64], [84,58], [66.74, 14.74]]) # 4 лапа снаружи
    points9 = np.array([[64.12, 45.47], [67,29], [71.07, 18.83]]) # 3 лапа снаружи
    points10 = np.array([[69.1, 24.37], [66.21, 14.68]]) # 4 лапа остаток снизу
    points11 = np.array([[70.44, 24.5],[71.57, 19.07]]) # 3 лапа остаток снизу
    points12 = np.array([[71, 45.23], [67,43], [69.87, 27.65]]) # 3 лапа внутри
    points13 = np.array([[71, 45.23], [74.3,43], [69.87, 27.65]]) # 4 лапа внутри
    points14 = np.array([[51.93, 13.58], [50.14, 4.43]]) # 2 лапа остаток снизу
    points15 = np.array([[52.807, 11.2], [50.739, 4.34]]) # 2 лапа остаток снизу
    points16 = np.array([[46.26, 51.02], [50.02, 54.58]]) # шея
    points17 = np.array([[72.23, 63.55],[73.1, 65.5],[74, 63.9]]) # начало хвоста
    points18 = np.array([[66.2, 14.65], [68.524, 22.11]])
    points19 = np.array([[66.74, 14.79], [68.627, 20.46]])

    body = list([points1,points2,points3, points4,points5, points6, points7, points8, points9, points10, points11, points12, points13, points14, points15, points16, points17, points18, points19])
    temp = []
    for item in body:
        bodyC = BezierCurve(item)
        temp.append(bodyC.draw_curve('black',1))

    for start in temp[16][::4]:
        fill = BezierCurve(np.array([start, [71, 45.23]]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[17], temp[18]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[10], temp[8]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[0], temp[1]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[13], temp[14]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[2], temp[3]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[5], temp[6]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[5], temp[15]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)

    for start, finish in zip(temp[2][:88], temp[6]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[12], temp[7]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[11], temp[8]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)

    for start, finish in zip(temp[6][:100:-1], temp[11]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)

    for point in temp[15]:
        fill = BezierCurve(np.array([point, [51.478, 37.3]]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[0], temp[4]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[9], temp[7][:60:-1]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)
    for start, finish in zip(temp[15], temp[3][:80]):
        fill = BezierCurve(np.array([start, finish]))
        fill.draw_curve('black',1)


def draw_paws():
    points1 = np.array([[46.96, 1.59], [47, 5.5], [53,5.5], [52.37, 1.18]])
    points2 = np.array([[46.96, 1.59], [49.8, 4], [52.37, 1.18]])
    points3 = np.array([[52.19, 4.32], [53, 9], [57,9], [57.84, 5.14]])
    points4 = np.array([[52.19, 4.32], [55, 7], [57.84, 5.14]])
    points5 = np.array([[62.96, 12.28], [63, 15.5], [69,15.5], [68.44, 11.32]])
    points6 = np.array([[62.96, 12.28], [66, 13.5], [68.44, 11.32]])
    points7 = np.array([[69.18, 15.4], [69, 20], [75, 20], [74.69, 16.65]])
    points8 = np.array([[69.18, 15.4], [72, 18], [74.69, 16.65]])

    paws = list([points1, points2, points3, points4, points5, points6, points7, points8])
    temp = []
    for item in paws:
        pawsC = BezierCurve(item)
        temp.append(pawsC.draw_curve('black',1))

    for i in range(len(paws) // 2):
        for start, finish in zip(temp[i * 2], temp[i * 2 + 1]):
            fill = BezierCurve(np.array([start, finish]))
            fill.draw_curve('black',1)



if __name__ == "__main__":
    draw_cat(img)

