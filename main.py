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
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    m = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b = y_mean - (m * x_mean)
    
    return [b, m]

def rmse(actual, predicted):
    sum_error = 0.0
    
    for i in range(len(actual)):
        sum_error += (predicted[i] - actual[i])**2
    
    return sqrt(sum_error/len(actual))

def get_predicted_values_and_rmse(dataset):
    test_set = []

    for row in dataset:
        row_copy = list(row)
        row_copy[-1] = None
        test_set.append(row_copy)

    predicted = simple_linear_regression(dataset, test_set)
    actual = [row[-1] for row in dataset]

    return {'predicted_values': predicted, 'rmse': rmse(actual, predicted)}

def simple_linear_regression(dataset, test_set):
    predictions = []
    b, m = coefficients(dataset)
    
    for row in test_set:
        yhat = b + (m * row[0])
        predictions.append(yhat)
    
    return predictions

# dataset = [[1, 1], [1, 3], [2, 3], [4, 3], [3, 2], [5, 5]]
# results = get_predicted_values_and_rmse(dataset)
# print(results)

if __name__ == '__main__':
    csv_data = load_csv()
    dataset = []

    for row in csv_data:
        """
        Corresponding values of index from CSV 
        [1]: Field
        [2]: Current Years of Experience
        [3]: Salary
        """
        data = (row[1], float(row[2]), float(row[3].split('PHP ')[1]))
        dataset.append(data)

    # print(dataset)

    assert len(csv_data) == len(dataset)

    # Plot all the points and colr them based on LEGEND_COLORS
    for data in dataset:
        plt.scatter(data[1] , data[2], color = LEGEND_COLORS.get(data[0]))

    # Legend for colors and their meanings
    legend_academe_blue = mpatches.Patch(color='blue', label='Academe')
    legend_corporate_red = mpatches.Patch(color='red', label='Corporate')
    legend_consultancy_yellow = mpatches.Patch(color='yellow', label='Consultancy')
    legend_government_green = mpatches.Patch(color='green', label='Government')
    legend_startup_purple = mpatches.Patch(color='purple', label='Startup')

    plt.legend(handles=[legend_academe_blue, legend_corporate_red, legend_consultancy_yellow, legend_government_green, legend_startup_purple], loc='lower right')
    plt.title('Filipino Salaries in Software Based on Years of Experience')
    plt.ylabel('Salary in PHP')
    plt.xlabel('Years of Experience')

    max_years_of_experience = max(dataset, key=itemgetter(1))[1]
    max_salary = max(dataset, key=itemgetter(1))[2]

    axes = plt.gca()
    axes.set_xlim([0, max_years_of_experience+1])
    axes.set_ylim([0, max_salary+10000])

    plt.show()

