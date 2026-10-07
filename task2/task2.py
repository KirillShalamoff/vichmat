import os
import re

def check_diag(a, b, c):
    """
    c[i] - главная диагональ
    a[i] - нижняя диагональ (a[0] = 0)
    b[i] - верхняя диагональ (b[N-1] = 0)
    """
    n = len(c)
    is_dominant = True
    strict_count = 0

    print("\n--- Проверка Теоремы 4.2 (Диагональное преобладание) ---")
    for i in range(n):
        c_val = abs(c[i])
        a_val = abs(a[i]) if i > 0 else 0.0
        b_val = abs(b[i]) if i < n - 1 else 0.0
        sum_off = a_val + b_val

        if c_val < sum_off:
            is_dominant = False
            print(f"[-] Нарушение в строке {i+1}: |c[{i+1}]| ({c_val:.4f}) < |a| + |b| ({sum_off:.4f})")
        elif c_val > sum_off:
            strict_count += 1

    if is_dominant:
        if strict_count > 0:
            print(f"[+] Условие выполнено! Найдено строк со строгим преобладанием: {strict_count}. Метод устойчив.")
        else:
            print("[~] Условие выполнено нестрого во всех строках.")
    else:
        print("[-] Условие Теоремы 4.2 НЕ выполнено! Метод прогонки может быть неустойчив.")
    print("-" * 58)
    return is_dominant

def thomas_algorithm(a, b, c, f):
    """
    Метод трёхдиагональной прогонки:
    a[i]*x[i-1] + c[i]*x[i] + b[i]*x[i+1] = f[i]
    """
    n = len(f)
    x = [0.0] * n
    alpha = [0.0] * n
    beta = [0.0] * n

    # Прямой ход
    alpha[0] = -b[0] / c[0]
    beta[0] = f[0] / c[0]

    for i in range(1, n):
        denom = c[i] + a[i] * alpha[i-1]
        if denom == 0:
            raise ValueError(f"Деление на ноль на шаге {i+1}. Прогонка не применима.")

        b_val = b[i] if i < n - 1 else 0.0
        alpha[i] = -b_val / denom
        beta[i] = (f[i] - a[i] * beta[i-1]) / denom

    # Обратный ход
    x[-1] = beta[-1]
    for i in range(n - 2, -1, -1):
        x[i] = alpha[i] * x[i+1] + beta[i]

    return x

def parse_and_solve(filename="input.txt"):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.replace('γ', 'gamma').replace('ε', 'epsilon')

    pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_\[\]]*)\s*=\s*(.*?)(?=(?:[a-zA-Z_][a-zA-Z0-9_\[\]]*\s*=)|[;\n]|$)', re.DOTALL)
    matches = pattern.findall(content)

    params = {'N': 0, 'epsilon': 0.0, 'gamma': 0.0}
    formulas = {}
    explicit_values = {}

    for key, val in matches:
        key = key.strip()
        val = val.strip().rstrip(';')
        if not val:
            continue

        if key in params:
            params[key] = int(val) if key == 'N' else float(val)
        elif '[i]' in key:
            formulas[key] = val
        else:
            match_idx = re.match(r'([a-z_]+)\[(\d+)\]', key, re.IGNORECASE)
            if match_idx:
                arr_name = match_idx.group(1)
                idx = int(match_idx.group(2))
                context = {'epsilon': params['epsilon'], 'gamma': params['gamma']}
                explicit_values[(arr_name, idx)] = float(eval(val, {}, context))

    N = params['N']
    if N <= 0:
        print("Ошибка: N должно быть больше 0.")
        return

    epsilon = params['epsilon']
    gamma = params['gamma']

    a, b, c, f = [], [], [], []

    for i in range(1, N + 1):
        context = {'i': i, 'epsilon': epsilon, 'gamma': gamma}

        val_a = eval(formulas.get('a[i]', '0'), {}, context)
        val_b = eval(formulas.get('b[i]', '0'), {}, context)
        val_c = eval(formulas.get('c[i]', '0'), {}, context)
        val_f = eval(formulas.get('f[i]', '0'), {}, context)

        if ('a', i) in explicit_values: val_a = explicit_values[('a', i)]
        if ('b', i) in explicit_values: val_b = explicit_values[('b', i)]
        if ('c', i) in explicit_values: val_c = explicit_values[('c', i)]
        if ('f', i) in explicit_values: val_f = explicit_values[('f', i)]

        a.append(float(val_a))
        b.append(float(val_b))
        c.append(float(val_c))
        f.append(float(val_f))

    print(f"--- Входные данные (N={N}, epsilon={epsilon}, gamma={gamma}) ---")

    check_diag(a, b, c)

    try:
        x = thomas_algorithm(a, b, c, f)
        print("--- Результат (вектор X) ---")
        for i, val in enumerate(x):
            print(f"x[{i+1:2d}] = {val:.8f}")
    except ValueError as e:
        print("\nОшибка при расчете:", e)

if __name__ == "__main__":
    parse_and_solve()
