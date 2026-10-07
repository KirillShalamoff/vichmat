import math

DELTA = 1e-7  # Порог сравнения с нулем для floating-point чисел

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

def solve_cubic(a, b, c, EPS):
    R = 1.0 + max(abs(a), abs(b), abs(c))
    D_deriv = a**2 - 3*b
    roots = []

    # 1. Проверка на корень кратности 3 (когда D_deriv ≈ 0)
    if abs(D_deriv) <= DELTA:
        x_inflect = -a / 3.0
        # Если в точке перегиба значение функции близко к 0, это корень кратности 3
        if abs(f(x_inflect, a, b, c)) <= DELTA:
            roots.append((x_inflect, 3, 0))
            return roots
        else:
            # Монотонная функция с 1 простым корнем
            root, iters = bisection(a, b, c, -R, R, EPS)
            if root is not None:
                roots.append((root, 1, iters))
            return roots

    if D_deriv < -DELTA:
        # Экстремумов нет, строго монотонная функция -> 1 простой корень
        root, iters = bisection(a, b, c, -R, R, EPS)
        if root is not None:
            roots.append((root, 1, iters))
    else:
        # Два экстремума
        x1 = (-a - math.sqrt(D_deriv)) / 3.0
        x2 = (-a + math.sqrt(D_deriv)) / 3.0

        y1, y2 = f(x1, a, b, c), f(x2, a, b, c)

        # Левый интервал [-R, x1]
        if y1 > DELTA:
            root, iters = bisection(a, b, c, -R, x1, EPS)
            if root is not None: roots.append((root, 1, iters))

        # Локальный максимум - корень кратности 2
        if abs(y1) <= DELTA:
            roots.append((x1, 2, 0))

        # Средний интервал [x1, x2]
        if y1 * y2 < -DELTA:
            root, iters = bisection(a, b, c, x1, x2, EPS)
            if root is not None: roots.append((root, 1, iters))

        # Локальный минимум - корень кратности 2
        if abs(y2) <= DELTA:
            roots.append((x2, 2, 0))

        # Правый интервал [x2, R]
        if y2 < -DELTA:
            root, iters = bisection(a, b, c, x2, R, EPS)
            if root is not None: roots.append((root, 1, iters))

    return roots

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
                    a, b, c, EPS = map(float, parts[:4])
                except ValueError:
                    print(f"Строка {line_idx}: Ошибка чтения данных ({line.strip()})")
                    continue

                print(f"\nТЕСТ №{count} Уравнение: x^3 + ({a})x^2 + ({b})x + ({c}) = 0 при EPS={EPS}")
                roots = solve_cubic(a, b, c, EPS)

                for r, mult, iters in roots:
                    print(f"  Корень: {r:12.8f} | Кратность: {mult} | Итераций: {iters}")

    except FileNotFoundError:
        print("Ошибка: Файл 'input.txt' не найден!")

if __name__ == "__main__":
    main()
