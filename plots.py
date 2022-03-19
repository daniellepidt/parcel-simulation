import statistics
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn-darkgrid")
from globals import SIM_TIME

def tic_avg_to_unite(tic_avg):
    tic_temp = [{} for i in range(3)]
    for z in range(3):  # For each size
        for l in tic_avg[z]:  # For each loop
            for key in tic_avg[z][l]:  #
                if tic_avg[z][l][key] in tic_temp[z].keys():
                    if l in tic_temp[z][tic_avg[z][l][key]].keys():
                        tic_temp[z][tic_avg[z][l][key]][l] += 1
                    else:
                        tic_temp[z][tic_avg[z][l][key]][l] = 1
                else:
                    tic_temp[z][tic_avg[z][l][key]] = {}
                    tic_temp[z][tic_avg[z][l][key]][l] = 1
    for z in range(3):  # Calculating the mean for all the loops
        for p in tic_temp[z]:
            tic_temp[z][p] = statistics.mean(tic_temp[z][p].values())

    tic_unite = [{} for z in range(3)]  # Uniting in groups of 50
    for z in range(3):  # For each size
        for p in tic_temp[z]:  # For each # of packages
            if p % 50 > 0 and int(p/50) in tic_unite[z].keys():
                tic_unite[z][int(p/50)] += tic_temp[z][p]
            else:
                tic_unite[z][int(p/50)] = tic_temp[z][p]
    return tic_unite

def output_results(tpa_lst, tic_avg, customer_return, pack_return=False):
    # For analysis
    # Measure #1
    # Calculate the average
    for i in range(6):
        for j in range(0, SIM_TIME+1):
            tpa_lst[i][j] = statistics.mean(tpa_lst[i][j])
    areas_indexes = {j: f"Area {j+1}" for j in range(0, 6)}
    df1 = pd.DataFrame(tpa_lst).rename(index=areas_indexes).T
    df1 = df1.loc[~(df1 == 0).all(axis=1)]

    # Measure #2
    # Calculating the # of packages and which day there was this amount
    tic_unite = tic_avg_to_unite(tic_avg)
    df2 = pd.DataFrame(tic_unite).rename(index={0: 'Small', 1: 'Medium', 2: 'Large'}).T.sort_index()
    df2 = df2.rename(index={j: f'{j * 50}-{(j + 1) * 50 -1}' for j in range(len(df2.index))})
    # Measure no.3
    if pack_return:
      pack_return_av = statistics.mean(pack_return)

    # Measure no.4
    customer_return_avg_new = statistics.mean(customer_return)

    return {
        'arrival_until_placement_df': df1,
        'packages_left_df': df2,
        'pack_return_av': pack_return_av,
        'customer_return_avg_new': customer_return_avg_new,
    }

def output_plots(first, second, third):
    dfs = [first, second, third]
    fig, axes = plt.subplots(nrows=2, ncols=4)
    fig.suptitle('Locker Configurations Comparison:', fontsize=20)
    figsize = (18, 6)
    fig.tight_layout() # Fit plots to window size.

    # Find maximal values for both plots' y-axis, in order to create a standard height for all of them.
    list_max_days_in_plot = []
    list_max_packages_in_plot = []
    for i in dfs:
        list_max_days_in_plot.append(i['arrival_until_placement_df'].sum(axis=1).max())
        list_max_packages_in_plot.append(i['packages_left_df'].sum(axis=1).max())
    max_value_days_in_plot = max(list_max_days_in_plot)
    max_value_packages_in_plot = max(list_max_packages_in_plot)


    for i in range(len(dfs)):
    # Visualization of the average
        df1 = dfs[i]['arrival_until_placement_df']
        df1_length = len(df1.index)
        ax1 = df1.plot.bar(
            stacked=True,
            rot=0,
            figsize=figsize,
            xticks=[i for i in range(0, df1_length, 5)],
            ylim=[0, max_value_days_in_plot],
            title=f'Config {i+1} - Time Until Placement',
            xlabel='Days',
            ylabel='Packages',
            ax=axes[0, i],
            legend=i==0,
        )

        df2 = dfs[i]['packages_left_df']
        ax2 = df2.plot.bar(
            stacked=True,
            rot=45,
            figsize=figsize,
            ylim=[0, max_value_packages_in_plot],
            title=f'Config {i+1} - Packages at Day\'s End',
            xlabel='Packages',
            ylabel='Days',
            ax=axes[1, i],
            legend=i==0,
        )
    
    df3 = pd.DataFrame({
        '1st': dfs[0]['pack_return_av'],
        '2nd': dfs[1]['pack_return_av'],
        '3rd': dfs[2]['pack_return_av'],
    }, index=[0]).T
    ax3 = df3.plot.bar(
    rot=0,
    figsize=figsize,
    title='Measure #3 - Package Return Average',
    xlabel='Configuration',
    ylabel='Packages',
    ax=axes[0, 3],
    legend=False
    )

    df4 = pd.DataFrame({
        '1st': dfs[0]['customer_return_avg_new'],
        '2nd': dfs[1]['customer_return_avg_new'],
        '3rd': dfs[2]['customer_return_avg_new'],
    }, index=[0]).T
    ax4 = df4.plot.bar(
    rot=0,
    figsize=figsize,
    title='Measure #4 - Customer Returns Average',
    xlabel='Configuration',
    ylabel='Customer Returns',
    ax=axes[1, 3],
    legend=False
    )
    
    plt.show()
