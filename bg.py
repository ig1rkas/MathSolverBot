from sympy import symbols, Eq, solve, simplify, GreaterThan, LessThan, StrictGreaterThan, StrictLessThan, reduce_inequalities
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def solve_equation(equation_str, variable='x', output_type='auto'):
    """
    Решает математическое уравнение с помощью библиотеки SymPy.
    
    Параметры:
    equation_str (str): строка с уравнением (например, "x**2 + 2x + 1 = 0")
    variable (str): переменная для решения (по умолчанию 'x')
    output_type (str): формат вывода ('auto', 'exact', 'numeric', 'pretty')
    
    Возвращает:
    Список решений или сообщение об ошибке
    """
    try:
        x = symbols(variable)
        
        transformations = (standard_transformations + (implicit_multiplication_application,))
        
        if '=' in equation_str:
            left, right = equation_str.split('=', 1)
            left_expr = parse_expr(left, transformations=transformations)
            right_expr = parse_expr(right, transformations=transformations)
            equation = Eq(left_expr, right_expr)
        else:
            expr = parse_expr(equation_str, transformations=transformations)
            equation = Eq(expr, 0)
        
        solutions = solve(equation, x)
        
        simplified_solutions = [simplify(sol) for sol in solutions]
        
        if output_type == 'pretty':
            return simplified_solutions
        
        elif output_type == 'exact':
            return simplified_solutions
        elif output_type == 'numeric':
            try:
                return [sol.evalf() for sol in simplified_solutions]
            except:
                return simplified_solutions
        else:  
            return simplified_solutions
            
    except Exception as e:
        return f"Ошибка при решении уравнения: {str(e)}"

def solve_inequality(inequality_str, variable='x'):
    """Решает неравенства
    
    Параметры:
    inequality_str (str): строка с уравнением
    variable (str): строка с названием переменной
    
    Возвращает:
    Строку решения неравенство или уведомление об ошибке"""
    try:
        x = symbols(variable)
        # Преобразуем неравенства в символьную форму
        if '>=' in inequality_str:
            left, right = inequality_str.split('>=')
            expr = parse_expr(left) - parse_expr(right)
            inequality = GreaterThan(expr, 0)
        elif '<=' in inequality_str:
            left, right = inequality_str.split('<=')
            expr = parse_expr(left) - parse_expr(right)
            inequality = LessThan(expr, 0)
        elif '>' in inequality_str:
            left, right = inequality_str.split('>')
            expr = parse_expr(left) - parse_expr(right)
            inequality = StrictGreaterThan(expr, 0)
        elif '<' in inequality_str:
            left, right = inequality_str.split('<')
            expr = parse_expr(left) - parse_expr(right)
            inequality = StrictLessThan(expr, 0)
        else:
            return "Неверный формат неравенства"
        
        solution = reduce_inequalities(inequality, x)
        return solution
    except Exception as e:
        return f"Ошибка при решении неравенства: {str(e)}"

def solve_system(equations_list, variables_list):
    """Решает систему уравнений
    
    Параметры:
    equations_list (list): принимает список строк уравнений
    variables_list (list): принимает список строк переменных системы уравнений
    
    Возвращает:
    список решения системы уравнений"""
    try:
        equations = []
        for eq_str in equations_list:
            if '=' in eq_str:
                left, right = eq_str.split('=', 1)
                left_expr = parse_expr(left)
                right_expr = parse_expr(right)
                equations.append(Eq(left_expr, right_expr))
            else:
                equations.append(Eq(parse_expr(eq_str), 0))
        
        sym_vars = symbols(','.join(variables_list))
        
        solutions = solve(equations, sym_vars)
        return solutions
    except Exception as e:
        return f"Ошибка при решении системы: {str(e)}"

