from calculate_savings import input_number, calculate_portion_saved

annual_salary = input_number('the starting annual salary')
total_cost = 10**6
semi_annual_raise = .07
months = 36

portion_saved, bisection_steps = calculate_portion_saved(
    annual_salary, total_cost, semi_annual_raise=semi_annual_raise, months=months)
if portion_saved is None:
    print(f'It is not possible to pay the down payment in three years')
else:
    print(f'Best savings rates: {portion_saved}')
    print(f'Steps in bisection search: {bisection_steps}')
