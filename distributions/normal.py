from scipy.stats import norm
import numpy as np


class normal:

    def __init__(self):
        self.name = "Normal"
        self.plot_title = "Normal Distribution ({} = 0)".format(u'\u03BC')
        self.sigma_values = [0.5, 1, 2, 5]
        self.x_range = np.linspace(-6,6,1000)
        self.mu = 0
        self.sigma = 1
        self.parameters = {"mu" : self.mu, "sigma" : self.sigma}
        self.wiki_text = """In probability theory, the normal (or Gaussian) distribution is a very common continuous probability distribution. Normal distributions are important in statistics and are often used in the natural and social sciences to represent real-valued random variables whose distributions are not known.\n\nThe normal distribution is useful because of the central limit theorem. In its most general form, under some conditions (which include finite variance), it states that averages of random variables independently drawn from independent distributions converge in distribution to the normal, that is, become normally distributed when the number of random variables is sufficiently large."""

    def draw_demo(self, plotWidget):
        plotWidget.clear()
        plotWidget.plotItem.legend.items=[]
        plotWidget.setTitle(self.plot_title)

        for i, sigma in enumerate(self.sigma_values):
            dist = norm(self.mu, sigma)

            plotWidget.plot(self.x_range, dist.pdf(self.x_range), 
                fillLevel=0, fillBrush=(255,255,255,30), pen=(i,4), 
                name="{sym} = {val}".format(sym=u'\u03C3',val=sigma))