from math import sqrt
from csv import reader
from operator import itemgetter

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

FILENAME = 'software_salary_data.csv'

LEGEND_COLORS = {
    'Academe': 'blue',
    'Corporate': 'red',
    'Consultancy': 'yellow',
    'Government': 'green',
    'Startup': 'purple'
}

MAX_YEARS_YEARS_OF_EXPERIENCE = 0
MAX_SALARY = 0

def load_csv():
    dataset = []
    with open(FILENAME, 'r') as file:
        csv_reader = reader(file)
        firstline = True
        for row in csv_reader:
            if firstline:
                firstline = False
                continue
            if not row:
                continue
            dataset.append(row)
    return dataset

def mean(values):
    return sum(values) / len(values)

def variance(values, mean):
    return sum([(x - mean)**2 for x in values])

def covariance(x, mean_x, y, mean_y):
    covar = 0.0

    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)

    return covar

def coefficients(dataset):
    x = [row[1] for row in dataset]
    y = [row[2] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    m = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b = y_mean - (m * x_mean)
    
    return (b, m)

def rmse(actual_values, predicted_values):
    sum_error = 0.0
    
    for i in range(len(actual_values)):
        year = actual_values[i][0]
        actual_value = actual_values[i][1]
        predicted_value = predicted_values[year]

        # print('{} | year: {} | actual: {} | predicted: {} | difference: {}'.format(
        #     i, year, actual_value, predicted_value, predicted_value - actual_value))

        sum_error += (predicted_value - actual_value)**2

    rmse =  sqrt(sum_error/len(actual_values))
    
    return rmse

def get_predicted_values_and_rmse(dataset):
    test_set = []

    for row in dataset:
        row_copy = list(row)
        row_copy[-1] = None
        test_set.append(row_copy)

    (predicted_values, b, m) = simple_linear_regression(dataset, test_set)
    # Make all years ints to calculate RMSE
    actual_values = [(int(row[1]), row[2]) for row in dataset]
    linear_regression_model = 'y = {}x + {}'.format(m, b)

    return {
        'predicted_values': predicted_values, 
        'rmse': rmse(actual_values, predicted_values),
        'linear_regression_model': linear_regression_model
    }

def simple_linear_regression(dataset, test_set):
    predicted_values = []
    b, m = coefficients(dataset)
    
    for year in range(int(MAX_YEARS_YEARS_OF_EXPERIENCE)+1):
        yhat = (m * year) + b
        predicted_values.append(yhat)
    
    return (predicted_values, round(b, 2), round(m, 2))


if __name__ == '__main__':
    csv_data = load_csv()
    overall_dataset = []
    corporate_dataset = []
    startup_dataset = []

    for row in csv_data:
        """
        Corresponding values of index from CSV 
        [1]: Field
        [2]: Current Years of Experience
        [3]: Salary
        """
        data = (row[1], float(row[2]), float(row[3].split('PHP ')[1]))
        overall_dataset.append(data)

        if row[1] == 'Corporate':
            corporate_dataset.append(data)
        elif row[1] == 'Startup':
            startup_dataset.append(data)

    assert len(csv_data) == len(overall_dataset)

    # Plot all the points and colr them based on LEGEND_COLORS
    for data in overall_dataset:
        plt.scatter(data[1] , data[2], color=LEGEND_COLORS.get(data[0]))

    # Legend for colors and their meanings
    legend_academe_blue = mpatches.Patch(color='blue', label='Academe')
    legend_corporate_red = mpatches.Patch(color='red', label='Corporate')
    legend_consultancy_yellow = mpatches.Patch(color='yellow', label='Consultancy')
    legend_government_green = mpatches.Patch(color='green', label='Government')
    legend_startup_purple = mpatches.Patch(color='purple', label='Startup')

    plt.title('Filipino Salaries in Software Based on Years of Experience')
    plt.ylabel('Salary in PHP')
    plt.xlabel('Years of Experience')

    MAX_YEARS_YEARS_OF_EXPERIENCE = max(overall_dataset, key=itemgetter(1))[1]
    MAX_SALARY = max(overall_dataset, key=itemgetter(1))[2]

    axes = plt.gca()
    axes.set_xlim([0, MAX_YEARS_YEARS_OF_EXPERIENCE+1])
    axes.set_ylim([0, MAX_SALARY+40000])

    overall_results = get_predicted_values_and_rmse(overall_dataset)
    print('Overall Results')
    print(overall_results)
    
    corporate_results = get_predicted_values_and_rmse(corporate_dataset)
    print('Corporate Results')
    print(corporate_results)

    startup_results = get_predicted_values_and_rmse(startup_dataset)
    print('Startup Results')
    print(startup_results)

    legend_startup_cyan = mpatches.Patch(color='cyan', label='Salary Regression Line: {}'.format(overall_results.get('linear_regression_model')))
    legend_startup_black = mpatches.Patch(color='black', label='Corporate Regression Line: {}'.format(corporate_results.get('linear_regression_model')))
    legend_startup_magenta = mpatches.Patch(color='magenta', label='Startup Regression Line: {}'.format(startup_results.get('linear_regression_model')))

    plt.legend(
        handles=[legend_academe_blue, legend_corporate_red, legend_consultancy_yellow, legend_government_green, legend_startup_purple, legend_startup_cyan, legend_startup_black, legend_startup_magenta], 
        bbox_to_anchor=(1.05,1),
        borderaxespad=0,
        loc=2)

    for year, value in enumerate(overall_results['predicted_values']):
        plt.scatter(year , value, color='cyan')

    for year, value in enumerate(corporate_results['predicted_values']):
        plt.scatter(year , value, color='black')

    for year, value in enumerate(startup_results['predicted_values']):
        plt.scatter(year , value, color='magenta')

    years = [i for i in range(int(MAX_YEARS_YEARS_OF_EXPERIENCE)+1)]
    overall_predicted_values = [value for value in overall_results['predicted_values']]
    corporate_predicted_values = [value for value in corporate_results['predicted_values']]
    startup_predicted_values = [value for value in startup_results['predicted_values']]

    plt.plot(years, overall_predicted_values,  color='cyan')
    plt.plot(years, corporate_predicted_values,  color='black')
    plt.plot(years, startup_predicted_values,  color='magenta')

    plt.show()
