def input_number(varName):
    try:
        return float(input(f"Enter {varName} as a float number: "))
    except:
        print('ERROR: That was not a number')
        exit(-1)


def calculate_savings(annual_salary, portion_saved, total_cost, semi_annual_raise=0, r=0.04, portion_down_payment=0.25):
    months_per_year = 12
    months_per_half_year = months_per_year // 2

    monthly_salary = annual_salary / months_per_year
    months_needed = 0
    current_savings = 0

    down_payment = total_cost * portion_down_payment
    while current_savings < down_payment:
        current_savings += current_savings * r / months_per_year
        current_savings += monthly_salary * portion_saved
        months_needed += 1
        if semi_annual_raise > 0 and months_needed % months_per_half_year == 0:
            annual_salary += annual_salary * semi_annual_raise
            monthly_salary = annual_salary / months_per_year

    return months_needed
