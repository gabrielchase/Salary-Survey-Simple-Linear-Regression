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
    """ Compute for the least-squares estimators in the given dataset. Dataset must be a tuple """

    x = [row[1] for row in dataset]
    y = [row[2] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    m = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b = y_mean - (m * x_mean)
    
    return (b, m)

def rmse(actual_values, predicted_values):
    """ 
        Computes the RMSE
        `actual_values` MUST BE A TUPLE containing the year and the actual salary  
        `predicted_values` must be the corresponding predicted salary per year. 
            - It's index is its respective year
    """

    sum_error = 0.0
    
    # Iterate through all values in `actual_values`
    for i in range(len(actual_values)):
        # Get the year and value of the current index in actual value
        year = actual_values[i][0]
        actual_value = actual_values[i][1]
        
        # Get the predicted value corresponding to the current actual value's year
        predicted_value = predicted_values[year]
        
        sum_error += (predicted_value - actual_value)**2

    rmse =  sqrt(sum_error/len(actual_values))
    
    return rmse

def r_squared(actual_values, predicted_values):
    """ 
        Computes the R^2 value.
        `actual_values` MUST BE A TUPLE containing the year and the actual salary  
        `predicted_values` must be the corresponding predicted salary per year. 
            - It's index is its respective year
    """
    
    actual_sum = 0
    predicted_sum = 0

    y_values = [row[1] for row in actual_values]
    y_mean = mean(y_values)

    for val in actual_values:
        year = val[0]
        salary = val[1]
        predicted_sum += (predicted_values[year] - y_mean)**2
        actual_sum += (salary - y_mean)**2

    return predicted_sum/actual_sum

def get_results(dataset):
    """ 
        Get the linear regression model, predicted values per year, 
        RMSE, and R^2 value  of the given dataset 
    """

    test_set = []

    for row in dataset:
        row_copy = list(row)
        row_copy[-1] = None
        test_set.append(row_copy)

    (predicted_values, b, m) = simple_linear_regression(dataset, test_set)
    # Make all years ints to calculate RMSE
    actual_values = [(int(row[1]), row[2]) for row in dataset]
    linear_regression_model = 'y = {}x + {}'.format(round(m, 2), round(b, 2))
    r2 = r_squared(actual_values, predicted_values)

    return {
        'linear_regression_model': linear_regression_model,
        'predicted_values': predicted_values, 
        'rmse': rmse(actual_values, predicted_values),
        'R^2': r2
    }

def simple_linear_regression(dataset, test_set):
    """ Perform simple linear regression """
    
    predicted_values = []
    b, m = coefficients(dataset)
    
    for year in range(int(MAX_YEARS_YEARS_OF_EXPERIENCE)+1):
        yhat = (m * year) + b
        predicted_values.append(yhat)
    
    return (predicted_values, round(b, 4), round(m, 4))

def print_results(title, results):
    print('\n------------------------\n')
    
    print(title.upper())
    print('Linear Regression Model: {}'.format(results['linear_regression_model']))
    print('Predicted Values\nYear: Predicted Val')
    for idx, val in enumerate(results['predicted_values']):
        print('{}: {}'.format(idx, round(val, 2)))
    print('RMSE: {}'.format(round(results['rmse'], 4)))
    print('R^2: {}'.format(round(results['R^2'], 4)))


if __name__ == '__main__':
    csv_data = load_csv()
    overall_dataset = []
    corporate_dataset = []
    startup_dataset = []

    """
        Corresponding values of index from CSV 
        [1]: Field
        [2]: Current Years of Experience
        [3]: Salary
    """
    for row in csv_data:
        data = (row[1], float(row[2]), float(row[3].split('PHP ')[1]))
        
        # ADD ALL VALUES TO `OVERALL_DATASET`  
        overall_dataset.append(data)

        # ADD CORPORATE DATA TO `CORPORATE_DATASET
        if row[1] == 'Corporate':
            corporate_dataset.append(data)
        # ADD STARTUP DATA TO `STARTUP_DATASET
        elif row[1] == 'Startup':
            startup_dataset.append(data)

    assert len(csv_data) == len(overall_dataset)

    # PLOT ALL POINTS OF THE DATASET AND THEIR DESIGNATED COLOR BASED ON FIELD
    for data in overall_dataset:
        plt.scatter(data[1] , data[2], color=LEGEND_COLORS.get(data[0]))

    # LEGEND FOR EACH COLOR AND THEIR RESPECTIVE FIELD
    legend_academe_blue = mpatches.Patch(color='blue', label='Academe')
    legend_corporate_red = mpatches.Patch(color='red', label='Corporate')
    legend_consultancy_yellow = mpatches.Patch(color='yellow', label='Consultancy')
    legend_government_green = mpatches.Patch(color='green', label='Government')
    legend_startup_purple = mpatches.Patch(color='purple', label='Startup')

    # GRAPH STUFF
    plt.title('Filipino Salaries in Software Based on Years of Experience')
    plt.ylabel('Salary in PHP')
    plt.xlabel('Years of Experience')

    MAX_YEARS_YEARS_OF_EXPERIENCE = max(overall_dataset, key=itemgetter(1))[1]
    MAX_SALARY = max(overall_dataset, key=itemgetter(1))[2]

    axes = plt.gca()
    axes.set_xlim([0, MAX_YEARS_YEARS_OF_EXPERIENCE+1])
    axes.set_ylim([0, MAX_SALARY+40000])

    # GET RESULTS OF EACH PLOT
    overall_results = get_results(overall_dataset)
    print_results('overall results', overall_results)
    
    corporate_results = get_results(corporate_dataset)
    print_results('corporate results', corporate_results)
    
    startup_results = get_results(startup_dataset)
    print_results('startup results', startup_results)
    
    # LEGEND OF EACH REGRESSION MODEL
    legend_startup_cyan = mpatches.Patch(color='cyan', label='Overall Salary Regression Line \n{}'.format(overall_results.get('linear_regression_model')))
    legend_startup_black = mpatches.Patch(color='black', label='Corporate Regression Line\n{}'.format(corporate_results.get('linear_regression_model')))
    legend_startup_magenta = mpatches.Patch(color='magenta', label='Startup Regression Line\n{}'.format(startup_results.get('linear_regression_model')))

    plt.legend(
        handles=[legend_academe_blue, legend_corporate_red, legend_consultancy_yellow, legend_government_green, legend_startup_purple, legend_startup_cyan, legend_startup_black, legend_startup_magenta], 
        bbox_to_anchor=(1.05,1),
        borderaxespad=0,
        loc=2)

    # PLOT PREDICTED VALUES AS POINTS OF EACH LINEAR REGRESSION MODEL
    for year, value in enumerate(overall_results['predicted_values']):
        plt.scatter(year , value, color='cyan')

    for year, value in enumerate(corporate_results['predicted_values']):
        plt.scatter(year , value, color='black')

    for year, value in enumerate(startup_results['predicted_values']):
        plt.scatter(year , value, color='magenta')

    # GET PREDICTED VALUES OF  EACH REGRESSION MODEL TO MAKE A LINE
    years = [i for i in range(int(MAX_YEARS_YEARS_OF_EXPERIENCE)+1)]
    overall_predicted_values = [value for value in overall_results['predicted_values']]
    corporate_predicted_values = [value for value in corporate_results['predicted_values']]
    startup_predicted_values = [value for value in startup_results['predicted_values']]

    # DRAW LINE OF EACH REGRESSION MODEL
    plt.plot(years, overall_predicted_values,  color='cyan')
    plt.plot(years, corporate_predicted_values,  color='black')
    plt.plot(years, startup_predicted_values,  color='magenta')

    plt.show()
