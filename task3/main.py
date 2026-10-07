def compute_f(A, x):
    """Вычисляет вектор f = A * x"""
    n = len(A)
    f = [0.0] * n
    for i in range(n):
        f[i] = sum(A[i][j] * x[j] for j in range(n))
    return f

def evaluate_norms(A, f, x_exact, x_k):
    """Вычисляет бесконечные (максимальные) нормы невязки и погрешности"""
    n = len(A)
    norm_r = 0.0
    norm_z = 0.0
    for i in range(n):
        # Вычисляем i-ю компоненту невязки r = Ax - f
        ax_i = sum(A[i][j] * x_k[j] for j in range(n))
        r_i = abs(ax_i - f[i])
        if r_i > norm_r:
            norm_r = r_i

        # Вычисляем i-ю компоненту погрешности z = x_k - x_exact
        z_i = abs(x_k[i] - x_exact[i])
        if z_i > norm_z:
            norm_z = z_i

    return norm_r, norm_z

def solve_jacobi(A, f, x_exact):
    n = len(A)
    x = [0.0] * n  # Начальное приближение x_0 = 0
    k = 0
    res_4, err_4, res_6, err_6 = -1, -1, -1, -1

    while True:
        norm_r, norm_z = evaluate_norms(A, f, x_exact, x)

        # Фиксируем шаги достижения нужной точности
        if norm_r < 1e-4 and res_4 == -1: res_4 = k
        if norm_z < 1e-4 and err_4 == -1: err_4 = k
        if norm_z < 1e-6 and err_6 == -1: err_6 = k

        # Остановка по невязке
        if norm_r < 1e-6:
            res_6 = k
            break
        # Вычисление следующего шага x^(k+1)
        x_new = [0.0] * n
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (f[i] - s) / A[i][i]

        x = x_new
        k += 1

    return res_4, err_4, res_6, err_6

def solve_seidel(A, f, x_exact):
    n = len(A)
    x = [0.0] * n  # Начальное приближение x_0 = 0
    k = 0
    res_4, err_4, res_6, err_6 = -1, -1, -1, -1

    while True:
        norm_r, norm_z = evaluate_norms(A, f, x_exact, x)

        if norm_r < 1e-4 and res_4 == -1: res_4 = k
        if norm_z < 1e-4 and err_4 == -1: err_4 = k
        if norm_z < 1e-6 and err_6 == -1: err_6 = k

        if norm_r < 1e-6:
            res_6 = k
            break

        # Вычисление следующего шага (значения x обновляются сразу)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (f[i] - s) / A[i][i]

        k += 1

    return res_4, err_4, res_6, err_6

def main():
    # Чтение данных из файла
    try:
        with open("input.txt", "r") as f_in:
            # Читаем все числа из файла, игнорируя переносы строк
            data = [float(x) for x in f_in.read().split()]
    except FileNotFoundError:
        print("Ошибка: Файл input.txt не найден.")
        return

    n = int(data[0])
    idx = 1

    # Заполнение матрицы A
    A = []
    for _ in range(n):
        row = []
        for _ in range(n):
            row.append(data[idx])
            idx += 1
        A.append(row)

    # Заполнение вектора точного решения x
    x_exact = data[idx : idx + n]

    # Вычисление вектора f
    f = compute_f(A, x_exact)

    # Решение
    j_r4, j_e4, j_r6, j_e6 = solve_jacobi(A, f, x_exact)
    s_r4, s_e4, s_r6, s_e6 = solve_seidel(A, f, x_exact)

    # Запись результатов
    with open("output.txt", "w", encoding="utf-8") as f_out:
        f_out.write("Матрица A:\n")
        for i, row in enumerate(A):
            row_str = ", ".join(f"{val:g}" for val in row)
            f_out.write(row_str + (",\n" if i < n - 1 else "\n"))

        f_out.write("Вектор f:\n")
        f_out.write(", ".join(f"{val:g}" for val in f) + "\n")

        f_out.write("Точное решение x:\n")
        f_out.write(", ".join(f"{val:g}" for val in x_exact) + "\n")

        f_out.write("epsilon = 1e-4\n")
        f_out.write(f"Метод Якоби сходится по невязке за {j_r4} шагов, по погрешности за {j_e4} шагов.\n")
        f_out.write(f"Метод Зейделя сходится по невязке за {s_r4} шагов, по погрешности за {s_e4} шагов.\n")

        f_out.write("epsilon = 1e-6\n")
        f_out.write(f"Метод Якоби сходится по невязке за {j_r6} шагов, по погрешности за {j_e6} шагов.\n")
        f_out.write(f"Метод Зейделя сходится по невязке за {s_r6} шагов, по погрешности за {s_e6} шагов.\n")

    print("Расчёт завершен. Результаты в файле output.txt")

if __name__ == "__main__":
    main()