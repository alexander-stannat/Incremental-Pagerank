import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QTime


class Window(QMainWindow):
    """Class to implement a window with an icon"""

    def __init__(self, window_width, window_height, window_position_horizontal, window_position_vertical):
        """
        Initializes the class above...
        :param window_width:
        :param window_height:
        :param window_position_horizontal:
        :param window_position_vertical:
        """
        super(Window, self).__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.window_position_horizontal = window_position_horizontal
        self.window_position_vertical = window_position_vertical

    def place_window(self):
        """
        Places the window at a particular position on the screen
        :return:
        """
        self.setWindowTitle("Network Explorer")
        self.resize(self.window_width, self.window_height)
        self.move(self.window_position_horizontal, self.window_position_vertical)
        self.setWindowIcon(QtGui.QIcon('Tribler Logo.png'))

        btn = QPushButton('Cancel', self)
        btn2 = QPushButton('Start', self)

        btn.move(150, 350)
        btn2.move(400, 350)

        # QMessageBox.question(self, 'Message', "Do you want to continue?", QMessageBox.Yes, QMessageBox.No)

        btn.setToolTip("This button takes you home")
        btn2.setToolTip("This button does not...")

        btn.resize(btn.sizeHint())
        btn2.resize(btn2.sizeHint())

        btn.clicked.connect(QApplication.instance().quit)
        btn2.clicked.connect(self.tell_off)

        self.show()
        return

    def tell_off(self):
        self.setGeometry(400, 250, 500, 300)
        self.setWindowTitle("Fuck Off!!!")
        self.statusBar().showMessage("F O")
        self.show()
        return


class StatusBar(QMainWindow):
    """ Class to implement a Status Bar"""

    def __init__(self):
        """
        Initialises the class
        """
        super(StatusBar, self).__init__()

    def lala(self):
        self.resize(1000, 500)
        return

    def place_window(self):
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+W')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        changeSizeAct = QAction(QIcon('lala.png'), '&Change Size', self)
        changeSizeAct.setShortcut('Alt+W')
        changeSizeAct.setStatusTip('Change the size of the window')
        changeSizeAct.triggered.connect(self.lala)

        self.addAction(exitAct)
        self.addAction(changeSizeAct)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(changeSizeAct)

        new_menu = QMenu('smaller submenu', self)
        new_menu_action = QAction('acction', self)
        new_menu.addAction(new_menu_action)

        fileMenu.addMenu(new_menu)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Interesting menu')
        self.show()
        self.statusBar().showMessage("In the above example, we create a menubar with one menu. This menu will "
                                     "contain one action which will terminate the application if selected. A "
                                     "statusbar is created as well. The action is accessible with the Ctrl+Q shortcut.")

class Clickmenu(QMainWindow):
    """
    lalala
    """
    NumButtons = ['Show Neighbourhood', 'Most Trusted Peer', 'MostLikelyPath']

    def __init__(self):
        super(Clickmenu, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Context menu')
        lbl1 = QLabel('Label', self)
        self.createVerticalGroupBox()
        self.show()

    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()
        layout = QVBoxLayout()
        for i in self.NumButtons:
            button = QPushButton(i)
            button.setObjectName(i)
        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalGroupBox.setLayout(layout)
        # button.clicked.connect(self.submitCommand)
