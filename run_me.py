# Import the base settings
import configs
from custom_policy_function import run_custom_policy_simulation
from plots import output_plots
import pandas as pd
import time

print('='*16+' Starting Simulation... '+'='*16)
# Recieve the number of iterations as an argument
print('Please enter number of iterations for each configuration')
loops_str = input('Number of Iterations: ')
print('-'*56)
try:
  loops = int(loops_str)
  print('Running Configuration 1...')
  first = run_custom_policy_simulation(loops, configs.config1)
  print('Configuration 1 complete.')
  print('-'*56)
  
  print('Running Configuration 2...')
  second = run_custom_policy_simulation(loops, configs.config2)
  print('Configuration 2 complete.')
  print('-'*56)
  
  print('Running Configuration 3...')
  third = run_custom_policy_simulation(loops, configs.config3)
  print('Configuration 3 complete.')
  
  print('-'*56)
# Output the results as an Excel file
  sum_of_package_days_df = pd.DataFrame({
    '1st': first['sum_of_package_days'],
    '2nd': second['sum_of_package_days'],
    '3rd': third['sum_of_package_days'],
  })
  timestr = time.strftime("%Y%m%d-%H%M%S")
  file_name = f'{timestr}_locker_configurations_comparison_{loops}_iterations.xlsx'
  print('Creating an Excel file under the name:')
  print(file_name)
  print('At the current directory.')
  with pd.ExcelWriter(file_name) as writer:
    sum_of_package_days_df.to_excel(writer, sheet_name='Sum of Package Days')
    first['arrival_until_placement_df'].to_excel(writer, sheet_name='1st Arrival Until Placement')
    second['arrival_until_placement_df'].to_excel(writer, sheet_name='2nd Arrival Until Placement')
    third['arrival_until_placement_df'].to_excel(writer, sheet_name='3rd Arrival Until Placement')
    first['packages_left_df'].to_excel(writer, sheet_name='1st Packages Left At Center')
    second['packages_left_df'].to_excel(writer, sheet_name='2nd Packages Left At Center')
    third['packages_left_df'].to_excel(writer, sheet_name='3rd Packages Left At Center')
    pack_return_df = pd.DataFrame({
        '1st': first['pack_return_av'],
        '2nd': second['pack_return_av'],
        '3rd': third['pack_return_av'],
    }, index=[0]).T
    pack_return_df.to_excel(writer, sheet_name='Package Return Average')
    customer_return_avg_df = pd.DataFrame({
        '1st': first['customer_return_avg_new'],
        '2nd': second['customer_return_avg_new'],
        '3rd': third['customer_return_avg_new'],
    }, index=[0]).T
    customer_return_avg_df.to_excel(writer, sheet_name='Customer Returns Average')
  print('-'*56)

  print('Printing plots...')
  output_plots(first, second, third)
  print('Plots printed successfully.')
  print('='*17 + ' Simulation Complete! ' + '='*17)

except ValueError as e:
  print(e)
  print('Error! Please enter an integer to start the simulation.')
