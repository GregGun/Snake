import copy
import random

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPaintEvent, QPainter, QKeyEvent, QColor, QBrush
from PyQt6.QtWidgets import QLabel, QErrorMessage


class Snake(QLabel):
    def __init__(self, parent=None):
        super(Snake, self).__init__(parent)

# Spielfeld(größe) festlegen
        self.__delta = 10
        self.__number_x = 30
        self.__number_y = 25

        self.__w = self.__number_x * self.__delta
        self.__h = self.__number_y * self.__delta
        self.__field = QRect(0, 0, self.__w, self.__h)

        self.setFixedSize(self.__field.size())

        self.__error_message = QErrorMessage()

# Farben für QBrushs definieren
        self.__brush_black = QBrush(QColor("black"))
        self.__brush_yellow = QBrush(QColor("yellow"))
        self.__brush_red = QBrush(QColor("red"))
        self.__brush_green = QBrush(QColor("green"))

# die Schlange (Liste aus Rechtecken) wird erstellt
        self.__list_of_rects = list()
        self.__list_of_rects.append(QRect(15 * self.__delta, 15 * self.__delta, self.__delta, self.__delta))

# Zufällige Anordnung von 'Loot' (hier: Seed("debug")
        random.seed("debug")
        # random.seed()
        self.__loot = self.generate_loot()

# Fenster wird angezeigt
        self.activateWindow()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)

        # paint background
        painter.setBrush(self.__brush_black)
        painter.drawRect(self.__field)

        # paint snake
        for rect in self.__list_of_rects:
            painter.drawRect(rect)
            painter.fillRect(rect, self.__brush_yellow)

# Immer das 1. Rechteck wird grün ausgemalt
        painter.fillRect(self.__list_of_rects[0], self.__brush_green)

        # paint loot
        painter.setBrush(self.__brush_red)
        painter.drawEllipse(self.__loot)

    def keyReleaseEvent(self, ev: QKeyEvent) -> None:
        super(Snake, self).keyReleaseEvent(ev)

# 'Kopf' der Schlange ist bei Index 0
        current_rect = self.__list_of_rects[0]

# hier wird gecheckt, ob wir uns noch im Spielfeld befinden
        if not self.__field.contains(current_rect):
            self.__error_message.showMessage("Out of boundary.")

# befindet sich der 'Kopf' auf dem Feld von 'Loot', dann wird der Schlange ein Rechteck hinzugefügt
        if self.__loot.contains(current_rect):
            self.__list_of_rects.append(QRect(current_rect.x(), current_rect.y(), self.__delta, self.__delta))

            self.__loot = self.generate_loot()

        x = current_rect.x()
        y = current_rect.y()

# pop() letztes element wird genommen und danach wird das letzte Element gelöscht
        last_rect = self.__list_of_rects.pop()

# mit den Pfeiltasten kann die Schlange gesteuert werden
        last_rect.setRect(x, y, self.__delta, self.__delta)
        match ev.key():
            case Qt.Key.Key_Left:
                last_rect.translate(- self.__delta, 0)
            case Qt.Key.Key_Right:
                last_rect.translate(self.__delta, 0)
            case Qt.Key.Key_Up:
                last_rect.translate(0, - self.__delta)
            case Qt.Key.Key_Down:
                last_rect.translate(0, self.__delta)

        self.__list_of_rects.insert(0, last_rect)

        self.update()

# 'Loot' wird an einem zufälligen Ort generiert
    def generate_loot(self):
        loot_x = random.randrange(0, self.__number_x) * self.__delta
        loot_y = random.randrange(0, self.__number_y) * self.__delta

        return QRect(loot_x, loot_y, self.__delta, self.__delta)
