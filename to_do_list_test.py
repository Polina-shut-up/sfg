import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtSql import *
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.uic import loadUi
import shelve


# Создание главного окна
class To_do_list(QMainWindow):
    def __init__(self):
        super(To_do_list, self).__init__()
        loadUi("window.ui", self)
        self.initUI()
    
    
    def __del__(self):
        for model in self.dates:
            del model
            
    
    def initUI(self):
        self.setWindowTitle("Perfect Notes")
        
        self.dates = {}
        
        self.openFile()
        
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        
        self.calendarWidget.selectionChanged.connect(self.calendarItemChanged)
        self.calendarItemChanged()
        date = QDate.currentDate()
        self.calendarWidget.setMinimumDate(date)
        self.calendarWidget.setFocus(QtCore.Qt.NoFocusReason)
        
        
        self.addButton.clicked.connect(self.addRecord)
        self.deleteButton.clicked.connect(self.delRecord)
        self.saveButton.clicked.connect(self.saveRecord)
    
    
    def saveFile(self):
        print(self.dates.values())
        print(self.dates.keys())
        db = shelve.open(r"db.dat", flag="c")
        print(len(self.dates.keys()))
        for key in self.dates.keys():
            model = self.dates[key]
            db[key] = model.getData()
            print(db.get(str(key)))
        db.close()
    
    def openFile(self):
        db = shelve.open(r"db.dat", flag="c")
        keys = db.keys()
        print(len(keys))
        if len(keys) > 0:
            for key in keys:
                value = db.get(key)
                print(key)
                print(value)
                if value != None:
                    model = TableModel(value)
                    print(model)
                    self.dates[key] = model
                    text = str(key)
                    date = QDate(int(text[:4]), int(text[4:6]), int(text[6:]))
                    self.calendarWidget.show_date_func(date)
                    self.calendarWidget.updateCells()
        db.close()
        
        
    def closeEvent(self, event):
        event.accept()
    
            
    def getDate(self):
        return str(self.calendarWidget.selectedDate().toPyDate()).replace("-", "")
    
        
    def calendarItemChanged(self):
        dateSelected = str(self.getDate()).replace("-", "")
        self.updateList(dateSelected)
        
        
    def updateList(self, date):
        if date in self.dates.keys():
            model = self.dates[date]
            self.listView.setModel(model)
            model.sort()     
        else:
            self.listView.setModel(None)
        self.listView.update()

            
    def saveRecord(self):
        self.saveFile()
            
    def addRecord(self):
        date = self.getDate()
        if not date in self.dates.keys():
            model = TableModel()
            self.listView.setModel(model)
            self.dates[date] = model
            self.listView.show()
        else:
            model = self.dates[date]
        
        row = model.rowCount()
        model.insertRow(row, QModelIndex())
        self.listView.update()
        last_index = self.listView.model().index(self.listView.model().rowCount() - 1, 0)
        self.listView.setCurrentIndex(last_index)
        self.listView.update()
        self.calendarWidget.show_date_func(self.calendarWidget.selectedDate())
        self.calendarWidget.updateCells()
        
    def delRecord(self):
        model = self.listView.model()
        if model == None:
            return
        elif model.rowCount() == 0:
            for item in self.dates:
                del item
            date = self.calendarWidget.selectedDate()
            self.calendarWidget.hide_date_func(date)
            self.calendarWidget.updateCell(date)
            return
        
        
        indices = self.listView.selectionModel().selectedIndexes()
        
        for index in sorted(indices):
            model.removeRow(index.row())

    
class TableModel(QAbstractListModel):
    def __init__(self, data = []):
        super().__init__()
        self.data = data
        
    def getData(self):
        return self.data
        
    def rowCount(self, parent = QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.data)
    
    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            return self.data[index.row()]
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.data[row]
            if value == "":
                return "<Введите текст>"
            return value
        if role == QtCore.Qt.ToolTipRole:
            return "<Введите текст>"
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            data_value = value
            self.data[row] = data_value
            self.dataChanged.emit(index, index)
            return True
        
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        flags = QAbstractTableModel.flags(index)
        return index.isValid() if flags | QtCore.Qt.ItemIsEditable else flags
    
    def insertRows(self, row, count, data, parent = QModelIndex()):
        # if parent.isValid():
        #     return False
        
        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(count):
            self.data.insert(row, data)
        self.endInsertRows()
        return True
    
    def removeRows(self, row, count, parent = QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            value = self.data[row]
            self.data.remove(value)
        self.endRemoveRows()
        return True
    
    def sort(self, column = 0, order = QtCore.Qt.AscendingOrder):
        QAbstractItemModel.layoutAboutToBeChanged
        
        if order == QtCore.Qt.AscendingOrder:
            list.sort(self.data, key = str.lower, reverse = False)
        else:
            list.sort(self.data, key = str.lower, reverse = True)
        QAbstractItemModel.layoutChanged
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = To_do_list()
    window.show()
    sys.exit(app.exec_())
