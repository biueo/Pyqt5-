from WindowUI import Ui_MainWindow
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QBasicTimer,QDate
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QDesktopWidget,QGridLayout,\
    QInputDialog,QColorDialog,QFileDialog,QHBoxLayout, QVBoxLayout,QMenu,qApp
from BurningWidget import BurningWidget

#自定义控件信号类,QObject可以用于使用属性connec
class Communicate(QObject):
    updateBW = pyqtSignal(int)

class WindowLogic(QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.center()
        self.statusBar().showMessage('Ready')
        # 滑块滑动对应数码管显示
        self.horizontalSlider.valueChanged.connect(self.lcdNumber.display)
        self.setMouseTracking(True)
        self.pushButton_4.clicked.connect(self.whichbuttonclicked)
        self.pushButton_5.clicked.connect(self.whichbuttonclicked)
        self.pushButton_6.clicked.connect(self.showDialog)
        self.pushButton_7.clicked.connect(self.showColorDialog)
        ## fileopen
        self.actionOpen.triggered.connect(self.showFileDialog)
        self.actionOpen.setShortcut("Ctrl+o")
        self.actionOpen.setStatusTip('Open new File')
        self.actionOut.triggered.connect(self.close)
        self.actionOut.setShortcut("Ctrl+q")
        # 自定义控件
        self.c = Communicate()
        self.wid = BurningWidget()
        #滑块滑动，数值信号传输给槽函数changeValue
        self.horizontalSlider_2.valueChanged[int].connect(self.changeValue)
        #change Value 槽函数中updateBW将数值信号传递给槽函数 self.wid.setValue
        self.c.updateBW[int].connect(self.wid.setValue)
        self.verticalLayout_2.addWidget(self.wid)
        # status bar
        self.actionStatus_bar.triggered.connect(self.togglemenu)
        # checkbox
        self.checkBox.stateChanged.connect(self.changeTitle)
        # pushbutton to change color
        self.pushButton_8.clicked.connect(self.changeColor)
        self.pushButton_9.clicked.connect(self.changeColor)
        self.pushButton_10.clicked.connect(self.changeColor)
        # 时间进度条
        self.timer = QBasicTimer()
        self.step =0
        self.pushButton_11.clicked.connect(self.doAction)
        #日历显示
        self.calendarWidget.clicked[QDate].connect(self.showDate)
        #lineedit
        self.lineEdit.textChanged[str].connect(self.changelabel)
        #onActivated
        self.comboBox.activated[str].connect(self.onActivated)

    def onActivated(self,text):
        self.label_5.setText('You select:'+text)
        self.label_5.adjustSize()

    def changelabel(self,text):
        self.label_4.setText('Name:'+text)
        self.label_4.adjustSize()

    def showDate (self,date):
        self.statusbar.showMessage(date.toString())

    def timerEvent(self, e):

        if self.step >= 100:
            self.timer.stop()
            self.pushButton_11.setText('Finished')
            return
        self.step = self.step + 1
        self.label_3.setText('{0}%'.format(self.step))
        self.progressBar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pushButton_11.setText('Start')
        elif self.step >= 100:
            self.step = 0
            self.timer.start(100,self)
            self.pushButton_11.setText('Stop')
        else:
            self.timer.start(100, self)
            self.pushButton_11.setText('Stop')

    def changeColor(self):
        sender = self.sender()
        if sender.text() == "Red":
            self.textBrowser.setStyleSheet("background-color: rgb(255, 0, 0);")
        elif sender.text() == "Blue":
            self.textBrowser.setStyleSheet("background-color: rgb(0, 0, 255);")
        elif sender.text() == "Green":
            self.textBrowser.setStyleSheet("background-color: rgb(0, 255, 0);")

    def changeTitle(self,state):
        if state == Qt.Checked:
            self.setWindowTitle('I have changed the window title')
        else:
            self.setWindowTitle('Learn pyqt5')

    def contextMenuEvent(self, event):

        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            self.close()

    def togglemenu(self,state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def changeValue(self,value):
        self.c.updateBW.emit(value)
        self.wid.repaint()


    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '$FileDir$')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)

    def showColorDialog(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.graphicsView.setStyleSheet("  background-color: %s; "
                                   % col.name())
    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter your name:')
        if ok:
                self.statusBar().showMessage('your name is '+str(text))


    def whichbuttonclicked(self):
        sender = self.sender()
        self.label_2.setText(sender.text()+' was pressed')
        self.statusBar().showMessage(sender.text()+' was pressed')
    # 退出提示框
    def closeEvent(self, event):
        reply = QMessageBox.warning(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Save |
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    # 设置退出键位
    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # 鼠标
    def mouseMoveEvent(self,e):
        x = e.x()
        y = e.y()
        text = "x:{0},Y:{1}".format(x,y)
        self.label.setText(text)
    # 窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_pushButton_clicked(self):

        self.graphicsView_2.setStyleSheet("border-image: url(:/mypic/images/image1.jpg);")

    def on_pushButton_2_clicked(self):

        self.graphicsView_2.setStyleSheet("border-image: url(:/mypic/images/image2.jpg);")

    def on_pushButton_3_clicked(self):

        self.graphicsView_2.setStyleSheet("border-image: url(:/mypic/images/image3.jpg);")
