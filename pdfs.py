import sys
from PyQt4 import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import qdarkstyle
from distributions import normal, chisquare, poisson, exponential, binomial, beta
"""
 TO DO: 
        - Demo plots with multiple variables (Beta):
                - zip through values of demo_parameters dict
        - Update other distributions... DRY
        - Add cdf functionality
        - Add reset button (easy, same as clicking on left button)
        
 """


distribs =  {1 : binomial.binomial(),
             2 : exponential.exponential()}
            # 3 : poisson.poisson_d()}
# distribs = {1 : normal.normal(),
#             2 : chisquare.chi_square(),
#             3 : poisson.poisson_d(),
#             4 : exponential.exponential(),
#             5 : binomial.binomial(),
#             6 : beta.dBeta(),
#             7 : normal.normal(),
#             8 : chisquare.chi_square(),
#             9 : normal.normal(),
#             10: chisquare.chi_square(),
#             11: normal.normal(),
#             12: chisquare.chi_square(),
#             13: normal.normal(),
#             14: chisquare.chi_square(),
#             15: normal.normal()
#                 }

greeks = {  'alpha' : u'\u03B1',
            'beta' : u'\u03B2',
            'mu' : u'\u03BC',
            'nu' : u'\u03BD',
            'sigma' : u'\u03C3',
            'lambda' : u'\u03BB',
            'n' : 'n',
            'p' : 'p',
            'k' : 'k'}





class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__() 

        self.setGeometry(50,50,1000,600)
        self.setWindowTitle("Probability Density Functions")

        # This is an assigned object because we're going to modify it
        mainMenu = self.menuBar()

        # Calls the status bar (bottom bar)
        self.statusBar()

        self.home()
    

    def home(self):
        self.plotWidget = pg.PlotWidget(labels = {'left': "f(x)", 'bottom': "x"})
        self.plotWidget.addLegend(offset=(-10,1))
       
        # Left side (distributions)
        buttons = {}
        for i, distrib in distribs.items():
            button = QtGui.QPushButton(distrib.name, self)
            button.clicked.connect(self.make_plot_changers(i))
            button.resize(button.minimumSizeHint())
            buttons[i] = button



        # Right side tweek the parameters
        self.parameter_sliders = {}
        for i, distrib in distribs.items():
            sliders = {}
            for param, properties in distrib.parameters.items():
                slwl = SliderWithLabel()
                slwl.label.setText(greeks[param])
                slwl.slider.valueChanged.connect(self.make_parameter_changers(i,param))
                sliders[param] = slwl
            self.parameter_sliders[i] = sliders
        
        self.text_box = QtGui.QTextEdit()
        self.text_box.setReadOnly(True)


        # ---------------------------------------------------------
        #| Layout                                                  |
        # ---------------------------------------------------------

        #Buttons left of plot
        buttons_left = QtGui.QVBoxLayout()
        for i, button in buttons.items():
            buttons_left.addWidget(button)

        #Parameters right of plot
        sliders_right = QtGui.QVBoxLayout()
        sliders_right.addStretch()
        for i, ps in self.parameter_sliders.items():
            for j, slider in ps.items():
                sliders_right.addWidget(slider)

        #Stack textbox and sliders
        right_stack = QtGui.QVBoxLayout()
        right_stack.addStretch()
        
        right_stack.addWidget(self.text_box)
        right_stack.addLayout(sliders_right)

        #Aligning left buttons, plot and parameters
        outer_box = QtGui.QHBoxLayout()
        outer_box.addLayout(buttons_left)
        outer_box.addWidget(self.plotWidget)
        outer_box.addLayout(right_stack)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(outer_box)

        # set central widget
        self.setCentralWidget(self.centralWidget)

        # set up beta distribution by default
        buttons[1].click()

        self.show()

    # ---------------------------------------------------------
    #| Factory Functions                                       |
    # ---------------------------------------------------------
    def make_plot_changers(self,id):
        def change_plot():
            # Show only relevant sliders
            for i, ps in self.parameter_sliders.items():
                for j, slider in ps.items():
                    if i == id:
                        slider.show()
                    else:
                        slider.hide()
            
            dist_obj = distribs[id]
            # Plot the distribution
            dist_obj.draw_demo(plotWidget=self.plotWidget,params=dist_obj.demo_params)
            
            QtGui.QApplication.processEvents() # Needed on mac for some reason
            
            self.text_box.setText(dist_obj.wiki_text)
        
        return change_plot

    def make_parameter_changers(self, id, parameter):
        def change_parameter():
            # Update value
            slider_value = self.parameter_sliders[id][parameter].slider.value()
            dist_obj = distribs[id]
            
            # Slider scale is 0-100, so have to linearly transform it to match the parameter
            slider_min = 0
            slider_max = 100
            param_max = dist_obj.parameters[parameter].maximum
            param_min = dist_obj.parameters[parameter].minimum
            old_range = (slider_value - slider_min)
            new_range = (param_max - param_min)
            value = ((old_range * new_range) / (slider_max - slider_min)) + param_min
            dist_obj.parameters[parameter].value = value
            
            # Update plot
            dist_obj.draw(self.plotWidget)
            
        return change_parameter

            



class SliderWithLabel(QtGui.QWidget): 
    def __init__(self, *var, **kw): 
        QtGui.QWidget.__init__(self, *var, **kw) 
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal) 
        self.label = QtGui.QLabel(self) 
        layout = QtGui.QHBoxLayout() 
        layout.setMargin(0) 
        layout.addWidget(self.label) 
        layout.addWidget(self.slider) 
        self.setLayout(layout) 

       




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    GUI = Window()
    sys.exit(app.exec_())



