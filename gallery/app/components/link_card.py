# coding:utf-8
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout

from qfluentwidgets import IconWidget, FluentIcon, TextWrap, SingleDirectionScrollArea
from ..common.style_sheet import StyleSheet
from ..common.signal_bus import signalBus

class LinkCard(QFrame):

    def __init__(self, icon, title, content, url, parent=None,routeKey=None):
        super().__init__(parent=parent)
        self.flag=True
        if (url == None or url == ''):
            self.flag=False        
        self.url = QUrl(url) 
        self.setFixedSize(198, 220)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 28, False)[0], self)
        self.urlWidget = IconWidget(FluentIcon.LINK, self)
        self.routekey = routeKey

        self.__initWidget()

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)

        self.iconWidget.setFixedSize(54, 54)
        self.urlWidget.setFixedSize(16, 16)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.urlWidget.move(170, 192)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if (self.flag==False):
            signalBus.switchToSampleCard.emit(self.routekey, 0)
            # QDesktopServices.openUrl(self.url)
        else:
            QDesktopServices.openUrl(self.url)


class LinkCardView(SingleDirectionScrollArea):
    """ Link card view """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Horizontal)
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.hBoxLayout.setContentsMargins(36, 0, 0, 0)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view.setObjectName('view')
        StyleSheet.LINK_CARD.apply(self)

    def addCard(self, icon, title, content, url,routeKey=None):
        """ add link card """
        card = LinkCard(icon, title, content, url, self.view,routeKey)
        self.hBoxLayout.addWidget(card, 0, Qt.AlignLeft)
