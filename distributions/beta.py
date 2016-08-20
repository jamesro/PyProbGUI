from scipy.stats import beta
import numpy as np


class dBeta:

    def __init__(self):
        self.name = "Beta"
        self.plot_title = "Beta Distribution "
        self.alpha_values = [0.5, 1, 2, 2, 5]
        self.beta_values = [0.5, 3, 2, 5, 1]
        self.x_range = np.linspace(0,1,1000)
        self.alpha = self.alpha_values[0]
        self.beta = self.beta_values[0] 
        self.parameters = {"alpha" : self.alpha, "beta" : self.beta}
        self.wiki_text =  "In probability theory and statistics, the beta distribution is a family of continuous probability distributions defined on the interval [0, 1] parametrized by two positive shape parameters, denoted by α and β, that appear as exponents of the random variable and control the shape of the distribution.\n\nThe beta distribution has been applied to model the behavior of random variables limited to intervals of finite length in a wide variety of disciplines. For example, it has been used as a statistical description of allele frequencies in population genetics; time allocation in project management / control systems; sunshine data; variability of soil properties; proportions of the minerals in rocks in stratigraphy; and heterogeneity in the probability of HIV transmission."


    def draw_demo(self, plotWidget):
        plotWidget.clear()
        plotWidget.plotItem.legend.items=[]
        plotWidget.setTitle(self.plot_title)

        for i, (a, b) in enumerate(zip(self.alpha_values, self.beta_values)):
            dist = beta(a,b)

            plotWidget.plot(self.x_range, dist.pdf(self.x_range), fillLevel=0, fillBrush=(255,255,255,30),
                pen=(i,5), name="{sym1} = {val1}, {sym2} = {val2}".format(sym1=u'\u03B1',
                    val1=a,sym2=u'\u03B2',val2=b))




       