import math

DELTA = 1e-7

def f(x, a, b, c):
    return x**3 + a * x**2 + b * x + c

def bisection(a, b, c, left, right, EPS):
    f_left = f(left, a, b, c)
    f_right = f(right, a, b, c)

    if f_left * f_right > 0:
        return None, 0

    if f_left == 0: return left, 0
    if f_right == 0: return right, 0

    iters = 0
    while (right - left) / 2.0 > EPS:
        iters += 1
        mid = (left + right) / 2.0
        f_mid = f(mid, a, b, c)

        if f_mid == 0:
            return mid, iters

        if f_left * f_mid < 0:
            right = mid
            f_right = f_mid
        else:
            left = mid
            f_left = f_mid

    return (left + right) / 2.0, iters


def main():
    try:
        with open("input.txt", "r") as file:
            print("--- Тестирование ---")
            count = 0
            for line_idx, line in enumerate(file, 1):
                parts = line.strip().split()
                if not parts:
                    continue
                count += 1
                try:
                    # Считываем коэффициенты и точность
                    a, b, c, EPS = map(float, parts[:4])
                except ValueError:
                    print(f"Строка {line_idx}: Ошибка чтения данных ({line.strip()})")
                    continue

                print(f"\nТЕСТ №{count} Уравнение: x^3 + ({a})x^2 + ({b})x + ({c}) = 0 при EPS={EPS}")
                
                # Заданный отрезок
                left_bound = -4.0
                right_bound = -3.0
                
                # Ищем корень методом бисекции именно на этом отрезке
                root, iters = bisection(a, b, c, left_bound, right_bound, EPS)

                if root is not None:
                    print(f"  Корень на отрезке [{left_bound}, {right_bound}]: {root:12.8f} | Итераций: {iters}")
                else:
                    print(f"  На отрезке [{left_bound}, {right_bound}] метод бисекции не применим (знаки на концах совпадают).")

    except FileNotFoundError:
        print("Ошибка: Файл 'input.txt' не найден!")


if __name__ == "__main__":
    main()
