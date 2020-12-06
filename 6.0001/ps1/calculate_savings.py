def input_number(varName):
    try:
        return float(input(f"Enter {varName} as a float number: "))
    except:
        print('ERROR: That was not a number')
        exit(-1)


def calculate_savings(annual_salary, portion_saved, total_cost, r=0.04, portion_down_payment=0.25):
    months_per_year = 12

    monthly_salary = annual_salary / months_per_year
    months_needed = 0
    current_savings = 0

    down_payment = total_cost * portion_down_payment
    while current_savings < down_payment:
        current_savings += current_savings * r / months_per_year
        current_savings += monthly_salary * portion_saved
        months_needed += 1

    return months_needed
