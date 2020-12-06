from calculate_savings import input_number, calculate_savings

annual_salary = input_number('the starting annual salary')
portion_saved = input_number('the portion of salary to be saved')
total_cost = input_number('the cost of your dream home')
semi_annual_raise = input_number('semi­annual raise percentage')

months_needed = calculate_savings(
    annual_salary, portion_saved, total_cost, semi_annual_raise=semi_annual_raise)
print(f'Number of months: {months_needed}')
