import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QTabWidget, QVBoxLayout,
                             QWidget, QMainWindow)

from tabs.daily.tab_daily import TabDaily
from tabs.single.tab_single import TabSingle


class NLDC_Main(QMainWindow):
    def __init__(self, title):
        super(NLDC_Main, self).__init__()
        self.title = title
        self.setupUI()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

    def setupUI(self):
        self.setGeometry(0, 0, 1366, 768)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
        self.wnd2Center()
        self.initTabs()

        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(self.tabs)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def wnd2Center(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    # def createActions(self):
    #     self.actNew = QAction(None, '&New', self,
    #                           statusTip='Create a New File',
    #                           triggered=self.newFile)
    #
    # def createMenus(self):
    #     self.mainMenu = self.menuBar().addMenu('&File')

    def initTabs(self):
        self.tabs = QTabWidget()
        self.tabList = []
        self.tabTitle = ['daily', 'single', 'monthly', 'yearly']

        self.tabList.append(TabDaily())
        self.tabList.append(TabSingle())
        self.tabList.append(QWidget())
        self.tabList.append(QWidget())

        for i in range(len(self.tabList)):
            self.tabs.addTab(self.tabList[i], self.tabTitle[i])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NLDC_Main('Natural Light Data Center')
    window.show()
    app.exec_()
