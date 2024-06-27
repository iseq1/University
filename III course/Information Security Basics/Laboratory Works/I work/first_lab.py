import random
import math
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Кастомная функция для быстрого
# возведения в степень длинных чисел по модулю.
def power_mod(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result


# Алгоритм Миллера-Робина
def miller_rabin_test(n, rounds):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    def check(a, s, d, n):
        x = power_mod(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = random.randint(2, n - 2)
        if not check(a, s, d, n):
            return False
    return True

# функцию, которая генерирует (возможно) простое
# число определенной битности.
def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1
        if miller_rabin_test(p, 10):
            return p



# функцию, которая проверяет длинное число p ( p –
# произвольное положительное целое число) на простоту с
# помощью теста Миллера-Рабина.
def is_prime(p, n=None):
    if n is None:
        n = math.ceil(math.log2(p))
    return miller_rabin_test(p, n)


# Для консоли
def main():
    while True:
        print("Главное меню:")
        print("0. Выход")
        print("1. Ввод с консоли")
        print("2. Ввод из файла")
        choice = input("\nВыберите вариант (0/1/2): ")

        if choice == '1':
            num = int(input("Введите число для проверки на простоту: "))
            rounds_input = input("Введите количество раундов (по умолчанию logp): ")
            if rounds_input:
                rounds = int(rounds_input)
            else:
                rounds = None
            if is_prime(num, rounds):
                print("\n||==========||==========||\n", f"{num} - возможно простое", "\n||==========||==========||\n")
            else:
                print("\n||==========||==========||\n", f"{num} - составное", "\n||==========||==========||\n")

        elif choice == '2':
            filename = input("Введите название файла (по умолчанию 'numbers.txt'): ")
            if filename == '':
                filename = 'numbers.txt'
            with open(filename, 'r') as file:
                lines = file.readlines()
                results = []
                for line in lines:
                    parts = line.split()
                    p = int(parts[0])
                    if len(parts) > 1:
                        rounds = int(parts[1])
                    else:
                        rounds = None
                    if is_prime(p, rounds):
                        results.append(f"{p} - возможно простое\n")
                    else:
                        results.append(f"{p} - составное\n")

            output_filename = input("Введите название файла для записи результатов (по умолчанию 'answer.txt'): ")
            if output_filename == '':
                output_filename = 'answer.txt'
            with open(output_filename, 'w') as output_file:
                output_file.writelines(results)
                print(f'Результат успешно записан в {output_filename}\n')

        elif choice == '0':
            break

        else:
            print("Некорректный выбор, попробуйте снова.")




# Для пользовательского интерфейса
def create_layout():
    def calculate(num, rounds_input=None):
        if rounds_input:
            rounds = int(rounds_input)
        else:
            rounds = None
        if is_prime(num, rounds):
            messagebox.showinfo('Ответ', f"{num} - возможно простое")
        else:
            messagebox.showinfo('Ответ', f"{num} - составное")

    def calculate_file(filename=None, output_filename= None):
        if filename == '':
            filename = 'numbers.txt'
        with open(filename, 'r') as file:
            lines = file.readlines()
            results = []
            for line in lines:
                parts = line.split()
                p = int(parts[0])
                if len(parts) > 1:
                    rounds = int(parts[1])
                else:
                    rounds = None
                if is_prime(p, rounds):
                    results.append(f"{p} - возможно простое\n")
                else:
                    results.append(f"{p} - составное\n")


        if output_filename == '':
            output_filename = 'answer.txt'
        with open(output_filename, 'w') as output_file:
            output_file.writelines(results)
            messagebox.showinfo('Ответ', f'Результат успешно записан в {output_filename}\n')


    window = tk.Tk()
    window.geometry('1000x450')
    window.title("Алгоритм Миллера-Робина")


    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, expand=True)

    # create frames
    frame1 = ttk.Frame(notebook, width=1000, height=450)
    frame1.pack(fill='both', expand=True)
    inputN_lb = Label(
        frame1,
        text="Введите число для проверки на простоту:",
        font='Times 18',
        fg='#000'
    )
    inputLog_lb = Label(
        frame1,
        text="Введите количество раундов (по умолчанию logp):",
        font='Times 18',
        fg='#000'
    )
    inputN_tf = Entry(
        frame1,
        font='Times 25',
        fg='#000'
    )
    inputLog_tf = Entry(
        frame1,
        font='Times 25',
        fg='#000'
    )
    cal_btn = Button(
        frame1,
        text='Рассчитать',
        command=lambda: calculate(int(inputN_tf.get()), inputLog_tf.get())  # Вызов функции при нажатии кнопки.
    )
    inputN_lb.grid(row=3, column=1, sticky='w')
    inputLog_lb.grid(row=4, column=1)
    inputN_tf.grid(row=3, column=2)
    inputLog_tf.grid(row=4, column=2, pady=5)
    cal_btn.grid(row=5, column=2)

    frame2 = ttk.Frame(notebook, width=1000, height=450)
    frame2.pack(fill='both', expand=True)
    inputFile_lb = Label(
        frame2,
        text="Введите название файла (по умолчанию 'numbers.txt'):",
        font='Times 12',
        fg='#000'
    )
    outputFile_lb = Label(
        frame2,
        text="Введите название файла для записи результатов (по умолчанию 'answer.txt'): ",
        font='Times 12',
        fg='#000'
    )
    warning_lb = Label(
        frame2,
        text="Не вводите названия файлов в поля ввода, \nесли выбранные по умолчанию файлы существуют и корректны!\n\nБудьте внимательны при вводе, \nв программе не предусмотрена обработка ошибок ввода пользлвателя",
        font='Times 12',
        fg='#fff',
        bg='#000',

    )
    inputFile_tf = Entry(
        frame2,
        font='Times 25',
        fg='#000'
    )
    outputFile_tf = Entry(
        frame2,
        font='Times 25',
        fg='#000'
    )
    cal_btn_file = Button(
        frame2,
        text='Рассчитать',
        command=lambda: calculate_file(inputFile_tf.get(), outputFile_tf.get())  # Вызов функции при нажатии кнопки.
    )
    inputFile_lb.grid(row=3, column=1)
    outputFile_lb.grid(row=4, column=1)
    inputFile_tf.grid(row=3, column=2)
    outputFile_tf.grid(row=4, column=2, pady=5)
    warning_lb.grid(row=5, column=1)
    cal_btn_file.grid(row=5, column=2)


    notebook.add(frame1, text='Ввод числа')
    notebook.add(frame2, text='Ввод файла')

    window.mainloop()


if __name__ == "__main__":

    # GIU - app
    create_layout()

    # consol - app
    # main()


