from scipy.stats import poisson
import numpy as np
import pyqtgraph as pg

class poisson_d:

    def __init__(self):
        self.name = "Poisson"
        self.plot_title = "Poisson Distribution"
        self.lambda_values = [1,2,5]
        self.x_range = np.arange(0,10)
        self.parameters = {"lambda" : {'value' : self.lambda_values[0], 'min' : 0.1, 'max' : 5}}
        self.wiki_text = "In probability theory and statistics, the Poisson distribution, named after French mathematician Siméon Denis Poisson, is a discrete probability distribution that expresses the probability of a given number of events occurring in a fixed interval of time and/or space if these events occur with a known average rate and independently of the time since the last event. The Poisson distribution can also be used for the number of events in other specified intervals such as distance, area or volume."

    def draw_demo(self, plotWidget):
        plotWidget.clear()
        plotWidget.plotItem.legend.items=[]
        plotWidget.setTitle(self.plot_title)

        for i, lm in enumerate(self.lambda_values):
            lm = self.parameters['lambda']['value']
            dist = poisson(lm)
            
            plotWidget.plot(self.x_range, dist.pmf(self.x_range), pen=(i,4), 
                fillLevel=0, fillBrush=(255,255,255,5),
                name="{sym} = {val}".format(sym=u"\u03BB",val=lm))
            
            bg = pg.BarGraphItem(x=self.x_range, height=dist.pmf(self.x_range),
                width=0.05, pen=(i,4), fillLevel = 30)

            plotWidget.addItem(bg)

    def draw(self, plotWidget):
        plotWidget.clear()
        plotWidget.plotItem.legend.items=[]
        lm = self.parameters['lambda']['value']
        dist = poisson(lm)
            
        plotWidget.plot(self.x_range, dist.pmf(self.x_range), 
            fillLevel=0, fillBrush=(255,255,255,5),
            name="{sym} = {val}".format(sym=u"\u03BB",val=lm))
        
        bg = pg.BarGraphItem(x=self.x_range, height=dist.pmf(self.x_range),
            width=0.05, fillLevel = 30)

        plotWidget.addItem(bg)