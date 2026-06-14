from .widget_controller import WidgetController
from PySide6.QtWidgets import QLineEdit, QSizePolicy

import sys
from html import unescape
from PySide6.QtWidgets import QLineEdit, QWidget, QSizePolicy
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QPalette, QColor, QPen, QFontMetrics, QPainterPath
from PySide6.QtCore import Signal, Property

class FocusLineEdit(QLineEdit):
    focused_in = Signal()
    focused_out = Signal()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused_in.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focused_out.emit()

class NotchedLineEdit(QWidget):
    def __init__(self, notch_text: str = " ", notch_width: int = 30, notch_height: int = 20,
                 notch_offset: int = 30, radius: int = 10, border_width: int = 2,
                 offset_y: int = 12, parent=None):
        super().__init__(parent)
        self._notch_text = notch_text
        self._notch_w = notch_width
        self._notch_h = notch_height
        self._notch_offset = notch_offset
        self._radius = radius
        self._border_w = border_width
        self._offset_y = max(0, int(offset_y))
        self._base_color = QColor("#cfcfcf")
        self._focus_color = QColor("#1976d2")
        self._invalid_color = QColor("#d32f2f")

        # child QLineEdit that will be visually shifted down by offset_y
        self.line = FocusLineEdit(self)
        self.line.focused_in.connect(self._on_focused_in)
        self.line.focused_out.connect(self._on_focused_out)
        self.line.setProperty("role", "default")
        self.line.setPlaceholderText("No current tab")
        self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # layout is optional; we'll position child manually in resizeEvent
        self.setMinimumHeight(self.line.sizeHint().height() + self._offset_y + int(self._notch_h/2) + 6)

        # allow focus to pass to child
        self.setFocusProxy(self.line)
        self._notch_w = self._compute_notch_w()

    def _on_focused_in(self):
        self.update()

    def _on_focused_out(self):
        self.update()

    def _compute_notch_w(self) -> float:
        # compute from text metrics
        fm = QFontMetrics(self.line.font())
        text = self._notch_text or ""
        # base text width
        text_w = fm.horizontalAdvance(text)
        # padding inside notch (left+right)
        padding = 12
        desired = text_w + padding
        return desired

    def setNotchText(self, text: str):
        self._notch_text = text
        self._notch_w = self._compute_notch_w()
        self.update()

    def setOffsetY(self, oy: int):
        self._offset_y = max(0, int(oy))
        self.setMinimumHeight(self.line.sizeHint().height() + self._offset_y + int(self._notch_h/2) + 6)
        self.update()
        self._reposition_child()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_child()
        self._notch_w = self._compute_notch_w()

    def _reposition_child(self):
        # place the QLineEdit child at y = offset_y, full width minus margins
        left_margin = 8
        right_margin = 8
        w = max(0, self.width() - left_margin - right_margin)
        h = self.line.sizeHint().height()
        self.line.setGeometry(left_margin, self._offset_y * 1.75, w, h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        pen_w = max(1, self._border_w) * 0.5
        inset = pen_w / 2.0

        left = inset + 8   # align with child left_margin
        top = inset + self._offset_y
        right = w - inset - 8
        bottom = h - inset

        # compute notch position
        if self._notch_offset is None:
            notch_x = (w - self._notch_w) / 2.0
        else:
            notch_x = float(self._notch_offset)
        # clamp notch inside left/right with radius margin
        notch_x = max(left + self._radius, min(notch_x, right - self._radius - self._notch_w))
        notch_w = float(min(self._notch_w, right - left - 2 * self._radius))
        notch_h = float(min(self._notch_h, (bottom - top) * 0.6))

        # build path for rounded rect with top notch (notch is a gap in top edge)
        path = QPainterPath()
        r = float(self._radius)

        path.moveTo(left + r, top)
        # left top to before notch
        if notch_x > left + r + 4:
            path.lineTo(notch_x - 4, top)
        else:
            path.lineTo(left + r, top)
        # jump over notch: continue from right side of notch
        path.moveTo(notch_x + notch_w + 4, top)
        path.lineTo(right - r, top)
        path.quadTo(right, top, right, top + r)
        path.lineTo(right, bottom - r)
        path.quadTo(right, bottom, right - r, bottom)
        path.lineTo(left + r, bottom)
        path.quadTo(left, bottom, left, bottom - r)
        path.lineTo(left, top + r)
        path.quadTo(left, top, left + r, top)

        # choose color based on state (invalid property on child or focus)
        invalid = bool(self.line.property("invalid"))
        focused = self.line.hasFocus()
        border_color = self._invalid_color if invalid else (self._focus_color if focused else self._base_color)

        pen = QPen(border_color, pen_w)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        # draw notch background and text above the border (nhô lên)
        if self._notch_text:
            fm = QFontMetrics(self.line.font())
            text = self._notch_text
            text_w = fm.horizontalAdvance(text)
            padding_x = 8
            bg_w = min(notch_w, text_w + padding_x)
            bg_x = notch_x + (notch_w - bg_w) / 2.0

            # desired top for bg: place it above the top edge by half notch height
            desired_bg_top = top - self._offset_y - (notch_h / 2.0)
            # ensure bg_top >= 0 so not clipped
            bg_top = max(0.0, desired_bg_top)
            bg_rect = QRectF(bg_x, bg_top, bg_w, notch_h)

            # draw text centered in bg_rect
            # painter.setPen(QPen(self.line.palette().color(QPalette.Text)))
            painter.setPen(QPen(border_color))
            text_x = bg_x + (bg_w - text_w) / 2.0
            text_y = bg_top + (bg_rect.height() + fm.ascent() - fm.descent()) / 2.0
            painter.drawText(QPointF(text_x, text_y), text)

        painter.end()

    def getBaseColor(self):
        return self._base_color

    def setBaseColor(self, c):
        # accept QColor or color string
        if isinstance(c, QColor):
            self._base_color = c
        else:
            self._base_color = QColor(str(c))
        self.update()

    baseColor = Property(QColor, getBaseColor, setBaseColor)

    def getFocusColor(self):
        return self._focus_color

    def setFocusColor(self, c):
        # accept QColor or color string
        if isinstance(c, QColor):
            self._focus_color = c
        else:
            self._focus_color = QColor(str(c))
        self.update()

    focusColor = Property(QColor, getFocusColor, setFocusColor)

    def getInvalidColor(self):
        return self._invalid_color

    def setInvalidColor(self, c):
        # accept QColor or color string
        if isinstance(c, QColor):
            self._invalid_color = c
        else:
            self._invalid_color = QColor(str(c))
        self.update()

    invalidColor = Property(QColor, getInvalidColor, setInvalidColor)

    def setPlaceholderText(self, text: str):
        self.line.setPlaceholderText(text)

    def setLabel(self, text: str):
        self._notch_text = text
        self._notch_w = self._compute_notch_w()

class TextFieldController(WidgetController):

    def __init__(self):
        super().__init__(layout = None, widget=NotchedLineEdit())
        self.widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.widget.setProperty("role", "default")

    def set_placeholder(self, text: str):
        self.widget.setPlaceholderText(text)

    def set_label(self, text: str):
        self.widget.setLabel(text)