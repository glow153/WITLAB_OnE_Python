import numpy as np
from PyQt5.QtCore import (Qt, pyqtSlot)
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QVBoxLayout, QWidget)
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from pysparkmgr import PySparkManager
from tabs.daily.panels import (Panel_Datelist, Panel_SelectedDataTable,
                               Panel_Filter)


class TabDaily(QWidget):

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        # init components

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.datelist = Panel_Datelist('날짜 선택')
        # self.gbxAxis = Panel_Axis('y축 설정')
        self.gbxSelDataTbl = Panel_SelectedDataTable('선택된 데이터')
        # self.gbxVisual = Panel_Visual('선 종류')
        self.gbxFilter = Panel_Filter('필터링 적용')
        self.btn_drawPlot = QPushButton("그래프 그리기")

        # Left Layout
        self.leftLayout = self.mainLayout_left()
        # Right Layout
        self.rightLayout = self.mainLayout_right()

        # Main Layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.setStretchFactor(self.leftLayout, 1)
        self.mainLayout.setStretchFactor(self.rightLayout, 0)

        self.setLayout(self.mainLayout)

        # set events
        self.btn_drawPlot.clicked.connect(self.drawLinePlot)

        # get PySparkManager
        self.pysparkmgr = PySparkManager()

    def mainLayout_left(self):
        layout_l = QVBoxLayout()
        layout_l.addWidget(self.canvas)
        return layout_l

    def mainLayout_right(self):
        layout_r = QVBoxLayout()
        layout_r.addWidget(self.datelist)
        layout_r.addWidget(self.gbxSelDataTbl)
        # layout_r.addWidget(self.gbxAxis)
        # layout_r.addWidget(self.gbxVisual)
        layout_r.addWidget(self.gbxFilter)
        layout_r.addWidget(self.btn_drawPlot)
        layout_r.addStretch(1)
        return layout_r

    @pyqtSlot(name='drawPlot')
    def drawLinePlot(self):
        # reset plot
        plt.close()
        self.fig.clear()

        daylist = self.datelist.getCheckedDates()
        self.gbxSelDataTbl.addDataFromSelectedDates()
        selectedColumn = self.gbxSelDataTbl.getSelectedItem()
        plotTitle = ''

        for day in daylist:  # multiple select by checked days
            df = self.pysparkmgr.getDF('nt_srs')

            sel = df.filter('date == "%s"' % day)

            timelist = sel.select('time') \
                .toPandas() \
                .values

            left = sel.select(selectedColumn[0]) \
                .toPandas() \
                .values

            hmlist = [x[0] for x in timelist]
            xtick_list = []
            xticklabel_list = []
            for i in range(0, len(hmlist)):
                if hmlist[i].split(':')[1] == '00':
                    xtick_list.append(i)
                    xticklabel_list.append(hmlist[i].split(':')[0])

            ax_left = self.fig.add_subplot(111)
            ax_left.plot(np.arange(len(timelist)), left,
                         color='blue', label=selectedColumn[0])
            ax_left.set_xticks(xtick_list)
            ax_left.set_xticklabels(xticklabel_list)

            ax_left.set_ylim(0, self.getYlim(selectedColumn[0]))

            ax_left.set_xlabel('time')
            ax_left.set_ylabel(selectedColumn[0])

            if len(selectedColumn) == 2:
                right = sel.select(selectedColumn[1]) \
                    .toPandas() \
                    .values
                ax_right = ax_left.twinx()
                ax_right.plot(np.arange(len(timelist)), right,
                              color='red', label=selectedColumn[1])
                ax_right.set_ylim(0, self.getYlim(selectedColumn[1]))
                ax_right.set_ylabel(selectedColumn[1])

            self.canvas.draw()

    def getYlim(self, type):
        if type == 'illum':
            return 130000
        elif type == 'cct':
            return 12000
        elif type == 'swr':
            return 60

    def makeTimeline(self, timelist):
        hmlist = [x[0] for x in timelist]
        xtick_list = []
        xticklabel_list = []
        for i in range(0, len(hmlist)):
            if hmlist[i].split(':')[1] == '00':
                xtick_list.append(i)
                xticklabel_list.append(hmlist[i].split(':')[0])
