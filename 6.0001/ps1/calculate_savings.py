months_per_year = 12
months_per_half_year = months_per_year // 2


def input_number(varName):
    try:
        return float(input(f"Enter {varName} as a float number: "))
    except:
        print('ERROR: That was not a number')
        exit(-1)


def add_savings(current_savings, r, monthly_salary, portion_saved):
    current_savings += current_savings * r / months_per_year
    current_savings += monthly_salary * portion_saved
    return current_savings


def update_annual_salary(months, semi_annual_raise, annual_salary):
    monthly_salary = annual_salary / months_per_year
    if semi_annual_raise > 0 and months > 0 and months % months_per_half_year == 0:
        annual_salary += annual_salary * semi_annual_raise
        monthly_salary = annual_salary / months_per_year
    return annual_salary, monthly_salary


def calculate_savings(annual_salary, portion_saved, total_cost, semi_annual_raise=0, r=0.04, portion_down_payment=0.25):
    monthly_salary = annual_salary / months_per_year
    annual_salary, monthly_salary = update_annual_salary(
        0, semi_annual_raise, annual_salary)
    months_needed = 0
    current_savings = 0

    down_payment = total_cost * portion_down_payment
    while current_savings < down_payment:
        months_needed += 1
        current_savings = add_savings(
            current_savings, r, monthly_salary, portion_saved)
        annual_salary, monthly_salary = update_annual_salary(
            months_needed, semi_annual_raise, annual_salary)

    return months_needed


def calculate_portion_saved(annual_salary, total_cost, semi_annual_raise=0, months=12, r=0.04, portion_down_payment=0.25, end=10**4, toleration=100):
    start = 0
    denom = end
    start_annual_salary = annual_salary
    down_payment = total_cost * portion_down_payment
    portion_saved = None
    bisection_steps = 0

    while start < end - 1:
        bisection_steps += 1
        mid = (start + end) // 2
        portion_saved = mid * 1. / denom
        annual_salary = start_annual_salary
        monthly_salary = annual_salary / months_per_year
        current_savings = 0
        months_needed = months

        while months_needed > 0:
            months_needed -= 1
            current_savings = add_savings(
                current_savings, r, monthly_salary, portion_saved)
            annual_salary, monthly_salary = update_annual_salary(
                months_needed, semi_annual_raise, annual_salary)
            if current_savings > down_payment - toleration:
                break

        if abs(current_savings - down_payment) < toleration:
            break
        elif current_savings > down_payment + toleration:
            end = mid
        elif current_savings < down_payment - toleration:
            portion_saved = None
            start = mid

    return portion_saved, bisection_steps
