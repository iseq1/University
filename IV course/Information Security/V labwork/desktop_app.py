import tkinter as tk
from tkinter import scrolledtext, messagebox
from SStestDEC import SquareSieve
import numpy as np


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Факторизация больших чисел")

        # Настройка grid
        self.setup_grid()

        # Лейбл по середине
        self.label1 = tk.Label(self.root, text="Число n")
        self.label1.grid(row=0, column=0, columnspan=3, pady=10)

        # Текстовое поле для ввода (небольшое)
        self.entry1 = tk.Text(self.root, width=20, height=1)
        self.entry1.grid(row=1, column=0, columnspan=3, pady=5)

        # Два лейбла с равным расстоянием по бокам и между
        self.label2 = tk.Label(self.root, text="Параметр M")
        self.label2.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.label3 = tk.Label(self.root, text="Параметр B")
        self.label3.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Два текстовых поля под лейблом (небольшие)
        self.entry2 = self.create_numeric_entry(self.root, width=20)
        self.entry2.grid(row=3, column=0, padx=10, pady=15)

        self.entry3 = self.create_numeric_entry(self.root, width=20)
        self.entry3.grid(row=3, column=2, padx=10, pady=15)

        # Текстовое поле для вывода длинного списка (с прокруткой)
        self.label5 = tk.Label(self.root, text="Результат просеивания")
        self.label5.grid(row=5, column=0, columnspan=3, pady=5)

        self.scroll_text1 = scrolledtext.ScrolledText(self.root, width=40, height=5, wrap=tk.WORD)
        self.scroll_text1.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

        # Лейбл по середине
        self.label6 = tk.Label(self.root, text="Матрица А")
        self.label6.grid(row=7, column=0, columnspan=3, pady=5)

        # Текстовое поле для вывода матрицы (с прокруткой)
        self.scroll_text2 = scrolledtext.ScrolledText(self.root, width=40, height=5, wrap=tk.WORD)
        self.scroll_text2.grid(row=8, column=0, columnspan=3, padx=10, pady=5)

        # Лейбл по середине
        self.label7 = tk.Label(self.root, text="Множество вектор-ответов")
        self.label7.grid(row=9, column=0, columnspan=3, pady=5)

        # Текстовое поле для вывода вектора
        self.scroll_text3 = scrolledtext.ScrolledText(self.root, width=40, height=5, wrap=tk.WORD)
        self.scroll_text3.grid(row=10, column=0, columnspan=3, padx=10, pady=5)

        # Два лейбла с равным расстоянием по бокам и между
        self.label8 = tk.Label(self.root, text="Число p")
        self.label8.grid(row=11, column=0, padx=10, pady=5, sticky="e")

        self.label9 = tk.Label(self.root, text="Число q")
        self.label9.grid(row=11, column=2, padx=10, pady=5, sticky="w")

        # Два текстовых поля под лейблом (небольшие)
        self.entry4 = scrolledtext.ScrolledText(self.root, width=20, height=1)
        self.entry4.grid(row=12, column=0, padx=10, pady=5)

        self.entry5 = scrolledtext.ScrolledText(self.root, width=20, height=1)
        self.entry5.grid(row=12, column=2, padx=10, pady=5)

        # Кнопка внизу
        self.button = tk.Button(self.root, text="Факторизация", command=self.on_button_click)
        self.button.grid(row=13, column=0, columnspan=3, pady=20)

    def setup_grid(self):
        """Настройка grid для динамического изменения размеров"""
        for i in range(14):  # Включая строку для кнопки
            self.root.grid_rowconfigure(i, weight=1)

        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

    def create_numeric_entry(self, parent, width=20):
        """Создаёт поле для ввода, в котором разрешены только цифры"""
        entry = tk.Entry(parent, width=width)
        # Привязываем обработчик события KeyPress
        entry.bind("<KeyPress>", self.validate_input)
        return entry

    def validate_input(self, event):
        """Проверка на ввод только цифр"""
        char = event.char
        if not char.isdigit() and char != '\x08':  # '\x08' - это символ Backspace
            return "break"  # Блокируем ввод
        return None  # Разрешаем ввод

    def on_button_click(self):
        """Обработчик нажатия кнопки"""
        try:
            self.scroll_text1.delete('1.0', 'end')
            self.scroll_text2.delete('1.0', 'end')
            self.scroll_text3.delete('1.0', 'end')
            self.entry5.delete('1.0', 'end')
            self.entry4.delete('1.0', 'end')

            # Для примера, выводим данные из текстовых полей
            n = self.entry1.get("1.0", tk.END).strip()
            M = self.entry2.get()
            B = self.entry3.get()
            if not all([item != "" and item.isdigit() for item in [n, M, B]]):
                raise Exception("Неверно указаны вводные данные!")
            square_sieve = SquareSieve(smoothness_parameter=int(B), M=int(M))
            factor = square_sieve.factorization(int(n))
            sifted_list = next(factor)
            if isinstance(sifted_list, np.ndarray):
                messagebox.showinfo(title='Уведомление', message=f"В ходе алгоритма полный квадрат не был найден!", )
                self.scroll_text1.insert(tk.END, f"{sifted_list}\n")
                A = next(factor)
                print(len(A))
                if len(A)==0:
                    messagebox.showwarning(title='Осторожно', message=f"В ходе алгоритма не получилось сформировать матрицу А.\nВероятнее всего, заданные параметры M и B слишком малы!")
                    return
                # вот тут если матрица == [] то не найдены числа при таких параметрах
                self.scroll_text2.insert(tk.END, f"{A}\n")
                solution_vectors = next(factor)
                self.scroll_text3.insert(tk.END, f"\n".join([str(sublist) for sublist in solution_vectors]))

                p, q = next(factor)
                if p is None and q is None:
                    messagebox.showinfo(title='Уведомление',
                                        message=f"В ходе алгоритма не удалось найти нетривиальное решение для уравнения Ax=0\nПопробуйте другие параметры B и M!", )
                self.entry5.insert(tk.END, str(q))
                self.entry4.insert(tk.END, str(p))
            else:
                messagebox.showinfo(title='Уведомление', message=f"В ходе алгоритма был найден полный квадрат {sifted_list}\nПоэтому числа p и q находятся по формуле без необходимости просеивания и последующих шагов алгоритма!", )
                p, q = next(factor)
                self.entry5.insert(tk.END, str(p))
                self.entry4.insert(tk.END, str(q))
        except Exception as e:
            messagebox.showerror(title='Ошибка', message=f"Ошибка при факторизации числа:\n{e}", )
            print(f"Ошибка при факторизации числа: {e}")



# Создание главного окна
root = tk.Tk()
# Создание приложения
app = MyApp(root)
# Запуск приложения
root.mainloop()
