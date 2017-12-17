# Results and Conclusions

(https://github.com/gabrielchase/Salary-Survey-Simple-Linear-Regression/blob/master/linear_regression_results.png "Results and Conclusions")

### All Fields Statistics:
    y = 8,636.55x + 26,574.56
    RMSE = 36726.8227
    R^2 = 0.4762

### Corporate Field Statistics
    y = 10,177.65x + 23,568.20
    RMSE = 34435.2072
    R^2= 0.5567

### Startup Field Statistics:
    y = 9,393.30 + 30,464.30
    RMSE = 43677.2864
    R^2= .4514

### Table of Values
| Year | All Software Fields | Corporate Field  | Startup Field |
| ---- |:-------------------:| :---------------:| :-----------: |
|  0   | 26,574.56           | 23,586.2         | 30,464.3      |
|  1   | 35,211.11           | 33,763.85        | 39,857.62     |
|  2   | 43,847.66           | 43,941.5         | 49,250.93     |
|  3   | 52,484.21           | 54,119.15        | 58,644.24     |
|  4   | 61,120.77           | 64,296.8         | 68,037.56     |
|  5   | 69,757.32           | 74,474.45        | 77,430.87     |
|  6   | 78,393.87           | 84,652.1         | 86,824.18     |
|  7   | 87,030.42           | 94,829.75        | 96,217.5      |
|  8   | 95,666.97           | 105,007.39       | 105,610.81    |
|  9   | 104,303.52          | 115,185.04       | 115,004.13    |
|  10  | 112,940.08          | 125,362.69       | 124,397.44    |
|  11  | 121,576.63          | 135,540.34       | 133,790.75    |
|  12  | 130,213.18          | 145,717.99       | 143,184.07    |
|  13  | 138,849.73          | 155,895.64       | 152,577.38    |
|  14  | 147,486.28          | 166,073.29       | 161,970.69    |
|  15  | 156,122.84          | 176,250.94       | 171,364.01    |
|  16  | 164,759.39          | 186,428.59       | 180,757.32    |



  Looking at the corporate field model, its starting salary ranks 
lowest among all the models but at the same time, its growth rate ranks the highest. The model suggests that even though one starts at a lower point,their career growth (salary-wise) in the field is much higher and in time, will be more profitable against the startup field.      

  When looking at the startup field, both least-squares estimators in
the startup field are higher than its counterpart in the overall 
regression model; this can lead us to assume that when working in the startup field, we can expect to be earning more than the general, 
average employee working in technology industry. 

  Comparing the startup and corporate field’s regression models, we 
can see that the starting salary in the startup field is noticeably 
higher than the corporate field, however, its growth per year, as stated 
before, is slower. The difference between the two decreases as the years 
go by and with the use of basic algebra, we can calculate that the 
startup’s linear regression model will be higher than the corporate’s 
until 8.769284 years. 

  We conclude that by working in the corporate or startup field, one 
is expected to make a higher income compared to the overall salary of 
software; startup salaries are always higher than the overall while 
corporate salaries become higher than the overall after the third year 
and increase at a very high rate. 

  Despite this, there are flaws in our models. Looking at the results, 
each model’s R^2 value is nothing significant - they all lie near the
50th percentile. This leads us to conclude that our model is not very 
successful in determining variance, thus making our predicted values 
“approximately 50%” related to the actual values in our data set. The 
same can also be said for our corporate and startup salary model.

  Our model’s calculated RMSE are quite high which means there is a 
lot of deviation in salaries on a given year between the model and the 
actual salary. These high numbers are due to some data points who make a 
significantly bigger salary during the early years of their career (ie. 
Point (2, 120,000), this person has been working two years and has a 
salary of PHP 120k/mo.) or someone who makes a lower salary despite 
having more years of experience (ie. Point(10, 53,000)). This also 
supports our previous conclusion in that the model does not account for 
variance well.
