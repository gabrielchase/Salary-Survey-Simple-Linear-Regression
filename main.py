from math import sqrt
from csv import reader

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

FILENAME = 'software_salary_data.csv'
""" 
[1]: Field
[2]: Current Years of Experience
[3]: Salary
"""

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

def simple_linear_regression(train, test):
    predictions = []
    b, m = coefficients(train)
    
    for row in test:
        yhat = b + (m * row[0])
        predictions.append(yhat)
    
    return predictions

# dataset = [[1, 1], [2, 3], [4, 3], [3, 2], [5, 5]]
# results = get_predicted_values_and_rmse(dataset)


dataset = load_csv()

field = []
years_of_experience = []
salary = []
legend_colors = {
    'Academe': 'blue',
    'Corporate': 'red',
    'Consultancy': 'yellow',
    'Government': 'green',
    'Startup': 'purple'
}

for row in dataset:
    field.append(row[1])
    years_of_experience.append(float(row[2]))
    salary.append(float(row[3].split('PHP ')[1]))

assert len(dataset) == len(field) == len(years_of_experience) == len(salary) 

# Plot all the points and colr them based on legend_colors
for idx, val in enumerate(dataset):
    plt.scatter(years_of_experience[idx] , salary[idx], color = legend_colors.get(field[idx]))

# Legend for colors and their meanings
legend_academe_blue = mpatches.Patch(color='blue', label='Academe')
legend_corporate_red = mpatches.Patch(color='red', label='Corporate')
legend_consultancy_yellow = mpatches.Patch(color='yellow', label='Consultancy')
legend_government_green = mpatches.Patch(color='green', label='Government')
legend_startup_purple = mpatches.Patch(color='purple', label='Startup')

plt.legend(handles=[legend_academe_blue, legend_corporate_red, legend_consultancy_yellow, legend_government_green, legend_startup_purple], loc='upper left')
plt.title('Filipino Salaries in Software Based on Years of Experience')
plt.ylabel('Salary in PHP')
plt.xlabel('Years of Experience')
plt.show()

