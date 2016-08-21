from scipy.stats import expon
import numpy as np
from .distributions import distribution, parameter

class exponential(distribution):
    
    def __init__(self): 
        distribution.__init__(self,name = "Exponential",
                        plot_title = "Exponential Distribution",
                        demo_params = {"lambda" : [0.5, 1, 1.5, 2.5]},
                        parameters = {"lambda" : parameter(0.5, 0.01, 5)},
                        wiki_text = "In probability theory and statistics, the exponential distribution (a.k.a. negative exponential distribution) is the probability distribution that describes the time between events in a Poisson process, i.e. a process in which events occur continuously and independently at a constant average rate. It is a particular case of the gamma distribution. It is the continuous analogue of the geometric distribution, and it has the key property of being memoryless. In addition to being used for the analysis of Poisson processes, it is found in various other contexts.\n\nThe exponential distribution is not the same as the class of exponential families of distributions, which is a large class of probability distributions that includes the exponential distribution as one of its members, but also includes the normal distribution, binomial distribution, gamma distribution, Poisson, and many others.",
                        x_range = np.linspace(1e-4, 10, 1000),
                        continuous = True)

    def get_distribution(self):
        return expon(scale = (1.0/self.parameters['lambda'].value))

    def cdf(self,x):
        return self.get_distribution().cdf(x = x)

    def sf(self,x):
        # Same as 1 - cdf but sometimes more accurate
        return self.get_distribution().sf(x = x)


