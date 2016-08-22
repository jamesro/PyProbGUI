from scipy.stats import chi2
import numpy as np
from .distributions import distribution, parameter

class chi_square(distribution):
    
    def __init__(self): 
        distribution.__init__(self, name = "Chi-Square",
                        plot_title = "Chi-Squared Distribution",
                        demo_params = {"k" : [1, 2, 5, 7]},
                        parameters = {"k" : parameter(1, 1, 10, continuous=False)},
                        wiki_text = "In probability theory and statistics, the chi-squared distribution (also chi-square or χ²-distribution) with k degrees of freedom is the distribution of a sum of the squares of k independent standard normal random variables. It is a special case of the gamma distribution and is one of the most widely used probability distributions in inferential statistics, e.g., in hypothesis testing or in construction of confidence intervals. When it is being distinguished from the more general noncentral chi-squared distribution, this distribution is sometimes called the central chi-squared distribution.\n\nThe chi-squared distribution is used in the common chi-squared tests for goodness of fit of an observed distribution to a theoretical one, the independence of two criteria of classification of qualitative data, and in confidence interval estimation for a population standard deviation of a normal distribution from a sample standard deviation. Many other statistical tests also use this distribution, like Friedman's analysis of variance by ranks.",
                        x_range = np.linspace(0,15,1000),
                        continuous = True)

    def get_distribution(self):
        return chi2(self.parameters['k'].value)