import matplotlib.pyplot as plt
import numpy as np
import imageio
import matplotlib.animation as animation

image = np.zeros((800, 600, 3), dtype=np.uint8)

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

    def bernstein_polynomial(self, k, n, t):
        return (self.factorial(n) // (self.factorial(k) * self.factorial(n - k))) * (t ** k) * ((1 - t) ** (n - k))

    def draw_curve(self, color, num_points=100):
        result = np.zeros((num_points, 2))
        step = 1 / (num_points - 1)

        for j, t in enumerate(np.arange(0, 1 + step, step)):
            ytmp, xtmp = 0, 0
            for k in range(len(self.points)):
                b = self.bernstein_polynomial(k, len(self.points) - 1, t)
                xtmp += self.points[k, 0] * b
                ytmp += self.points[k, 1] * b


            result[j] = [xtmp, ytmp]
        # print('start',result,'end')
        # plt.plot(result[:, 0], result[:, 1], color=color)
        return result



fig, ax = plt.subplots()
ax = plt.axes(xlim=(-100, 600), ylim=(0, 500))
plt.axis('off')
line, = ax.plot([], [], color='black')
line2, = ax.plot([], [], color='black')
line3, = ax.plot([], [], color='black')
line4, = ax.plot([], [], color='black')

first = np.array([[250,250],[340,310],[350,250]])
second = np.array([[250,250],[340,190],[350,250]])
third = np.array([[250,250],[160,310],[150,250]])
fourth = np.array([[250,250],[160,190],[150,250]])

one = BezierCurve(first).draw_curve('black')
two = BezierCurve(second).draw_curve('black')
three = BezierCurve(third).draw_curve('black')
four = BezierCurve(fourth).draw_curve('black')

M = first[2][0] - third[2][0]
T = max([itemy for itemx, itemy in one]) - min([itemy for itemx, itemy in two])

dx = np.linspace(0,M,60)


def make_dx_for_cp(start, stop):
    dx = np.linspace(start, stop, 60)
    return dx
def make_dx_for_cp_2(start, stop):
    dx = np.linspace(start, stop, 40)
    return dx

def animate(frames):
    if frames<60:
        new_line1 = np.array([[250,250],[make_dx_for_cp(340, (350+make_dx_for_cp(0, (1.5*M - M)/2)[frames]))[frames],make_dx_for_cp(310, 250)[frames]],[350+make_dx_for_cp(0, (1.5*M - M)/2)[frames],250]])
        new_one = BezierCurve(new_line1)
        new1 = new_one.draw_curve('black')
        x = [new1[i][0] for i in range(len(new1))]
        y = [new1[i][1] for i in range(len(new1))]
        line.set_data(x,y)

        new_line2 = np.array([[250,250],[make_dx_for_cp(340, 350)[frames],make_dx_for_cp(190, 250)[frames]],[350+make_dx_for_cp(0, (1.5*M - M)/2)[frames],250]])
        new_two = BezierCurve(new_line2)
        new2 = new_two.draw_curve('black')
        x = [new2[i][0] for i in range(len(new2))]
        y = [new2[i][1] for i in range(len(new2))]
        line2.set_data(x, y)

        new_line3 = np.array([[250,250],[make_dx_for_cp(160, 150)[frames],make_dx_for_cp(310, 250)[frames]],[150-make_dx_for_cp(0, (1.5*M - M)/2)[frames],250]])
        new_three = BezierCurve(new_line3)
        new3 = new_three.draw_curve('black')
        x = [new3[i][0] for i in range(len(new3))]
        y = [new3[i][1] for i in range(len(new3))]
        line3.set_data(x, y)

        new_line4 = np.array([[250,250],[make_dx_for_cp(160, 150)[frames],make_dx_for_cp(190, 250)[frames]],[150-make_dx_for_cp(0,(1.5*M - M)/2)[frames],250]])
        new_four = BezierCurve(new_line4)
        new4 = new_four.draw_curve('black')
        x = [new4[i][0] for i in range(len(new4))]
        y = [new4[i][1] for i in range(len(new4))]
        line4.set_data(x, y)

    if frames>=61:
        new_line1 = np.array([[250, 250], [make_dx_for_cp_2(350, 340)[frames-60], make_dx_for_cp_2(250, 310+(1.5*T-T)/2)[frames-60]],
                              [350+M/4 - make_dx_for_cp_2(0, (1.5*M - M)/2)[frames-60], 250]])
        new_one = BezierCurve(new_line1)
        new1 = new_one.draw_curve('black')
        x = [new1[i][0] for i in range(len(new1))]
        y = [new1[i][1] for i in range(len(new1))]
        line.set_data(x, y)

        new_line2 = np.array([[250, 250], [make_dx_for_cp_2(350, 340)[frames-60], make_dx_for_cp_2(250, 190-(1.5*T-T)/2)[frames-60]],
                              [350+M/4 - make_dx_for_cp_2(0, (1.5*M - M)/2)[frames-60], 250]])
        new_two = BezierCurve(new_line2)
        new2 = new_two.draw_curve('black')
        x = [new2[i][0] for i in range(len(new2))]
        y = [new2[i][1] for i in range(len(new2))]
        line2.set_data(x, y)

        new_line3 = np.array([[250, 250], [make_dx_for_cp_2(150, 160)[frames-60], make_dx_for_cp_2(250, 310+(1.5*T-T)/2)[frames-60]],
                              [150-M/4 + make_dx_for_cp_2(0, (1.5*M - M)/2)[frames-60], 250]])
        new_three = BezierCurve(new_line3)
        new3 = new_three.draw_curve('black')
        x = [new3[i][0] for i in range(len(new3))]
        y = [new3[i][1] for i in range(len(new3))]
        line3.set_data(x, y)

        new_line4 = np.array([[250, 250], [make_dx_for_cp_2(150, 160)[frames-60], make_dx_for_cp_2(250, 190-(1.5*T-T)/2)[frames-60]],
                              [150-M/4 + make_dx_for_cp_2(0, (1.5*M - M)/2)[frames-60], 250]])
        new_four = BezierCurve(new_line4)
        new4 = new_four.draw_curve('black')
        x = [new4[i][0] for i in range(len(new4))]
        y = [new4[i][1] for i in range(len(new4))]
        line4.set_data(x, y)


    return line, line2, line3, line4,

if __name__ == "__main__":
    ani = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True, )
    ani.save('animation.gif', writer='pillow', fps=30)
    plt.show()
