from scipy.stats import chi2
import numpy as np

class chi_square:

    def __init__(self):
        self.name = "Chi-Square"
        self.plot_title = "Chi-squared Distribution ({} = 0)".format(u"\u03BC")
        self.k_values = [1, 2, 5, 7]
        self.x_range = np.linspace(0,15,1000)
        self.mu = 0
        self.k = self.k_values[0]
        self.parameters = {"mu" : self.mu, "k" : self.k}
        self.wiki_text = "In probability theory and statistics, the chi-squared distribution (also chi-square or χ²-distribution) with k degrees of freedom is the distribution of a sum of the squares of k independent standard normal random variables. It is a special case of the gamma distribution and is one of the most widely used probability distributions in inferential statistics, e.g., in hypothesis testing or in construction of confidence intervals. When it is being distinguished from the more general noncentral chi-squared distribution, this distribution is sometimes called the central chi-squared distribution.\n\nThe chi-squared distribution is used in the common chi-squared tests for goodness of fit of an observed distribution to a theoretical one, the independence of two criteria of classification of qualitative data, and in confidence interval estimation for a population standard deviation of a normal distribution from a sample standard deviation. Many other statistical tests also use this distribution, like Friedman's analysis of variance by ranks."

    def draw_demo(self, plotWidget):
        plotWidget.clear()
        plotWidget.plotItem.legend.items=[]
        plotWidget.setTitle(self.plot_title)

        for i,k in enumerate(self.k_values):
            dist = chi2(k, self.mu)

            plotWidget.plot(self.x_range, dist.pdf(self.x_range), fillLevel=0,
                fillBrush=(255,255,255,30), pen=(i,4),
                name="{sym} = {val}".format(sym='k',val=k))