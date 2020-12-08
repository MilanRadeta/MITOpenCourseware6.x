# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name:
# Collaborators (discussion):
# Time:

from matplotlib import pyplot as pl
import pylab
import re
import pathlib

root_folder = pathlib.Path(__file__).parent.absolute().__str__()

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""


class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """

    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)',
                            items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]


"""
End helper code
"""


def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    return [pylab.polyfit(x, y, deg) for deg in degs]


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = sum(y) / len(y)
    sum_diffs = sum((y - estimated) ** 2)
    sum_mean_diffs = sum((y - mean) ** 2)
    return 1 - sum_diffs / sum_mean_diffs


def plot_data_and_estimation(x, y, estimated, title, xlabel='Year', ylabel='Degrees Celsius'):
    pl.figure()
    pl.plot(x, y, 'bo', label='Raw Data')
    pl.plot(x, estimated, 'r-', label='Estimation')
    pl.legend()
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)
    pl.title(title)
    pl.show()


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        estimated = pylab.polyval(model, x)

        n = len(model) - 1
        r2 = r_squared(y, estimated)
        seos = se_over_slope(x, y, estimated, model) if n <= 1 else None

        title = 'n=%d' % n
        title += ', R^2=%.4f' % r2
        if seos is not None:
            title += ', SE/slope=%.4f' % seos

        plot_data_and_estimation(x, y, estimated, title)


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    avg_per_city = []
    for city in multi_cities:
        temps = calc_avg_city_annual_temps(climate, city, years)
        avg_per_city.append(temps)

    avg_per_city = pylab.array(avg_per_city)
    return sum(avg_per_city) / len(avg_per_city)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    result = []
    for i in range(len(y)):
        start = max(0, i - window_length + 1)
        end = i + 1
        sum_years = sum(y[start:end])
        n = min(i + 1, window_length)
        result.append(sum_years / n)

    return pylab.array(result)


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return (sum((y - estimated) ** 2) / len(y)) ** (1/2)


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """
    national_annual_temps = gen_cities_avg(climate, multi_cities, years)

    stds = []
    for i in range(len(years)):
        year = years[i]
        annual_temp = national_annual_temps[i]

        temps_per_cities = []
        for city in multi_cities:
            temps = climate.get_yearly_temp(city, year)
            temps_per_cities.append(temps)
        temps_per_cities = pylab.array(temps_per_cities)

        avg_yearly_temps = sum(temps_per_cities) / len(multi_cities)
        diffs = (avg_yearly_temps - annual_temp) ** 2
        std = (sum(diffs) / len(avg_yearly_temps)) ** (1/2)

        stds.append(std)
    return pylab.array(stds)


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        estimated = pylab.polyval(model, x)
        n = len(model) - 1
        rm_se = rmse(y, estimated)
        title = 'n=%d' % n
        title += ', RMSE=%.4f' % rm_se
        plot_data_and_estimation(x, y, estimated, title)


def calc_avg_city_annual_temps(climate, city, years):
    result = []
    for year in years:
        yearly_temp = climate.get_yearly_temp(city, year)
        if year % 4 == 0:
            annual_temp = sum(yearly_temp) / 366
        else:
            annual_temp = sum(yearly_temp) / 365
        result.append(annual_temp)
    return pylab.array(result)


def calc_daily_city_temps(climate, city, years, day=10, month=1):
    result = []

    for year in years:
        temps = climate.get_daily_temp(city, month, day, year)
        result.append(temps)

    return pylab.array(result)


if __name__ == '__main__':
    # Part A.4
    degs = [1]
    climate = Climate(root_folder + '/data.csv')

    years = pylab.array(TRAINING_INTERVAL)
    temps = calc_daily_city_temps(climate, 'NEW YORK', years)
    models = generate_models(years, temps, degs)
    evaluate_models_on_training(years, temps, models)

    temps = calc_avg_city_annual_temps(climate, 'NEW YORK', years)
    models = generate_models(years, temps, degs)
    evaluate_models_on_training(years, temps, models)

    # Part B
    temps = gen_cities_avg(climate, CITIES, years)
    models = generate_models(years, temps, degs)
    evaluate_models_on_training(years, temps, models)

    # Part C
    temps = moving_average(temps, 5)
    models = generate_models(years, temps, degs)
    evaluate_models_on_training(years, temps, models)

    # Part D.2
    temps = gen_cities_avg(climate, CITIES, years)
    temps = moving_average(temps, 5)
    degs = [1, 2, 20]
    models = generate_models(years, temps, degs)
    evaluate_models_on_training(years, temps, models)

    years = pylab.array(TESTING_INTERVAL)
    temps = gen_cities_avg(climate, CITIES, years)
    temps = moving_average(temps, 5)
    evaluate_models_on_testing(years, temps, models)

    # Part E
    degs = [1]
    years = pylab.array(TRAINING_INTERVAL)
    temps = gen_std_devs(climate, CITIES, years)
    temps = moving_average(temps, 5)
    models = generate_models(years, temps, degs)
    evaluate_models_on_training(years, temps, models)
