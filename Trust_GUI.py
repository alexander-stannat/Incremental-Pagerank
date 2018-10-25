import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QTime


class Window(object):
    """Class to implement a window with an icon"""

    def __init__(self, window_width, window_height, window_position_horizontal, window_position_vertical):
        """
        Initializes the class above...
        :param window_width:
        :param window_height:
        :param window_position_horizontal:
        :param window_position_vertical:
        """
        self.window_width = window_width
        self.window_height = window_height
        self.window_position_horizontal = window_position_horizontal
        self.window_position_vertical = window_position_vertical

    def place_window(self):
        """
        Places the window at a particular position on the screen
        :return:
        """
        app = QtWidgets.QApplication(sys.argv)
        widget = QtWidgets.QWidget()
        widget.setWindowTitle("Network Explorer")
        widget.resize(self.window_width, self.window_height)
        widget.move(self.window_position_horizontal, self.window_position_vertical)
        widget.setWindowIcon(QtGui.QIcon('Tribler Logo.png'))
        exit(app.exec_())
        return


    """def add_date_and_time(self):
        
        Adds date and time to the window
        :return:
        
        datetime = QDateTime.currentDateTime()
        date = QDate.currentDate()
        time = QTime.currentTime()
        return datetime.toString() + "\n" + date.toString() + "\n" + time.toString()

    def add_button(self, text, position):
        
        :param text:
        :param position:
        :return:
        
        app = QtWidgets.QApplication(sys.argv)
        button = QtGui.QPushButton('Button')
        #  button = button.setToolTip('This is a <b>QPushButton</b> widget')
        button.setFixedSize(400, 400)
        button.show()
        app.exec_()
        return
        """

