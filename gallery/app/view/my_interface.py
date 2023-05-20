# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QButtonGroup,QLabel
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit)
from qfluentwidgets import LineEdit
from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.trie import Trie
class LineEdit1(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('Search icons'))
        self.setFixedWidth(305)
        self.textChanged.connect(self.search)
class LineEdit2(LineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(305)
        self.setFixedHeight(100)
class editPromptInterface(GalleryInterface):
    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.my,
            subtitle='114514',
            parent=parent
        )
        self.trie = Trie()
        self.view = QWidget(self)
        self.iconLibraryLabel = QLabel(self.tr('Prompt库'), self)
        #self.searchLineEdit = LineEdit1(self)
        self.input = LineEdit2(self)
        self.input.setText(self.tr('n m s l！'))
        self.input.setClearButtonEnabled(True)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.__initWidget()
    def __initWidget(self):
        self.view.setObjectName('view')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.iconLibraryLabel)
        self.vBoxLayout.addWidget(self.input)
        self.vBoxLayout.setAlignment(Qt.AlignTop)