from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QCheckBox, QTableWidget,
                             QAbstractItemView, QListWidget, QListWidgetItem,
                             QHeaderView, QTableWidgetItem)
from matplotlib import colors as mcolors

from pysparkmgr import PySparkManager


class Panel_Datelist(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        self.listwdg = QListWidget()

        # init layout
        self.layout = QVBoxLayout()
        # self.listwdg.setFixedWidth(90)
        self.layout.addWidget(self.listwdg)
        self.setLayout(self.layout)

        # get date list from dataframe using pyspark
        self.datelist = self.getDatelist()
        self.makeList(self.datelist)

    def getDatelist(self):  # 날짜만 가져옴
        pysparkmgr = PySparkManager()
        datelist = pysparkmgr.getDF('nt_srs') \
            .select('date') \
            .sort('date') \
            .distinct() \
            .toPandas().values.tolist()
        return list(map(lambda date: date[0], datelist))

    def makeList(self, datelist):
        for dt in datelist:
            item = QListWidgetItem()
            item.setText(dt)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.listwdg.addItem(item)

    def getCheckedDates(self):
        ret = []
        for i in range(self.listwdg.count()):
            if self.listwdg.item(i).checkState() == Qt.Checked:
                ret.append(self.listwdg.item(i).text())
        return ret


class Panel_SelectedDataTable(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)

        self.leftAxisType = ['illum', 'cct', 'swr']
        self.rightAxisType = ['illum', 'cct', 'swr']

        self.cbxLeft = QComboBox()
        self.cbxRight = QComboBox()
        self.chkEnableRightAxis = QCheckBox('오른쪽 축')
        self.layout = QGridLayout()
        self.tblwdgLeft = QTableWidget(0, 4)
        self.tblwdgRight = QTableWidget(0, 4)
        self.createSelectedDataTable()

        self.chkEnableRightAxis.setChecked(False)
        self.cbxRight.setEnabled(False)

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        self.chkEnableRightAxis.stateChanged.connect(self.enableRightAxis)

    def setItemsInCbx(self):
        self.cbxLeft.addItems(self.leftAxisType)
        self.cbxRight.addItems(self.rightAxisType)

    def createSelectedDataTable(self):
        self.tblwdgLeft.setFixedWidth(130)
        self.tblwdgLeft.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblwdgLeft.setHorizontalHeaderLabels(("date", "color", "marker", "dash"))
        self.tblwdgLeft.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tblwdgLeft.verticalHeader().hide()
        self.tblwdgLeft.setShowGrid(False)
        # self.tblwdgLeft.cellActivated.connect()

        self.tblwdgRight.setFixedWidth(130)
        self.tblwdgRight.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblwdgRight.setHorizontalHeaderLabels(("date", "color", "marker", "dash"))
        self.tblwdgRight.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tblwdgRight.verticalHeader().hide()
        self.tblwdgRight.setShowGrid(False)
        # self.tblwdgRight.cellActivated.connect()

    def setComponentsWithLayout(self):
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 2)
        self.layout.setColumnStretch(3, 2)

        self.layout.addWidget(QLabel('왼쪽 축'), 0, 0)
        self.layout.addWidget(self.chkEnableRightAxis, 0, 1)
        self.layout.addWidget(self.cbxLeft, 1, 0)
        self.layout.addWidget(self.cbxRight, 1, 1)
        self.layout.addWidget(self.tblwdgLeft, 2, 0)
        self.layout.addWidget(self.tblwdgRight, 2, 1)

        if not self.chkEnableRightAxis.isChecked():
            self.tblwdgRight.setEnabled(False)

        self.setLayout(self.layout)

    def enableRightAxis(self):
        if self.chkEnableRightAxis.isChecked():
            self.cbxRight.setEnabled(True)
            self.tblwdgRight.setEnabled(True)
        else:
            self.cbxRight.setEnabled(False)
            self.tblwdgRight.setEnabled(False)

    def addDataFromSelectedDates(self, datelist, right_enable=False):
        for day in datelist:
            selectedDateItem = QTableWidgetItem(day)
            selectedDateItem.setFlags(Qt.ItemIsUserCheckable)
            colorItem = QTableWidgetItem()

            row = self.tblwdgLeft.rowCount()
            self.tblwdgLeft.insertRow(row)
            self.tblwdgLeft.setItem(row, 0, day)
            self.tblwdgLeft.setItem(row, 1, day)
            self.tblwdgLeft.setItem(row, 2, day)
            self.tblwdgLeft.setItem(row, 3, day)

            if right_enable:
                pass

            row += 1

    def getSelectedItem(self):
        if self.chkEnableRightAxis.isChecked():
            return [str(self.cbxLeft.currentText()), str(self.cbxRight.currentText())]
        else:
            return [str(self.cbxLeft.currentText())]


class Panel_Visual(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)

        self.colorlist = self.getNamedColorList()
        self.markerlist = ['.', ',', 'o', 'v', '<', '>', '^',
                           '1', '2', '3', '4', 's', 'p', '*',
                           'h', 'H', '+', 'x', 'D', 'd']
        self.linelist = ['-', '--', '-.', ':']

        self.cbxColor = QComboBox()
        self.cbxMarkerType = QComboBox()
        self.cbxLineType = QComboBox()

        self.layout = QGridLayout()

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        # disable for testmode
        self.cbxColor.setEnabled(False)
        self.cbxMarkerType.setEnabled(False)
        self.cbxLineType.setEnabled(False)

    def getNamedColorList(self):
        # matplotlib color list : named_color.py
        # https://matplotlib.org/examples/color/named_colors.html
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                        for name, color in colors.items())
        sorted_names = [name for hsv, name in by_hsv]
        return sorted_names

    def setItemsInCbx(self):
        self.cbxColor.addItems(self.colorlist)
        self.cbxMarkerType.addItems(self.markerlist)
        self.cbxLineType.addItems(self.linelist)

    def setComponentsWithLayout(self):
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 2)
        self.layout.setColumnStretch(3, 2)

        self.layout.addWidget(QLabel('색상'), 0, 0)
        self.layout.addWidget(self.cbxColor, 0, 1)
        self.layout.addWidget(QLabel('마커'), 1, 0)
        self.layout.addWidget(self.cbxMarkerType, 1, 1)
        self.layout.addWidget(QLabel('선'), 2, 0)
        self.layout.addWidget(self.cbxLineType, 2, 1)

        self.setLayout(self.layout)


class Panel_Filter(QGroupBox):

    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)
        self.setCheckable(True)
        self.setChecked(False)

        self.filterTypeList = ['jake\'s filter']

        self.cbxFilterType = QComboBox()
        self.layout = QHBoxLayout()

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        # self.chkEnableFilter.stateChanged.connect(self.enableFilter)

    def setItemsInCbx(self):
        self.cbxFilterType.addItems(self.filterTypeList)

    def setComponentsWithLayout(self):
        # self.layout.addWidget(self.chkEnableFilter)
        self.layout.addWidget(QLabel('필터링 알고리즘'))
        self.layout.addWidget(self.cbxFilterType)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    # def enableFilter(self):
    #     if self.chkEnableFilter.isChecked():
    #         self.cbxFilterType.setEnabled(True)
    #     else:
    #         self.cbxFilterType.setEnabled(False)
