from PyQt5.QtWidgets import QCalendarWidget, QApplication
from PyQt5.QtCore import QDate, QPoint, Qt


class Scheduler(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.events = {
        }
        

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        if date in self.events:
            painter.setBrush(Qt.red)
            painter.drawEllipse(rect.topLeft() + QPoint(12, 7), 3, 3) 
            
    def hide_date_func(self, date):
        if date in self.events.keys():
            del self.events[date]
            self.updateCells()

    def show_date_func(self, date):
        self.events[date] = date
    