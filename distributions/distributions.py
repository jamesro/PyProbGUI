import numpy as np
import pyqtgraph as pg


class distribution:

    def __init__(self,name,plot_title,demo_params,parameters,wiki_text,x_range,continuous=True):
        self.name = name
        self.plot_title = plot_title
        self.demo_params = demo_params
        self.parameters = parameters
        self.wiki_text = wiki_text
        self.x_range = x_range
        self.continuous = continuous

    def clear_plot(self, plotWidget):
        plotWidget.clear()
        plotWidget.plotItem.legend.items=[]
        plotWidget.setTitle(self.plot_title)
    
    def draw_demo(self,plotWidget,params):
        self.clear_plot(plotWidget)
          
        for param, values in params.items():
            n_plots = len(values) # Dangerous, always require the same amount
            for i in range(n_plots):
                name = "{sym} = {val}  ".format(sym=param,val=values[i])
        
        
                if self.continuous:
            
                    self.parameters[param].value = values[i]
                    self.update_xrange()
                    dist = self.get_distribution()
                    plotWidget.plot(self.x_range, dist.pdf(self.x_range), fillLevel=0, 
                                    fillBrush=(255,255,255,30), pen=(i,n_plots), 
                                    name=name)

        
                else:
                    
                    self.parameters[param].value = values[i]
                    self.update_xrange()
                    dist = self.get_distribution()
                    plotWidget.plot(self.x_range, dist.pmf(self.x_range), 
                                    pen=(i,n_plots), fillLevel=0,
                                    fillBrush=(255,255,255,5),
                                    name=name)
                    
                    bg = pg.BarGraphItem(x=self.x_range, height=dist.pmf(self.x_range),
                                        width=0.05, pen=(i,n_plots), fillLevel = 30)

                    plotWidget.addItem(bg)

    def draw(self,plotWidget):
        self.clear_plot(plotWidget)
        name = ""
        for param_name, obj in self.parameters.items():
            name += "{sym} = {val}  ".format(sym=param_name,val=obj.value)

        if self.continuous:
            self.update_xrange()
            dist = self.get_distribution()
            plotWidget.plot(self.x_range, dist.pdf(self.x_range), fillLevel=0, 
                             fillBrush=(255,255,255,30), 
                             name=name)
        else:
            self.update_xrange()
            dist = self.get_distribution()
            plotWidget.plot(self.x_range, dist.pmf(self.x_range), fillLevel=0,
                            fillBrush=(255,255,255,5), name=".")
                        
            bg = pg.BarGraphItem(x=self.x_range, height=dist.pmf(self.x_range),
                                width=0.05, fillLevel = 30)

            plotWidget.addItem(bg)


    def get_distribution(self):
        pass

    def update_xrange(self):
        pass

class parameter:

    def __init__(self, init_value, minimum, maximum):
        self.value = init_value
        self.minimum = minimum
        self.maximum = maximum



