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
        - Discrete sliders need integer values for n    ---> DONE
        - Update other distributions... DRY
        - Add cdf functionality
        - Add reset button (easy, same as clicking on left button)
        - Stop right panel from stretching, prefer the plot to stretch --> DONE (finally...)
        - calculations not working for normal distribution
        - Add shading functionality for CDFs (should be easy...)
        
 """


distribs =  {1 : binomial.binomial(),
             2 : exponential.exponential(),
             3 : chisquare.chi_square(),
             4 : normal.normal(),
             5 : poisson.poisson_d()}
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
        self.active_distribution = None

        self.plotWidget = pg.PlotWidget(labels = {'left': "f(x)",
                                                  'bottom': "x"})
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

        # Combo box for continuous variables
        self.cdf_cont_combo_box = QtGui.QComboBox()
        self.cdf_cont_combo_box.addItem("P(X < x)")
        self.cdf_cont_combo_box.addItem("P(X > x)")
        self.cdf_cont_combo_box.addItem("2P(X > x)")
        # Combo box for discrete variables
        self.cdf_disc_combo_box = QtGui.QComboBox()
        self.cdf_disc_combo_box.addItem("P(X < x)")
        self.cdf_disc_combo_box.addItem("P(X > x)")
        self.cdf_disc_combo_box.addItem("P(X = x)")
        # "x = " box
        self.x_input = QtGui.QLineEdit() 
        self.x_input.setPlaceholderText("x = ")
        self.x_input.returnPressed.connect(self.calculate)
        # self.x_input.setGeometry(1,2,3,4)
        self.answer_box = QtGui.QLineEdit()
        self.answer_box.setReadOnly(True)
        self.title = QtGui.QLineEdit()
        self.title.setReadOnly(True)
        
        f = self.title.font()
        f.setPointSize(27)
        self.title.setFont(f)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
 


        """
        ██╗      █████╗ ██╗   ██╗ ██████╗ ██╗   ██╗████████╗
        ██║     ██╔══██╗╚██╗ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝
        ██║     ███████║ ╚████╔╝ ██║   ██║██║   ██║   ██║   
        ██║     ██╔══██║  ╚██╔╝  ██║   ██║██║   ██║   ██║   
        ███████╗██║  ██║   ██║   ╚██████╔╝╚██████╔╝   ██║   
        ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   
        """
        #Buttons left of plot
        buttons_left = QtGui.QVBoxLayout()
        for i, button in buttons.items():
            buttons_left.addWidget(button)

        #Parameters right of plot
        sliders_right = QtGui.QVBoxLayout()
        for i, ps in self.parameter_sliders.items():
            for j, slider in ps.items():
                # slider.setSizePolicy(sizePolicy)
                sliders_right.addWidget(slider)

        #Combo boxes (one always invisible)
        combo_boxes = QtGui.QVBoxLayout()
        combo_boxes.addWidget(self.cdf_cont_combo_box)
        combo_boxes.addWidget(self.cdf_disc_combo_box)
        #CDF calculator
        cdf_calc = QtGui.QHBoxLayout()
        cdf_calc.addLayout(combo_boxes)
        cdf_calc.addWidget(self.x_input)

        #Stack textbox and sliders
        right_stack = QtGui.QVBoxLayout()
        right_stack.addWidget(self.title)
        right_stack.addWidget(self.text_box)
        right_stack.addLayout(sliders_right)
        right_stack.addLayout(cdf_calc)
        right_stack.addWidget(self.answer_box)
    
        
        #Aligning left buttons, plot and parameters
        # outer_box = QtGui.QHBoxLayout()
        # outer_box.addLayout(buttons_left)
        # outer_box.addWidget(self.plotWidget)
        # outer_box.addLayout(right_stack)

        outer_box = QtGui.QGridLayout()
        outer_box.addLayout(buttons_left,0,0)
        outer_box.addWidget(self.plotWidget,0,1)
        outer_box.addLayout(right_stack,0,2)
        outer_box.setColumnStretch(1,3)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(outer_box)

        # set central widget
        self.setCentralWidget(self.centralWidget)

        # set up beta distribution by default
        buttons[1].click()

        self.show()

    """
    ██████╗ ██╗   ██╗████████╗████████╗ ██████╗ ███╗   ██╗                    
    ██╔══██╗██║   ██║╚══██╔══╝╚══██╔══╝██╔═══██╗████╗  ██║                    
    ██████╔╝██║   ██║   ██║      ██║   ██║   ██║██╔██╗ ██║                    
    ██╔══██╗██║   ██║   ██║      ██║   ██║   ██║██║╚██╗██║                    
    ██████╔╝╚██████╔╝   ██║      ██║   ╚██████╔╝██║ ╚████║                    
    ╚═════╝  ╚═════╝    ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═══╝                    
                                                                              
    ███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
    ██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
    █████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
    ██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
    ██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    """
    def calculate(self):

        if self.active_distribution.continuous:
            question = self.cdf_cont_combo_box.currentText()
        else:
            question = self.cdf_disc_combo_box.currentText()
        
        try:
            x = float(self.x_input.text())
        except Exception:
            return None

        if '<' in question:
            answer = self.active_distribution.sf(x)
        elif '>' in question:
            answer = (2 - ('2' not in question)) * self.active_distribution.cdf(x) # Ha! 
        elif '=' in question:
            answer = self.active_distribution.pmf(x)
        else:
            raise ValueError('Combo box did something unexpected')

        self.answer_box.setText(str(answer))

    """
    ███████╗ █████╗  ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗               
    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝               
    █████╗  ███████║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝                
    ██╔══╝  ██╔══██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝                 
    ██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║                  
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝                  
                                                                              
    ███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
    ██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
    █████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
    ██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
    ██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    """
    def make_plot_changers(self,id):
        def change_plot():
            self.x_input.clear()
            self.answer_box.clear()
            # Show only relevant sliders
            for i, ps in self.parameter_sliders.items():
                for j, slider in ps.items():
                    if i == id:
                        slider.show()
                    else:
                        slider.hide()
            
            self.active_distribution = distribs[id]
            # Get the right combo box
            if self.active_distribution.continuous:
                self.cdf_disc_combo_box.hide()
                self.cdf_cont_combo_box.show()
            else:
                self.cdf_cont_combo_box.hide()
                self.cdf_disc_combo_box.show()

            # Plot the distribution and update wiki text
            self.active_distribution.draw_demo(plotWidget=self.plotWidget,params=self.active_distribution.demo_params)
            self.title.setText(self.active_distribution.name)
            self.text_box.setText(self.active_distribution.wiki_text)
            QtGui.QApplication.processEvents() # Needed on mac for some reason
        return change_plot

    def make_parameter_changers(self, id, parameter):
        def change_parameter():
            # Update value
            slider_value = self.parameter_sliders[id][parameter].slider.value()
            self.active_distribution = distribs[id]
            
            # Slider scale is 0-100, so have to linearly transform it to match the parameter
            slider_min = 0
            slider_max = 100
            param_max = self.active_distribution.parameters[parameter].maximum
            param_min = self.active_distribution.parameters[parameter].minimum
            old_range = (slider_value - slider_min)
            new_range = (param_max - param_min)
            value = ((old_range * new_range) / (slider_max - slider_min)) + param_min
            if not self.active_distribution.parameters[parameter].continuous:
                self.active_distribution.parameters[parameter].value = np.round(value)
            else:    
                self.active_distribution.parameters[parameter].value = value
            
            # Update plot
            self.active_distribution.draw(self.plotWidget)
            
        return change_parameter



"""
 ██████╗██╗   ██╗███████╗████████╗ ██████╗ ███╗   ███╗ 
██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔═══██╗████╗ ████║ 
██║     ██║   ██║███████╗   ██║   ██║   ██║██╔████╔██║ 
██║     ██║   ██║╚════██║   ██║   ██║   ██║██║╚██╔╝██║ 
╚██████╗╚██████╔╝███████║   ██║   ╚██████╔╝██║ ╚═╝ ██║ 
 ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝ 
                                                       
██╗    ██╗██╗██████╗  ██████╗ ███████╗████████╗███████╗
██║    ██║██║██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝██╔════╝
██║ █╗ ██║██║██║  ██║██║  ███╗█████╗     ██║   ███████╗
██║███╗██║██║██║  ██║██║   ██║██╔══╝     ██║   ╚════██║
╚███╔███╔╝██║██████╔╝╚██████╔╝███████╗   ██║   ███████║
 ╚══╝╚══╝ ╚═╝╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝
"""
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



