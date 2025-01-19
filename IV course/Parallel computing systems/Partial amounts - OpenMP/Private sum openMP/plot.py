import matplotlib.pyplot as plt
import numpy as np
import os


def read_file(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            data = file.read()
        return data
    else:
        print("File not exist!")
        return None


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "speedup_data.txt")

    # file_path = "D:/project under development/C++ proj/Системы паралельных вычислений/Практика/test/11-22-2024/Private sum openMP/Private sum openMP/speedup_data.txt"
    file_data = read_file(file_path)

    if file_data:
        print("speedup_data.txt was successfully found and opened")

        speedup_data = [line.split(',') for line in file_data.split('\n') if line.split(',')[0].isdigit()]
        num_threads = [int(num_thread[0]) for num_thread in speedup_data]
        speedups = [float(speedup[1]) for speedup in speedup_data]

        plt.scatter(num_threads, speedups, color='blue', marker='o')
        slope, intercept = np.polyfit(num_threads, speedups, 1)
        regression_line = np.polyval([slope, intercept], num_threads)


        min_speedup = min(speedups)
        max_speedup = max(speedups)
        plt.ylim(min_speedup - 0.005, max_speedup + 0.005)  # Оставляем небольшой интервал вокруг максимума и минимума чтобы график не был линеен
        plt.xlabel('Кол-во потоков')
        plt.ylabel('Ускорение')
        plt.title('Диаграмма ускорения в зависимости от кол-ва потоков')
        plt.plot(num_threads, regression_line, color='red', label='Линия тренда')
        plt.legend()
        print("The speedup diagram depending on the number of threads has been successfully constructed and demonstrated!")
        plt.savefig("plot.png")
        plt.show()
