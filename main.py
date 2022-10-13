# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from genData_sample import *
import pandas as pd
import numpy as np
import threading
import time
os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.running = False
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Agcam - fast camera"
        description = "Agcam APP - super fast measurement available camera."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_measurement.clicked.connect(self.buttonClick)
        widgets.btn_analysis.clicked.connect(self.buttonClick)
        widgets.btn_open.clicked.connect(self.buttonClick)
        widgets.btn_start.clicked.connect(self.buttonClick)
        widgets.btn_stop.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_measurement":
            widgets.stackedWidget.setCurrentWidget(widgets.Measurement)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_analysis":
            widgets.stackedWidget.setCurrentWidget(widgets.Analysis)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_start":
            if self.running == False:
                self.XRange = 110
                widgets.cam_GraphWidget_1.clear()
                widgets.cam_GraphWidget_1.setXRange(0, self.XRange)
                widgets.cam_GraphWidget_2.clear()
                widgets.cam_GraphWidget_2.setXRange(0, self.XRange)
                widgets.cam_GraphWidget_3.clear()
                widgets.cam_GraphWidget_3.setXRange(0, self.XRange)
                self.running = True
                self.th_measure = threading.Thread(target=self.genSample_Data)
                self.th_measure.start()
                self.mytimer = QTimer()
                self.mytimer.start(1 / 24 * 1000)  # 1초마다 차트 갱신 위함...
                self.mytimer.timeout.connect(self.plot_data)
            else:
                self.running = False
                self.mytimer.stop()
                self.th_measure.join()

            """
            
            ros를 통해서 csv를 가져오는 펑션
            
            그래프 출력 펑션
            
        
            """

        if btnName == "btn_stop":
            self.running = False




        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    '''
    gen data
    '''
    def genSample_Data(self):
        i=0
        self.time = []
        self.x = []
        self.y = []
        self.z = []
        while self.running:
            self.time.append(i)

            self.x.append(random.uniform(-5, 5))
            self.y.append(random.uniform(-5, 5))
            self.z.append(random.uniform(-5, 5))

            i = i+1
            time.sleep(0.01)
    '''
    plot data def
    '''

    def plot_data(self):
        self.range_time = 110
        widgets.cam_GraphWidget_1.clear()
        widgets.cam_GraphWidget_1.addLegend()
        self.pl_x = widgets.cam_GraphWidget_1.plot(pen='r',name='Camera X data')
        self.pl_y = widgets.cam_GraphWidget_1.plot(pen='y',name='Camera Y data')
        self.pl_z = widgets.cam_GraphWidget_1.plot(pen='b',name='Camera Z data')


        if len(self.time) < self.range_time*60:
            self.pl_x.setData(self.time, self.x)
            self.pl_y.setData(self.time, self.y)
            self.pl_z.setData(self.time, self.z)


        else:
            self.pl_x.setData(self.time[-self.XRange*60:], self.x[-self.XRange*60:])
            self.pl_y.setData(self.time[-self.XRange*60:], self.y[-self.XRange*60:])
            self.pl_z.setData(self.time[-self.XRange*60:], self.z[-self.XRange*60:])


            widgets.cam_GraphWidget_1.setYRange(
                min(self.x[-self.XRange*60:]) * 1.2, max(self.x[-self.XRange*60:]) * 1.2)



        if len(self.time) > 1:
            
            if self.time[-1] > self.range_time:
                k = self.time[-1] - self.range_time
                widgets.cam_GraphWidget_1.setXRange(k, k + self.range_time)


        widgets.cam_GraphWidget_1.show()    # RESIZE EVENTS


    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
