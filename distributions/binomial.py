from scipy.stats import binom
import numpy as np
import pyqtgraph as pg
from .distributions import distribution, parameter


class binomial(distribution):
    n = 25
    def __init__(self): 
        distribution.__init__(self,name = "Binomial",
                        plot_title = "Binomial Distribution",
                        demo_params = {"p" : [0.1,0.25,0.5]},
                        parameters = {"n" : parameter(n,1,100),
                                      "p" : parameter(0.1,0,1)},
                        wiki_text = "In probability theory and statistics, the binomial distribution with parameters n and p is the discrete probability distribution of the number of successes in a sequence of n independent yes/no experiments, each of which yields success with probability p. A success/failure experiment is also called a Bernoulli experiment or Bernoulli trial; when n = 1, the binomial distribution is a Bernoulli distribution. The binomial distribution is the basis for the popular binomial test of statistical significance.\n\nThe binomial distribution is frequently used to model the number of successes in a sample of size n drawn with replacement from a population of size N. If the sampling is carried out without replacement, the draws are not independent and so the resulting distribution is a hypergeometric distribution, not a binomial one. However, for N much larger than n, the binomial distribution is a good approximation, and widely used.",
                        x_range = np.arange(0,n),
                        continuous = False)

    def get_distribution(self):
        return binom(self.parameters['n'].value,self.parameters['p'].value)

    def update_xrange(self):
        self.x_range = np.arange(0, self.parameters['n'].value)


