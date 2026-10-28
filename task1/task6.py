def f(xx):
    return xx**3 - 10 * xx + 20

def df(xx):
    return 3 * xx**2 - 10

# Разделительная рамка и шапка
BORDER = "+-----+-------------+-------------+---------------+---------------+----------------+-------------------+"
HEADER = "|  n  |     x_n     |   f(x_n)    | |dx_n| < eps  | delta_n < eps |  |f(x_n)| < eps | delta_n < delta/2 |"

def print_table_header(title):
    print(f"\n{title}")
    print(BORDER)
    print(HEADER)
    print(BORDER)

def print_row(n, x, fx, dx_str, delta_str, fx_str, rate_str):
    # Фиксированная ширина столбцов с выравниванием
    print(f"| {n:<3} | {x:<11.6f} | {fx:<11.6f} | {dx_str:^13} | {delta_str:^13} | {fx_str:^14} | {rate_str:^17} |")


def newton_method(x0, eps, z):
    print_table_header("=== Метод Ньютона ===")
    x = x0
    delta_prev = abs(x - z)
    
    # n = 0
    print_row(0, x, f(x), "-", "да" if delta_prev < eps else "нет", "да" if abs(f(x)) < eps else "нет", "-")
    
    for n in range(1, 20):
        x_prev = x
        x = x_prev - f(x_prev) / df(x_prev)
        dx = abs(x_prev - x)
        delta_n = abs(x - z)
        fx = abs(f(x))
        
        cond1 = "да" if dx < eps else "нет"
        cond2 = "да" if delta_n < eps else "нет"
        cond3 = "да" if fx < eps else "нет"
        cond4 = "да" if delta_n < delta_prev / 2 else "нет"
        
        print_row(n, x, f(x), cond1, cond2, cond3, cond4)
        delta_prev = delta_n
        if dx < eps:
            break
    print(BORDER)


def simplified_newton(x0, eps, z):
    print_table_header("=== Упрощённый метод Ньютона ===")
    x = x0
    df_x0 = df(x0)
    delta_prev = abs(x - z)
    
    print_row(0, x, f(x), "-", "да" if delta_prev < eps else "нет", "да" if abs(f(x)) < eps else "нет", "-")
    
    for n in range(1, 20):
        x_prev = x
        x = x_prev - f(x_prev) / df_x0
        dx = abs(x_prev - x)
        delta_n = abs(x - z)
        fx = abs(f(x))
        
        cond1 = "да" if dx < eps else "нет"
        cond2 = "да" if delta_n < eps else "нет"
        cond3 = "да" if fx < eps else "нет"
        cond4 = "да" if delta_n < delta_prev / 2 else "нет"
        
        print_row(n, x, f(x), cond1, cond2, cond3, cond4)
        delta_prev = delta_n
        if dx < eps:
            break
    print(BORDER)


def secant_method(x0, x1, eps, z):
    print_table_header("=== Метод секущих ===")
    
    delta_0 = abs(x0 - z)
    print_row(0, x0, f(x0), "-", "да" if delta_0 < eps else "нет", "да" if abs(f(x0)) < eps else "нет", "-")
    
    delta_1 = abs(x1 - z)
    dx_1 = abs(x1 - x0)
    cond1 = "да" if dx_1 < eps else "нет"
    cond2 = "да" if delta_1 < eps else "нет"
    cond3 = "да" if abs(f(x1)) < eps else "нет"
    cond4 = "да" if delta_1 < delta_0 / 2 else "нет"
    print_row(1, x1, f(x1), cond1, cond2, cond3, cond4)
    
    x_prev2 = x0
    x_prev1 = x1
    delta_prev = delta_1
    
    for n in range(2, 20):
        x = x_prev1 - f(x_prev1) * (x_prev1 - x_prev2) / (f(x_prev1) - f(x_prev2))
        dx = abs(x - x_prev1)
        delta_n = abs(x - z)
        fx = abs(f(x))
        
        cond1 = "да" if dx < eps else "нет"
        cond2 = "да" if delta_n < eps else "нет"
        cond3 = "да" if fx < eps else "нет"
        cond4 = "да" if delta_n < delta_prev / 2 else "нет"
        
        print_row(n, x, f(x), cond1, cond2, cond3, cond4)
        delta_prev = delta_n
        x_prev2 = x_prev1
        x_prev1 = x
        if dx < eps:
            break
    print(BORDER)


# Точный корень из пункта 1 и параметры
z_exact = -3.8910204097628593
eps = 1e-5
x0 = -4.0
x1 = -3.9

# Запуск методов
newton_method(x0, eps, z_exact)
simplified_newton(x0, eps, z_exact)
secant_method(x0, x1, eps, z_exact)
